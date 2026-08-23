import { useState } from "react";
import { api } from "../api";

export default function ResumeUpload({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError("");
    try {
      const resume = await api.uploadResume(file);
      onUploaded(resume);
      setFile(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>1. Upload Resume</h2>
      <input
        type="file"
        accept=".pdf,.txt"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={handleUpload} disabled={!file || loading}>
        {loading ? "Parsing..." : "Upload & Parse"}
      </button>
      {error && <p className="error">{error}</p>}
    </div>
  );
}
