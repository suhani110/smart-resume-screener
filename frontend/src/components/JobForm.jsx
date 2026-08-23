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
      <h2>Job description</h2>
      <p className="hint">Required skills are extracted the same way, so both sides compare fairly.</p>
      <input
        type="text"
        placeholder="Role title — e.g. Backend Engineer"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <textarea
        placeholder="Paste the full job description…"
        rows={6}
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button onClick={handleCreate} disabled={!title || !text || loading}>
        {loading ? "Saving…" : "Save job description"}
      </button>
      {error && <p className="error">{error}</p>}
    </div>
  );
}
