import autogen
from autogen.coding import LocalCommandLineCodeExecutor


def main():
    config_list = autogen.config_list_from_json(
        env_or_file="OAI_CONFIG_LIST.json"
    )

    # Create a local command line code executor.
    executor = LocalCommandLineCodeExecutor(
        timeout=10,
        work_dir="code",
    )

    assistant = autogen.AssistantAgent(
        name="Assistant",
        llm_config={
            "config_list": config_list
        },
        system_message="If you want the user to save the code in a file before executing it, put # filename: "
                       "<filename> inside the code block as the first line.  You are a helpful assistant.  Return "
                       "'TERMINATE' when the task is done."
    )

    user_proxy = autogen.UserProxyAgent(
        name="user",
        human_input_mode="NEVER",
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        code_execution_config={"executor": executor},
    )

    # trying this out with saving html file!
    user_proxy.initiate_chat(
        assistant,
        message="""
        Create a simple html that opens a simple home page and stylize it
        with some css and save that in a separate file.  Create a simple 
        button on the html page that when clicked, just displays 'Hello!'.
        You can also create a javascript file to make this happen.
        Make sure to comment out the file names at the top of each file.
        """
    )


if __name__ == "__main__":
    main()