import os
import tempfile

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain,
)
from langchain_classic.chains import (
    create_retrieval_chain,
)

app = FastAPI()



# Global vector store
vectorstore = None


embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


class QueryRequest(BaseModel):
    query: str


@app.post("/upload Pdf")
async def upload_pdf(file: UploadFile = File(...)):
    global vectorstore

    
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf",
    ) as tmp:

        tmp.write(await file.read())
        pdf_path = tmp.name

    try:

        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        # Split documents
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

        chunks = splitter.split_documents(docs)

        # Create vector store
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="chroma_db",
        )

        return {
            "message": "PDF uploaded successfully",
            "chunks": len(chunks),
        }

    finally:
        os.remove(pdf_path)


@app.post("/ask")
async def ask_question(request: QueryRequest):
    global vectorstore

    if vectorstore is None:
        return {
            "error": "Please upload a PDF first."
        }

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )

    llm = ChatGroq(
        model_name="openai/gpt-oss-20b",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,
    )

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
        ),
    ])

    stuff_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=prompt,
    )

    retrieval_chain = create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=stuff_chain,
    )

    response = retrieval_chain.invoke(
        {"input": request.query}
    )

    return {
        "query": request.query,
        "answer": response["answer"],
    }


@app.get("/")
async def root():
    return {
        "message": "FastAPI RAG API is "
    }

