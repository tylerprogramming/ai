import autogen
from autogen.coding import LocalCommandLineCodeExecutor


def main():
    # Create a local command line code executor.
    executor = LocalCommandLineCodeExecutor(
        timeout=10,
        work_dir="code",
    )

    assistant = autogen.AssistantAgent(
        name="Assistant",
        llm_config={
            "config_list": [
                {
                    "model": "llama3", # replace this with the model you downloaded with ollama pull <model>
                    "base_url": "http://localhost:11434/v1",
                    "api_key": "ollama",
                },
            ],
            # "config_list": [
            #     {
            #         "model": "gpt-4",
            #         "api_key": "your-api-key",
            #     },
            # ],
            "cache_seed": None,
        },
    system_message = """ You are an amazing python developer.  You are especially good at creating games.  You are a 10x Engineer if you didn't know by now.

                        If you want the user to save the code in a file before executing it, put # filename:
                       <filename> inside the code block as the first line.  You are a helpful assistant.  Return
                       'TERMINATE' when the task is done.
                       """
    )

    user_proxy = autogen.UserProxyAgent(
        name="user",
        human_input_mode="ALWAYS",
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        code_execution_config={"executor": executor},
    )

    # trying this out with saving html file!
    user_proxy.initiate_chat(
        assistant,
        message="""
            I want you to create the python code for the game snake.  Be thorough and make sure you implement all the
            rules for the game properly.  Only code the game, no documentation.
        """)


if __name__ == "__main__":
    main()
