import SignalMeter from "./SignalMeter";

export default function CandidateLeaderboard({ results }) {
  if (!results.length) {
    return (
      <div className="empty-state">
        No candidates screened yet. Select a resume and job description above, then run a match.
      </div>
    );
  }

  const sorted = [...results].sort((a, b) => b.match_score - a.match_score);

  return (
    <div className="leaderboard">
      {sorted.map((r) => (
        <div key={r.id} className={`candidate-row ${r.shortlisted ? "is-shortlisted" : ""}`}>
          <div className="candidate-name-row">
            {r.candidate_name}
            {r.shortlisted && <span className="badge">Shortlisted</span>}
          </div>
          <SignalMeter score={r.match_score} />

          {(r.matched_skills.length > 0 || r.missing_skills.length > 0) && (
            <div className="chip-row">
              {r.matched_skills.map((s) => (
                <span className="chip matched" key={`m-${s}`}>
                  {s}
                </span>
              ))}
              {r.missing_skills.map((s) => (
                <span className="chip missing" key={`x-${s}`}>
                  {s}
                </span>
              ))}
            </div>
          )}

          <div className="justification">{r.justification}</div>
        </div>
      ))}
    </div>
  );
}
