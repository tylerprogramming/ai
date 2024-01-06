import autogen

config_list = autogen.config_list_from_dotenv(
    dotenv_file_path=".",
    filter_dict={
        "model": ["gpt-4"],
    }
)

# config_list = [
#     {
#         "model": "NULL",
#         "base_url": os.getenv("base_url"),
#         "api_key": "NULL",
#     },
# ]

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
                    },
                    "new_file_name": {
                        "type": "string",
                        "description": "new file name that will be captioned"
                    }
                },
                "required": ["audio_filepath", "new_file_name"],
            },
        }
    ],
    "config_list": config_list,
    "timeout": 120,
}
