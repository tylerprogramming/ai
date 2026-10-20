"""A minimal AutoGen v0.7 model client that runs a HuggingFace model locally with transformers.

In AutoGen v0.7 a custom model is just a subclass of `ChatCompletionClient`.
You pass an instance of it to `AssistantAgent(model_client=...)` like any other client.
"""
import asyncio
from typing import AsyncGenerator, Sequence, Union

from autogen_core.models import (
    AssistantMessage,
    ChatCompletionClient,
    CreateResult,
    FunctionExecutionResultMessage,
    LLMMessage,
    ModelCapabilities,
    ModelInfo,
    RequestUsage,
    SystemMessage,
    UserMessage,
)
from transformers import AutoModelForCausalLM, GenerationConfig, GPTNeoXTokenizerFast


class CustomModelClient(ChatCompletionClient):
    def __init__(self, model: str, device: str = "cpu", max_length: int = 256):
        print(f"CustomModelClient config: model={model}, device={device}, max_length={max_length}")
        self.device = device
        self.model_name = model
        self.model = AutoModelForCausalLM.from_pretrained(model, trust_remote_code=True).to(self.device)
        self.tokenizer = GPTNeoXTokenizerFast.from_pretrained(model, use_fast=False)
        self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        self.tokenizer.padding_side = "left"

        # How many new tokens to generate per reply.
        self.max_length = max_length
        self._total_usage = RequestUsage(prompt_tokens=0, completion_tokens=0)
        self._last_usage = RequestUsage(prompt_tokens=0, completion_tokens=0)

        print(f"Loaded model {model} to {self.device}")

    # --- helpers ---------------------------------------------------------

    @staticmethod
    def _to_chat_messages(messages: Sequence[LLMMessage]) -> list[dict]:
        """Convert AutoGen messages into the role/content dicts that chat templates expect."""
        chat = []
        for m in messages:
            if isinstance(m, SystemMessage):
                chat.append({"role": "system", "content": m.content})
            elif isinstance(m, UserMessage):
                # content can be a list (text + images); this text-only model keeps just the text.
                content = m.content if isinstance(m.content, str) else "\n".join(c for c in m.content if isinstance(c, str))
                chat.append({"role": "user", "content": content})
            elif isinstance(m, AssistantMessage):
                chat.append({"role": "assistant", "content": str(m.content)})
            elif isinstance(m, FunctionExecutionResultMessage):
                chat.append({"role": "user", "content": "\n".join(r.content for r in m.content)})
        return chat

    def _generate(self, chat: list[dict]) -> tuple[str, int, int]:
        inputs = self.tokenizer.apply_chat_template(chat, return_tensors="pt", add_generation_prompt=True).to(self.device)
        inputs_length = inputs.shape[-1]

        # add inputs_length to max_length
        generation_config = GenerationConfig(
            max_length=self.max_length + inputs_length,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        outputs = self.model.generate(inputs, generation_config=generation_config)
        # Decode only the newly generated text, excluding the prompt
        new_tokens = outputs[0, inputs_length:]
        text = self.tokenizer.decode(new_tokens, skip_special_tokens=True)
        return text, inputs_length, len(new_tokens)

    # --- the ChatCompletionClient interface ------------------------------

    async def create(self, messages, *, tools=[], tool_choice="auto", json_output=None, extra_create_args={}, cancellation_token=None) -> CreateResult:
        # Generation is slow and blocking, so run it in a thread to keep the event loop free.
        text, prompt_tokens, completion_tokens = await asyncio.to_thread(self._generate, self._to_chat_messages(messages))
        self._last_usage = RequestUsage(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens)
        self._total_usage = RequestUsage(
            prompt_tokens=self._total_usage.prompt_tokens + prompt_tokens,
            completion_tokens=self._total_usage.completion_tokens + completion_tokens,
        )
        return CreateResult(finish_reason="stop", content=text, usage=self._last_usage, cached=False)

    async def create_stream(self, messages, *, tools=[], tool_choice="auto", json_output=None, extra_create_args={}, cancellation_token=None) -> AsyncGenerator[Union[str, CreateResult], None]:
        # Local models here don't stream token by token: we just yield the full result once.
        yield await self.create(messages)

    async def close(self) -> None:
        pass  # nothing to clean up

    def actual_usage(self) -> RequestUsage:
        return self._last_usage

    def total_usage(self) -> RequestUsage:
        return self._total_usage

    def count_tokens(self, messages: Sequence[LLMMessage], *, tools=[]) -> int:
        return len(self.tokenizer.apply_chat_template(self._to_chat_messages(messages)))

    def remaining_tokens(self, messages: Sequence[LLMMessage], *, tools=[]) -> int:
        return max(0, self.tokenizer.model_max_length - self.count_tokens(messages))

    @property
    def model_info(self) -> ModelInfo:
        # A plain text model: no tools, images or JSON mode.
        return ModelInfo(vision=False, function_calling=False, json_output=False, family="unknown", structured_output=False)

    @property
    def capabilities(self) -> ModelCapabilities:  # deprecated in v0.7, but still part of the interface
        return ModelCapabilities(vision=False, function_calling=False, json_output=False)
