export default function ResultsTable({ results }) {
  if (!results.length) {
    return <p className="muted">No screening results yet. Run screening above to see candidates here.</p>;
  }

  return (
    <table className="results-table">
      <thead>
        <tr>
          <th>Candidate</th>
          <th>Score</th>
          <th>Shortlisted</th>
          <th>Matched Skills</th>
          <th>Missing Skills</th>
          <th>Justification</th>
        </tr>
      </thead>
      <tbody>
        {results.map((r) => (
          <tr key={r.id} className={r.shortlisted ? "shortlisted-row" : ""}>
            <td>{r.candidate_name}</td>
            <td className="score-cell">{r.match_score.toFixed(1)}/10</td>
            <td>{r.shortlisted ? "✅ Yes" : "—"}</td>
            <td>{r.matched_skills.join(", ") || "—"}</td>
            <td>{r.missing_skills.join(", ") || "—"}</td>
            <td className="justification-cell">{r.justification}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
