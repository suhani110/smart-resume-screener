import { useState } from "react";
import { api } from "../api";

export default function JobForm({ onCreated }) {
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleCreate = async () => {
    if (!title || !text) return;
    setLoading(true);
    setError("");
    try {
      const job = await api.createJob(title, text);
      onCreated(job);
      setTitle("");
      setText("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>2. Add Job Description</h2>
      <input
        type="text"
        placeholder="Job title (e.g. Backend Engineer)"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <textarea
        placeholder="Paste the full job description here..."
        rows={6}
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button onClick={handleCreate} disabled={!title || !text || loading}>
        {loading ? "Saving..." : "Save Job Description"}
      </button>
      {error && <p className="error">{error}</p>}
    </div>
  );
}
