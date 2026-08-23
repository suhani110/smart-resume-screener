import { useEffect, useState } from "react";
import { api } from "./api";
import CandidateLeaderboard from "./components/CandidateLeaderboard";
import JobForm from "./components/JobForm";
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

  const activeJobTitle = jobs.find((j) => j.id === Number(selectedJobId))?.title;

  return (
    <div className="app">
      <div className="masthead">
        <div className="mark">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path
              d="M4 12c0-4.4 3.6-8 8-8s8 3.6 8 8-3.6 8-8 8"
              stroke="#fff"
              strokeWidth="1.6"
              strokeLinecap="round"
            />
            <circle cx="12" cy="12" r="2.2" fill="#fff" />
            <path d="M4 12h3.2M17 12h3" stroke="#fff" strokeWidth="1.6" strokeLinecap="round" />
          </svg>
        </div>
        <h1>Smart Resume Screener</h1>
      </div>
      <p className="tagline">
        Extract structured signal from a resume, weigh it against a job description, and see a
        ranked, justified shortlist — not just a guess.
      </p>

      <div className="step-rail">
        <span className="step active"><span className="step-num">01</span>Upload</span>
        <span className="step active"><span className="step-num">02</span>Describe role</span>
        <span className="step active"><span className="step-num">03</span>Screen & rank</span>
      </div>

      {error && <p className="error">{error}</p>}

      <div className="grid">
        <ResumeUpload onUploaded={refreshLists} />
        <JobForm onCreated={refreshLists} />
      </div>

      <div className="card">
        <h2>Run a match</h2>
        <p className="hint">Pick one parsed resume and one saved role to score.</p>
        <div className="run-row">
          <select value={selectedResumeId} onChange={(e) => setSelectedResumeId(e.target.value)}>
            <option value="">Select resume…</option>
            {resumes.map((r) => (
              <option key={r.id} value={r.id}>
                {r.candidate_name} — {r.filename}
              </option>
            ))}
          </select>

          <select value={selectedJobId} onChange={(e) => setSelectedJobId(e.target.value)}>
            <option value="">Select job description…</option>
            {jobs.map((j) => (
              <option key={j.id} value={j.id}>
                {j.title}
              </option>
            ))}
          </select>

          <button onClick={handleRunScreening} disabled={!selectedResumeId || !selectedJobId || running}>
            {running ? "Scoring…" : "Run match"}
          </button>
        </div>
      </div>

      <div className="card">
        <h2>Shortlist{activeJobTitle ? ` — ${activeJobTitle}` : ""}</h2>
        <p className="hint">Ranked by match score. Candidates at 7.0+ are auto-shortlisted.</p>
        <CandidateLeaderboard results={results} />
      </div>
    </div>
  );
}
