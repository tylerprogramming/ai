import autogen
import dotenv

from autogen_transcribe_video.functions import recognize_transcript_from_video, translate_transcript

dotenv.load_dotenv()

config_list = autogen.config_list_from_dotenv(
    dotenv_file_path=".",
    filter_dict={
        "model": ["gpt-4"],
    }
)

llm_config = {
    "functions": [
        {
            "name": "recognize_transcript_from_video",
            "description": "recognize the speech from video and transfer into a txt file",
            "parameters": {
                "type": "object",
                "properties": {
                    "audio_filepath": {
                        "type": "string",
                        "description": "path of the video file",
                    }
                },
                "required": ["audio_filepath"],
            },
        },
        {
            "name": "translate_transcript",
            "description": "using translate_text function to translate the script",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_language": {
                        "type": "string",
                        "description": "source language",
                    },
                    "target_language": {
                        "type": "string",
                        "description": "target language",
                    }
                },
                "required": ["source_language", "target_language"],
            },
        },
    ],
    "config_list": config_list,
    "timeout": 120,
}

chatbot = autogen.AssistantAgent(
    name="chatbot",
    system_message="For coding tasks, only use the functions you have been provided with. Reply TERMINATE when the "
                   "task is done.",
    llm_config=llm_config,
    code_execution_config={"work_dir": "scripts"},
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "scripts", "use_docker": False},
)

user_proxy.register_function(
    function_map={
        "recognize_transcript_from_video": recognize_transcript_from_video,
        "translate_transcript": translate_transcript,
    }
)


def initiate_chat():
    target_video = input("What is your target video path?: ")
    source_language = input("What is the source language? (i.e. English): ")
    target_language = input("What is destination language? (i.e. French): ")

    user_proxy.initiate_chat(
        chatbot,
        message=f"For the video located in {target_video}, recognize the speech and transfer it into a script file, "
                f"then translate from {source_language} text to a {target_language} video subtitle text, and transfer "
                f"it into a script file called transcribed.txt. ",
    )


initiate_chat()
