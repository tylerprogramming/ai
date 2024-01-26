import autogen
import functions
import config

chatbot = autogen.AssistantAgent(
    name="chatbot",
    system_message=f"You are in charge of taking a video file and then caption it after"
                   f"transcribing it.",
    llm_config=config.llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=2,
    code_execution_config= {
        "work_dir": "code",
        "use_docker": False
    }
)

user_proxy.register_function(
    function_map={
        "recognize_transcript_from_video": functions.recognize_transcript_from_video,
    }
)
