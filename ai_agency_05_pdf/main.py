import os

import autogen
import dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI
from typing_extensions import Annotated

dotenv.load_dotenv()

# load the pdf file from directory
loaders = [PyPDFLoader('./ancient_rome.pdf')]
docs = []
for file in loaders:
    docs.extend(file.load())
# split text to chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
docs = text_splitter.split_documents(docs)

# pages = loaders[0].load_and_split()
# print(pages[0])

# create a vectorstore
vectorstore = Chroma(
    collection_name="full_documents",
    embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                             model_kwargs={'device': 'cpu'})
)
vectorstore.add_documents(docs)

qa = ConversationalRetrievalChain.from_llm(
    OpenAI(temperature=0),
    vectorstore.as_retriever(),
    memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True)
)

# set config for autogen
config_list = [
    {
        # "base_url": os.getenv("BASE_URL"),
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model": "gpt-3.5-turbo"
    }
]

# set autogen user agent and assistant agent with function calling
llm_config = {
    "timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0.7,
}

# create an AssistantAgent instance "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
)

# create a UserProxyAgent instance "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    code_execution_config=False,
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)


@user_proxy.register_for_execution()
@assistant.register_for_llm(description="PDF Assistant.")
def chat_docs(question: Annotated[str, "The question to be asked"]) -> str:
    response = qa({"question": question})
    return response["answer"]


user_proxy.initiate_chat(
    assistant,
    message="""
Find the answers to the question below from the ancient_rome.pdf and do not write any code.

1. Can you give me a multiple choice question from the pdf with 4 choices and 1 of them being the answer?  Also give the reason for the answer and the page it was found on

Start the work now.
"""
)
