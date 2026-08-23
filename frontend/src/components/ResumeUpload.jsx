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
      <h2>Upload resume</h2>
      <p className="hint">PDF or TXT — skills, education, and experience are extracted automatically.</p>
      <div className="dropzone">
        Drop a file or browse
        <div>
          <input
            type="file"
            accept=".pdf,.txt"
            onChange={(e) => setFile(e.target.files[0])}
          />
        </div>
        {file && <div className="file-picked">{file.name}</div>}
      </div>
      <div style={{ marginTop: 14 }}>
        <button onClick={handleUpload} disabled={!file || loading}>
          {loading ? "Parsing…" : "Upload & parse"}
        </button>
      </div>
      {error && <p className="error">{error}</p>}
    </div>
  );
}
