from transformers import AutoTokenizer, GenerationConfig, AutoModelForCausalLM, GPTNeoXTokenizerFast
from types import SimpleNamespace


class CustomModelClient:
    def __init__(self, config, **kwargs):
        print(f"CustomModelClient config: {config}")
        self.device = config.get("device", "cpu")
        self.model = AutoModelForCausalLM.from_pretrained(config["model"], trust_remote_code=True).to(self.device)
        self.model_name = config["model"]
        self.tokenizer = GPTNeoXTokenizerFast.from_pretrained(config["model"], use_fast=False)
        self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        self.tokenizer.padding_side = 'left'

        messages = [
            {
                "role": "system",
                "content": "You are a friendly chatbot who always responds in the style of a pirate",
            },
        ]
        self.tokenizer.apply_chat_template(messages)

        # params are set by the user and consumed by the user since they are providing a custom model
        # so anything can be done here
        gen_config_params = config.get("params", {})
        self.max_length = gen_config_params.get("max_length", 256)

        print(f"Loaded model {config['model']} to {self.device}")

    def create(self, params):
        if params.get("stream", False) and "messages" in params:
            raise NotImplementedError("Local models do not support streaming.")
        else:
            num_of_responses = params.get("n", 1)

            # can create my own data response class
            # here using SimpleNamespace for simplicity
            # as long as it adheres to the ClientResponseProtocol

            response = SimpleNamespace()

            inputs = self.tokenizer.apply_chat_template(
                params["messages"], return_tensors="pt", add_generation_prompt=True
            ).to(self.device)
            inputs_length = inputs.shape[-1]

            # add inputs_length to max_length
            max_length = self.max_length + inputs_length
            generation_config = GenerationConfig(
                max_length=max_length,
                eos_token_id=self.tokenizer.eos_token_id,
                pad_token_id=self.tokenizer.eos_token_id,
            )

            response.choices = []
            response.model = self.model_name

            for _ in range(num_of_responses):
                outputs = self.model.generate(inputs, generation_config=generation_config)
                # Decode only the newly generated text, excluding the prompt
                text = self.tokenizer.decode(outputs[0, inputs_length:])
                choice = SimpleNamespace()
                choice.message = SimpleNamespace()
                choice.message.content = text
                choice.message.function_call = None
                response.choices.append(choice)

            return response

    @staticmethod
    def message_retrieval(self, response):
        """Retrieve the messages from the response."""
        choices = response.choices
        return [choice.message.content for choice in choices]

    @staticmethod
    def cost(self, response) -> float:
        """Calculate the cost of the response."""
        response.cost = 0
        return 0

    @staticmethod
    def get_usage(response):
        # returns a dict of prompt_tokens, completion_tokens, total_tokens, cost, model
        # if usage needs to be tracked, else None
        return {}
