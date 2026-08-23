function bandColor(score) {
  if (score >= 7) return "var(--signal-high)";
  if (score >= 4) return "var(--signal-mid)";
  return "var(--signal-low)";
}

export default function SignalMeter({ score }) {
  const pct = Math.max(0, Math.min(100, (score / 10) * 100));
  const color = bandColor(score);

  return (
    <div className="signal-meter" role="img" aria-label={`Match score ${score.toFixed(1)} out of 10`}>
      <div className="track">
        <div className="fill" style={{ width: `${pct}%`, background: color }} />
        <div className="ticks">
          {Array.from({ length: 9 }).map((_, i) => (
            <span key={i} />
          ))}
        </div>
      </div>
      <span className="readout" style={{ color }}>
        {score.toFixed(1)}/10
      </span>
    </div>
  );
}
