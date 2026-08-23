import { useEffect, useState } from "react";
import { api } from "./api";
import JobForm from "./components/JobForm";
import ResultsTable from "./components/ResultsTable";
import ResumeUpload from "./components/ResumeUpload";

export default function App() {
  const [resumes, setResumes] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [selectedResumeId, setSelectedResumeId] = useState("");
  const [selectedJobId, setSelectedJobId] = useState("");
  const [results, setResults] = useState([]);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");

  const refreshLists = async () => {
    const [r, j] = await Promise.all([api.listResumes(), api.listJobs()]);
    setResumes(r);
    setJobs(j);
  };

  useEffect(() => {
    refreshLists().catch((e) => setError(e.message));
  }, []);

  useEffect(() => {
    if (!selectedJobId) {
      setResults([]);
      return;
    }
    api
      .listResultsForJob(selectedJobId)
      .then(setResults)
      .catch((e) => setError(e.message));
  }, [selectedJobId]);

  const handleRunScreening = async () => {
    if (!selectedResumeId || !selectedJobId) return;
    setRunning(true);
    setError("");
    try {
      await api.runScreening(Number(selectedResumeId), Number(selectedJobId));
      const updated = await api.listResultsForJob(selectedJobId);
      setResults(updated);
    } catch (err) {
      setError(err.message);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>🧠 Smart Resume Screener</h1>
        <p className="muted">Upload resumes, add a job description, and get LLM-scored, justified matches.</p>
      </header>

      {error && <p className="error">{error}</p>}

      <div className="grid">
        <ResumeUpload onUploaded={refreshLists} />
        <JobForm onCreated={refreshLists} />
      </div>

      <div className="card">
        <h2>3. Run Screening</h2>
        <div className="run-row">
          <select value={selectedResumeId} onChange={(e) => setSelectedResumeId(e.target.value)}>
            <option value="">Select resume...</option>
            {resumes.map((r) => (
              <option key={r.id} value={r.id}>
                {r.candidate_name} ({r.filename})
              </option>
            ))}
          </select>

          <select value={selectedJobId} onChange={(e) => setSelectedJobId(e.target.value)}>
            <option value="">Select job description...</option>
            {jobs.map((j) => (
              <option key={j.id} value={j.id}>
                {j.title}
              </option>
            ))}
          </select>

          <button onClick={handleRunScreening} disabled={!selectedResumeId || !selectedJobId || running}>
            {running ? "Scoring..." : "Run Match"}
          </button>
        </div>
      </div>

      <div className="card">
        <h2>4. Results {selectedJobId ? `for "${jobs.find((j) => j.id === Number(selectedJobId))?.title || ""}"` : ""}</h2>
        <ResultsTable results={results} />
      </div>
    </div>
  );
}
