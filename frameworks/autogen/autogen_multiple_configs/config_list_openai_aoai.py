import autogen

config_list = autogen.config_list_openai_aoai(
    key_file_path=".",
    openai_api_key_file="/txt/key_openai.txt",
    aoai_api_key_file="/txt/key_aoai.txt",
    openai_api_base_file="/txt/base_openai.txt",
    aoai_api_base_file="/txt/base_aoai.txt",
    exclude='aoai'
)

print(config_list)
