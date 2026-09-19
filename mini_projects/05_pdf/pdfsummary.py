import os

os.environ["OPENAI_API_KEY"] = "sk-1111"
os.environ["base_url"] = "http://localhost:1234/v1"

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI

if __name__ == "__main__":
    print("starting")
    pdf_path = "/Users/tylerreed/PycharmProjects/ai/ai_agency_05_pdf/ancient_rome.pdf"
    loader = PyMuPDFLoader(file_path=pdf_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=30)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    # stored in ram in local machine
    vectorstore = FAISS.from_documents(documents=docs, embedding=embeddings)
    vectorstore.save_local("faiss_index_react")

    my_vectorstore = FAISS.load_local("faiss_index_react", embeddings)
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), retriever=my_vectorstore.as_retriever(), chain_type="map_reduce", )
    response = qa.invoke("Summarize Julius Caesar")
    print(response)
    print("done")
