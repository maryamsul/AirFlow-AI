import { useState } from "react";

export default function Analyze() {
  const [scenario, setScenario] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function analyze() {
    setLoading(true);

    const res = await fetch("http://localhost:8080/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        scenario: scenario
      })
    });

    const data = await res.json();

    // Gemini returns JSON string → parse it
    data.ai = JSON.parse(data.ai);

    setResult(data);
    setLoading(false);
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Airport Congestion Analyzer</h2>

      <textarea
        placeholder="Describe the scenario (eg: Festival rush, delayed flights...)"
        value={scenario}
        onChange={(e) => setScenario(e.target.value)}
        rows={4}
        style={{ width: "100%" }}
      />

      <button onClick={analyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {result && (
        <div style={{ marginTop: 20 }}>
          <h3>Risk Level: {result.ai.risk_level}</h3>

          <p><strong>Reason:</strong> {result.ai.reasoning}</p>

          <ul>
            {result.ai.actions.map((a, i) => (
              <li key={i}>{a}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
