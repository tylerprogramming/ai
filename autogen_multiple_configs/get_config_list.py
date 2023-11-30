import autogen

api_keys = ["SAMPLE_API_KEY"]
api_bases = ["http://localhost:8001"]
api_type = "openai"
api_version = "api-preview-01"

config_list = autogen.get_config_list(
    api_keys,
    api_bases,
    api_type,
    api_version
)

print(config_list)
