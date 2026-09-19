import json
import os
from datetime import datetime

import autogen
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
            "temperature": 0,
        }

        # create an AssistantAgent instance "assistant"
        assistant = autogen.AssistantAgent(
            name="assistant",
            system_message="As the assistant agent, the question, multiple choice answers, the answer to the "
                           "question, and the reason should be put into json format and returned in proper format.",
            llm_config=llm_config,
        )

        json_assistant = autogen.AssistantAgent(
            name="json_assistant",
            system_message="As the json assistant agent, my only purpose is to take the response from the assistant "
                           "agent,"
                           "and format the question, multiple choices answers, the answer to the question and the "
                           "reason"
                           "and put them into a json format.",
            llm_config=llm_config
        )

        converter = autogen.AssistantAgent(
            name="converter",
            system_message="I only convert the response given to me to json format, and that is all and return it.",
            llm_config=llm_config
        )

        # create a UserProxyAgent instance "user_proxy"
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
            code_execution_config=False,
            llm_config=llm_config
        )


        @user_proxy.register_for_execution()
        @assistant.register_for_llm(description="PDF Assistant.")
        def ask_question(question: Annotated[str, "The question to be asked"]) -> json:
            response = qa({"question": question})
            current_json = json.dumps(response["answer"])
            cleaner_json_content = current_json.replace("\\", "").replace("\n", "")
            return json.dumps(cleaner_json_content)


        @user_proxy.register_for_execution()
        @json_assistant.register_for_llm(description="JSON Formatter")
        def json_format(mcq: Annotated[str, "The converted json to be saved"]) -> str:
            with open(file_name, 'w') as json_file:
                json.dump(mcq, json_file, indent=2)
            return mcq


        chat_results = user_proxy.initiate_chats(
            [
                {
                    "recipient": assistant,
                    "message": """
                        Find the answers to the question below from the {uploaded_file} and do not write any code.
        
                        1. Can you give me a multiple choice question from the pdf with 4 choices and 1 of them being the answer?  Also give the reason for the answer and the page it was found on.
                        2. Make all the choices under the property choices, and the answer to be called correct_answer
                    """,
                    "clear_history": True,
                    "silent": False,
                },
                {
                    "recipient": converter,
                    "message": """
                        The only job here is to convert the json from previous agent into json format 
                        and also remove newline characters and return updated json format.
                    """,
                    "summary_method": "last_msg"
                },
                {
                    "recipient": json_assistant,
                    "message": """
                        Take the context from the assistant and convert it to json and save it to disk to a 
                        json file in this directory.
                     """,
                    "summary_method": "reflection_with_llm",
                    "carryover": "I want to save this to disk with the name tester.json"
                }
            ]
        )

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
