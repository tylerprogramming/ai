import json
import os
from datetime import datetime

import dotenv
import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI
from typing_extensions import Annotated

import agents

dotenv.load_dotenv()

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
            OpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0),
            vectorstore.as_retriever(),
            memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        )


        @agents.user_proxy.register_for_execution()
        @agents.assistant.register_for_llm(description="PDF Assistant.")
        def ask_question(question: Annotated[str, "The question to be asked"]) -> json:
            response = qa({"question": question})
            current_json = json.dumps(response["answer"])
            cleaner_json_content = current_json.replace("\\", "").replace("\n", "")
            return json.dumps(cleaner_json_content)


        @agents.user_proxy.register_for_execution()
        @agents.json_assistant.register_for_llm(description="JSON Formatter")
        def save_file(mcq: Annotated[str, "The converted json to be saved"]) -> str:
            with open(file_name, 'w') as new_json:
                json.dump(mcq, new_json, indent=2)
            return mcq


        chat_results = agents.initiate_agent_chats()

        # Read JSON data from the file
        with open(file_name, 'r') as json_file:
            json_data = json.load(json_file)

        # Retrieve the "question" property
        question = json_data.get("question", None)
        correct_answer = json_data.get("correct_answer", None)
        reason = json_data.get("reason", None)
        choice_a = json_data.get("choices", {}).get("A", None)
        choice_b = json_data.get("choices", {}).get("B", None)
        choice_c = json_data.get("choices", {}).get("C", None)
        choice_d = json_data.get("choices", {}).get("D", None)

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