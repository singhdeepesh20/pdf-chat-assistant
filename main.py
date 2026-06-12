from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile
import os

# Document loading
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

# Text splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Vector store
from langchain_community.vectorstores import Chroma

# Embeddings
from langchain_huggingface import HuggingFaceEmbeddings

# Prompting
from langchain_core.prompts import ChatPromptTemplate

# LLM
from langchain_groq import ChatGroq

# Chains
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)
from langchain_classic.chains import create_retrieval_chain

document_loader=DirectoryLoader(
    "data",
    glob="*.pdf",
    loader_cls=PyPDFLoader
)

docs=document_loader.load()


text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)

chunks=text_splitter.split_documents(docs)

embeddings=HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

vectorstore=Chroma.from_documnets(chunks,embeddings,persist_directory="chroma_db")

retriever=vectorstore.as_retriever(search_type="similarity",search_kwargs={"k":4})

query= "what is roadmap for basic rag ?"

llm=ChatGroq(model_name="openai/gpt-oss-20b",api_key=os.getenv("GROQ_API_KEY"),temperature=0)


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a helpful assistant.

        Use ONLY the provided context.
        If the answer is not present, say:
        "I don't have enough information in the documents."
        """
    ),
    (
        "human",
        """
        Context:
        {context}

        Question:
        {input}
        """
    )
])

stuff_chain=create_stuff_documents_chain(llm=llm,prompt=prompt)

retrieval_chain=create_retrieval_chain(retriever=retriever,combine_documents_chain=stuff_chain)


response=retrieval_chain.run({"input":query})

print(response)
