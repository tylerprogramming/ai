import asyncio
import json
from datetime import datetime

import dotenv
import streamlit as st
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI
from typing_extensions import Annotated

dotenv.load_dotenv()  # OPENAI_API_KEY from .env


async def create_question(qa, file_name):
    """Have the agents write a multiple choice question from the PDF and save it to file_name as json."""
    # set the model client for autogen
    model_client = OpenAIChatCompletionClient(model="gpt-5.4-mini", temperature=0, seed=42, timeout=600)

    # the tools are plain functions with type hints, given to the agents that call them
    def ask_question(question: Annotated[str, "The question to be asked"]) -> json:
        """PDF Assistant."""
        response = qa({"question": question})
        current_json = json.dumps(response["answer"])
        cleaner_json_content = current_json.replace("\\", "").replace("\n", "")
        return json.dumps(cleaner_json_content)

    def json_format(mcq: Annotated[str, "The converted json to be saved"]) -> str:
        """JSON Formatter"""
        with open(file_name, 'w') as json_file:
            json.dump(mcq, json_file, indent=2)
        return mcq

    # create an AssistantAgent instance "assistant"
    assistant = AssistantAgent(
        name="assistant",
        system_message="As the assistant agent, the question, multiple choice answers, the answer to the "
                       "question, and the reason should be put into json format and returned in proper format.",
        model_client=model_client,
        tools=[ask_question],
        reflect_on_tool_use=True,
    )

    json_assistant = AssistantAgent(
        name="json_assistant",
        system_message="As the json assistant agent, my only purpose is to take the response from the assistant "
                       "agent,"
                       "and format the question, multiple choices answers, the answer to the question and the "
                       "reason"
                       "and put them into a json format.",
        model_client=model_client,
        tools=[json_format],
        reflect_on_tool_use=True,
    )

    converter = AssistantAgent(
        name="converter",
        system_message="I only convert the response given to me to json format, and that is all and return it.",
        model_client=model_client,
    )

    # The old initiate_chats ran these chats one after another, carrying the earlier chats'
    # results over into the next one. Here each agent gets its message plus that carryover.
    chats = [
        (assistant, """
            Find the answers to the question below from the {uploaded_file} and do not write any code.

            1. Can you give me a multiple choice question from the pdf with 4 choices and 1 of them being the answer?  Also give the reason for the answer and the page it was found on.
            2. Make all the choices under the property choices, and the answer to be called correct_answer
        """, []),
        (converter, """
            The only job here is to convert the json from previous agent into json format 
            and also remove newline characters and return updated json format.
        """, []),
        (json_assistant, """
            Take the context from the assistant and convert it to json and save it to disk to a 
            json file in this directory.
         """, ["I want to save this to disk with the name tester.json"]),
    ]

    carryover = []
    try:
        for agent, message, extra_carryover in chats:
            context = "\n".join(extra_carryover + carryover)
            task = f"{message}\nContext:\n{context}" if context else message
            result = await agent.run(task=task)
            carryover.append(result.messages[-1].to_text())  # like summary_method="last_msg"
    finally:
        await model_client.close()


with st.sidebar:
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        st.write("File uploaded successfully!")

if uploaded_file is not None:
    current_timestamp = datetime.timestamp(datetime.now())
    file_name = 'question-' + str(int(current_timestamp)) + '.json'

    # Enable button if PDF is uploaded
    button_enabled = st.sidebar.button("Create a Question!")

    # load the pdf file from directory
    file = PyMuPDFLoader(uploaded_file.name)

    if button_enabled:
        docs = []
        docs.extend(file.load())

        # split text to chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
        docs = text_splitter.split_documents(docs)

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

        # AutoGen v0.7 is async, so run the agents with asyncio.run inside the Streamlit script
        asyncio.run(create_question(qa, file_name))

        # Read JSON data from the file
        with open(file_name, 'r') as json_file:
            json_data = json.load(json_file)

        cleaned_json_content = json_data.replace("\\", "").replace("\n", "")

        new_json = json.loads(cleaned_json_content)

        # Retrieve the "question" property
        question = new_json.get("question", None)
        correct_answer = new_json.get("correct_answer", None)
        reason = new_json.get("reason", None)
        choice_a = new_json.get("choices", {}).get("A", None)
        choice_b = new_json.get("choices", {}).get("B", None)
        choice_c = new_json.get("choices", {}).get("C", None)
        choice_d = new_json.get("choices", {}).get("D", None)

        st.header('The Question', divider='rainbow')
        st.subheader(question)

        c1, c2 = st.columns(2)

        with c1:
            st.info(choice_a)
            st.info(choice_b)
        with c2:
            st.info(choice_c)
            st.info(choice_d)

        st.caption("The Correct Answer:")
        st.subheader(correct_answer)

        st.caption("The Reason:")
        st.subheader(reason)
