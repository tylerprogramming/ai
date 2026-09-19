import os
import chromadb
import autogen

from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.agentchat.contrib.vectordb.chromadb import ChromaVectorDB
from chromadb.utils import embedding_functions

from dotenv import load_dotenv

load_dotenv()

config_list = autogen.config_list_from_json("OAI_CONFIG_LIST.json")

CHROMA_DB_PATH="/tmp/chromadb"
CHROMA_COLLECTION="autogen-rag-chroma"

chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(name=CHROMA_COLLECTION)

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name="text-embedding-ada-002")

vector_db = ChromaVectorDB(path=CHROMA_DB_PATH, embedding_function=openai_ef)

assistant = AssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    llm_config={
        "timeout": 600,
        "config_list": config_list,
    },
)

ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "qa",
        "docs_path": [
            "https://raw.githubusercontent.com/microsoft/autogen/refs/heads/main/README.md",
            "./docs"
        ],
        "chunk_token_size": 2000,
        "model": config_list[2]["model"],
        "vector_db": vector_db,
        "overwrite": False,  # set to True if you want to overwrite an existing collection
        "get_or_create": True,  # set to False if don't want to reuse an existing collection
        "collection_name": CHROMA_COLLECTION,
        "embedding_function": openai_ef,
        "context_max_tokens": 10000,
    },
    code_execution_config=False,  # set to False if you don't want to execute the code
)

qa_problem = "What is Autogen Studio?  Please give a detailed overview of the project."
chat_result = ragproxyagent.initiate_chat(
    assistant, message=ragproxyagent.message_generator, problem=qa_problem, n_results=2
)

# Check the last entry for "UPDATE CONTEXT", otherwise print the last entry
if chat_result.chat_history[-1]['content'] == 'UPDATE CONTEXT':
    for entry in reversed(chat_result.chat_history[:-1]):  # Exclude the last entry
        if entry['role'] == 'user':
            print(entry['content'])  # Output the content of the found entry
            break
else:
    print(chat_result.chat_history[-1]['content'])
