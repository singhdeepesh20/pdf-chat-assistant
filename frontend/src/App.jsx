import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

function App() {
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [chunks, setChunks] = useState(null);
  const [query, setQuery] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loadingUpload, setLoadingUpload] = useState(false);
  const [loadingAsk, setLoadingAsk] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files?.[0] || null);
    setUploadMessage("");
    setChunks(null);
    setError("");
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a PDF file before uploading.");
      return;
    }

    setLoadingUpload(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Upload failed. Please try again.");
        return;
      }

      setUploadMessage(data.message || "PDF uploaded successfully.");
      setChunks(data.chunks ?? null);
      setChatHistory((history) => [
        ...history,
        { role: "system", text: "PDF uploaded successfully." },
      ]);
    } catch (err) {
      setError("Unable to upload PDF. Check backend status and try again.");
    } finally {
      setLoadingUpload(false);
    }
  };

  const handleAsk = async () => {
    if (!query.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoadingAsk(true);
    setError("");

    try {
      const response = await fetch(`${API_BASE}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: query.trim() }),
      });

      const data = await response.json();

      if (!response.ok || data.error) {
        setError(data.error || "Unable to fetch an answer.");
        return;
      }

      setChatHistory((history) => [
        ...history,
        { role: "user", text: query.trim() },
        { role: "assistant", text: data.answer || "No answer returned." },
      ]);
      setQuery("");
    } catch (err) {
      setError("Error asking question. Check backend connectivity.");
    } finally {
      setLoadingAsk(false);
    }
  };

  return (
    <div className="app-shell">
      <header>
        <h1>PDF Chat Assistant</h1>
        <p>Upload a PDF and chat with its content.</p>
      </header>

      <section className="panel">
        <div className="upload-card">
          <h2>Upload PDF</h2>
          <input type="file" accept="application/pdf" onChange={handleFileChange} />
          <button onClick={handleUpload} disabled={loadingUpload}>
            {loadingUpload ? "Uploading..." : "Upload PDF"}
          </button>
          {uploadMessage && <p className="success">{uploadMessage}</p>}
          {chunks !== null && (
            <p className="meta">Chunks created: {chunks}</p>
          )}
        </div>

        <div className="chat-card">
          <h2>Ask a question</h2>
          <textarea
            rows="4"
            placeholder="Enter your question here..."
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
          <button onClick={handleAsk} disabled={loadingAsk || !uploadMessage}>
            {loadingAsk ? "Thinking..." : "Ask"}
          </button>
          {!uploadMessage && (
            <p className="hint">Upload a PDF first to enable question answering.</p>
          )}
        </div>
      </section>

      {error && <div className="toast error">{error}</div>}

      <section className="history-card">
        <h2>Conversation</h2>
        {chatHistory.length === 0 && <p>No messages yet.</p>}
        <div className="messages">
          {chatHistory.map((item, index) => (
            <div key={`${item.role}-${index}`} className={`message ${item.role}`}>
              <span className="role-label">{item.role === "assistant" ? "Assistant" : item.role === "user" ? "You" : "System"}</span>
              <p>{item.text}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default App;
