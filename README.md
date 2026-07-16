<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F172A,50:1E3A8A,100:0EA5E9&height=200&section=header&text=PDF%20RAG%20Assistant&fontSize=44&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Retrieval-Augmented%20Question%20Answering%20over%20PDF%20Documents&descAlignY=58&descSize=16" width="100%" />

# PDF RAG Assistant

### Ask Questions Over PDFs Using Retrieval-Augmented Generation (RAG)

<p>
A production-inspired document intelligence system built with <b>FastAPI</b>, <b>LangChain</b>, <b>ChromaDB</b>, <b>React</b>, and <b>Groq</b>.
Upload a PDF, retrieve relevant context through semantic search, and generate grounded answers using an LLM.
</p>

<p>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/ChromaDB-6366F1?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge)

</p>

</div>

---

## Overview

**PDF RAG Assistant** is a Retrieval-Augmented Generation (RAG) application that enables users to interact with PDF documents using natural language.

Instead of relying solely on an LLM's internal knowledge, the system retrieves the most relevant sections of the uploaded document through semantic similarity search and uses them as context for answer generation.

This retrieval-first workflow significantly reduces hallucinations and ensures responses remain grounded in the uploaded document.

---

## Demo Architecture

<p align="center">
<img src="assets/architecture.svg" width="100%">
</p>

---

# Key Features

### Document Processing

- Upload PDF documents
- Automatic text extraction
- Intelligent recursive chunking
- Embedding generation using HuggingFace models

### Semantic Retrieval

- Vector similarity search
- Top-k document retrieval
- Persistent ChromaDB storage
- Fast semantic lookup

### Grounded Generation

- Context-aware answers
- Hallucination reduction
- Explicit fallback when information is unavailable
- Groq-powered low latency inference

### Modern API

- FastAPI backend
- RESTful endpoints
- React frontend
- Easy deployment

---

# System Architecture

```text
                  Upload PDF
                       │
                       ▼
             PyPDFLoader (LangChain)
                       │
                       ▼
       RecursiveCharacterTextSplitter
        Chunk Size: 1000 | Overlap: 200
                       │
                       ▼
      HuggingFace Embedding Model
      BAAI/bge-small-en-v1.5
                       │
                       ▼
                Chroma Vector DB
              (Persistent Storage)
                       │
               Similarity Search
                  Top K = 4
                       │
                       ▼
         Retrieved Relevant Chunks
                       │
                       ▼
          LangChain Retrieval Chain
                       │
                       ▼
              ChatGroq (GPT-OSS)
                       │
                       ▼
               Grounded Response
```

---

# Tech Stack

| Category | Technologies |
|-----------|--------------|
| Backend | FastAPI, LangChain |
| Frontend | React.js |
| Vector Database | ChromaDB |
| Embeddings | HuggingFace BAAI/bge-small-en-v1.5 |
| LLM | Groq (GPT-OSS 20B) |
| Language | Python 3.10+, JavaScript |

---
<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0EA5E9,50:1E3A8A,100:0F172A&height=100&section=footer" width="100%"/>
</div>

