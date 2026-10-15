const BASE_URL = "https://smart-resume-screener-1-hsfz.onrender.com";

async function handle(res) {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed with status ${res.status}`);
  }
  return res.json();
}

export const api = {
  uploadResume: (file) => {
    const formData = new FormData();
    formData.append("file", file);
    return fetch(`${BASE_URL}/resumes/upload`, { method: "POST", body: formData }).then(handle);
  },
  listResumes: () => fetch(`${BASE_URL}/resumes`).then(handle),
  createJob: (title, raw_text) =>
    fetch(`${BASE_URL}/jobs`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, raw_text }),
    }).then(handle),
  listJobs: () => fetch(`${BASE_URL}/jobs`).then(handle),
  runScreening: (resume_id, job_id) =>
    fetch(`${BASE_URL}/screening/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resume_id, job_id }),
    }).then(handle),
  listResultsForJob: (job_id, shortlistedOnly = false) =>
    fetch(`${BASE_URL}/screening/job/${job_id}?shortlisted_only=${shortlistedOnly}`).then(handle),
};
