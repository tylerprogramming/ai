from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


class AutoGenInteraction:
    def __init__(self, api_key, transcription):
        self.model_client = OpenAIChatCompletionClient(
            model="gpt-5.4-mini",
            api_key=api_key,
            # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
            model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
            # temperature=0 removed: gpt-5 models only accept the default temperature
        )
        self.transcription = transcription

    async def initiate_chat(self):
        # Each agent.run() is one turn, so the agents no longer need to reply with TERMINATE
        agent_summarizer = AssistantAgent(
            "agent_summarizer",
            model_client=self.model_client,
            system_message="You are an assistant agent.",
        )

        agent_translator = AssistantAgent(
            "ai_agent_translator",
            model_client=self.model_client,
            system_message="You are an assistant agent.",
        )

        # Chat 1: summarize the transcription
        result = await Console(agent_summarizer.run_stream(
            task=f"Can you summarize: {self.transcription} this nicely with the title and then bullet points?"
        ))
        summary = result.messages[-1].content  # "last_msg" summary, carried over to the next chat

        # Chat 2: translate the summary
        await Console(agent_translator.run_stream(
            task=f"Can you translate this into Dutch?\n\nContext:\n{summary}"
        ))

        await self.model_client.close()
