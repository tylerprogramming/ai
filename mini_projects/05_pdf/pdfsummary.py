"""Summarize a PDF with LangChain (FAISS index + map-reduce RetrievalQA).

Usage:  python pdfsummary.py path/to/file.pdf ["question"]

Uses OpenAI by default (OPENAI_API_KEY in .env). To use a local OpenAI-compatible server
such as LM Studio instead, set OPENAI_BASE_URL=http://localhost:1234/v1 (and any OPENAI_API_KEY).
"""
import os
import sys

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

load_dotenv()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python pdfsummary.py path/to/file.pdf [\"question\"]")
    pdf_path = sys.argv[1]
    question = sys.argv[2] if len(sys.argv) > 2 else "Summarize this document"

    print("starting")
    loader = PyMuPDFLoader(file_path=pdf_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=30)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    # stored in ram in local machine, and saved next to this script
    index_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "faiss_index_react")
    vectorstore = FAISS.from_documents(documents=docs, embedding=embeddings)
    vectorstore.save_local(index_dir)

    # FAISS indexes are pickled; only load ones you created yourself (like the one saved above)
    my_vectorstore = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
    llm = ChatOpenAI(model="gpt-5.4-mini")
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=my_vectorstore.as_retriever(), chain_type="map_reduce")
    response = qa.invoke(question)
    print(response["result"])
    print("done")
