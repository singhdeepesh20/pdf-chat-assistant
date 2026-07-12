<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F172A,50:1E3A8A,100:0EA5E9&height=180&section=header&text=PDF%20RAG%20Assistant&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Ask%20questions%20over%20your%20documents%20—%20powered%20by%20retrieval-augmented%20generation&descAlignY=58&descSize=15" width="100%"/>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/ChromaDB-6366F1?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge)

</div>

<img src="assets/architecture.svg" width="100%"/>

## Overview

**PDF RAG Assistant** is a retrieval-augmented generation system that lets you upload a PDF and ask natural-language questions about its contents. The backend chunks and embeds the document, stores the embeddings in a vector database, and retrieves the most relevant passages to ground every answer — reducing hallucination and keeping responses tied to the source material. The frontend is a React single-page app that provides the upload and chat interface.

If the answer isn't present in the uploaded document, the system says so explicitly rather than guessing.

## Features

- **PDF ingestion** — upload any PDF; text is extracted, chunked, and embedded automatically
- **Semantic search** — retrieves the top-k most relevant chunks for a given question via similarity search
- **Grounded answers** — the LLM is instructed to answer only from retrieved context, with an explicit fallback when the answer isn't present
- **Persistent vector store** — embeddings are persisted to disk via ChromaDB, so re-querying doesn't require re-embedding
- **Fast inference** — uses Groq's LPU-backed inference for low-latency responses

## Architecture

| Stage | Component |
|---|---|
| Document loading | `PyPDFLoader` (LangChain) |
| Chunking | `RecursiveCharacterTextSplitter` — 1000-token chunks, 200-token overlap |
| Embeddings | `BAAI/bge-small-en-v1.5` via HuggingFace |
| Vector store | ChromaDB (persisted locally) |
| Retrieval | Similarity search, top-4 chunks |
| Generation | Groq (`openai/gpt-oss-20b`) via `ChatGroq` |
| Orchestration | LangChain retrieval chain (`create_retrieval_chain` + `create_stuff_documents_chain`) |
| Frontend | React.js |

## Tech Stack

**Backend:** FastAPI · LangChain · ChromaDB · HuggingFace Embeddings · Groq
**Frontend:** React.js
**Language:** Python 3.10+, JavaScript

## API Reference

### `POST /upload_pdf`
Uploads a PDF, chunks it, embeds it, and stores it in the vector database.

**Request:** `multipart/form-data` with a `file` field
**Response:**
```json
{
  "message": "PDF uploaded successfully",
  "chunks": 42
}
```

### `POST /ask`
Answers a question using the currently indexed document.

**Request:**
```json
{ "query": "What is the main conclusion of the document?" }
```
**Response:**
```json
{
  "query": "What is the main conclusion of the document?",
  "answer": "..."
}
```
Returns an error if no document has been uploaded yet.

### `GET /`
Health check — confirms the API is running.

> **Note:** the current upload route is registered as `/upload Pdf` (with a space) in `main.py` — likely a typo. Recommend renaming it to `/upload_pdf` for a clean, URL-safe path before deploying.

## Getting Started

### Backend

```bash
git clone https://github.com/singhdeepesh20/pdf-rag-assistant.git
cd pdf-rag-assistant/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

Run the API:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### Frontend

```bash
cd ../frontend
npm install
npm run dev
```

## Project Structure

```
pdf-rag-assistant/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── chroma_db/          # persisted vector store (generated at runtime)
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
└── README.md
```

## Roadmap

- [ ] Multi-document support (query across multiple uploaded PDFs)
- [ ] Streaming responses to the frontend
- [ ] Source citation — show which page/chunk an answer came from
- [ ] Swap local ChromaDB for a hosted vector DB for multi-user deployments

## License

MIT — see [LICENSE](LICENSE) for details.

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0EA5E9,50:1E3A8A,100:0F172A&height=100&section=footer" width="100%"/>
</div>

