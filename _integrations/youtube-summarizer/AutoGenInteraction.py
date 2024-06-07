import autogen


class AutoGenInteraction:
    def __init__(self, api_key, transcription):
        self.llm_config = {
            "config_list": [{
                "model": "gpt-3.5-turbo",
                "api_key": api_key
            }],
            "temperature": 0,
            "cache_seed": None
        }
        self.transcription = transcription

    def initiate_chat(self):
        user = autogen.UserProxyAgent(
            "user",
            system_message="You are an administrator.",
            human_input_mode="NEVER",
            is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
            code_execution_config=False,
        )

        agent_summarizer = autogen.AssistantAgent(
            "agent_summarizer",
            system_message="You are an assistant agent. When you are done, reply with TERMINATE",
            llm_config=self.llm_config
        )

        agent_translator = autogen.AssistantAgent(
            "ai_agent_translator",
            system_message="You are an assistant agent. When you are done, reply with TERMINATE",
            llm_config=self.llm_config
        )

        user.initiate_chats(
            [
                {
                    "recipient": agent_summarizer,
                    "message": f"Can you summarize: {self.transcription} this nicely with the title and then bullet points?",
                    "clear_history": True,
                    "silent": False,
                    "summary_method": "last_msg",
                },
                {
                    "recipient": agent_translator,
                    "message": "Can you translate this into Dutch?",
                    "summary_method": "last_msg",
                },
            ]
        )
