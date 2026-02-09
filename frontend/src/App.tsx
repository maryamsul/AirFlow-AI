import { useState, useEffect } from 'react';
import Visualizations from './Components/Visualizations';
import './App.css';

interface CurrentMetrics {
  cctv_count: number;
  terminal_capacity: number;
  utilization_rate: number;
  timestamp: string;
}

interface ForecastPoint {
  timestamp: string;
  predicted_count: number;
  utilization_rate: number;
  risk_level: string;
  confidence_interval: {
    lower: number;
    upper: number;
  };
}

interface AnalysisData {
  current_metrics: CurrentMetrics;
  forecast: ForecastPoint[];
  gemini_insights: string;
  risk_level: string;
  recommendations: string[];
}

interface ManualInput {
  cctv_count: string;
  terminal_capacity: string;
  active_flights: string;
  arriving_flights: string;
  departing_flights: string;
}

function App() {
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [apiHealth, setApiHealth] = useState<boolean>(false);
  const [useManualInput, setUseManualInput] = useState(true);
  
  const [manualInput, setManualInput] = useState<ManualInput>({
    cctv_count: '450',
    terminal_capacity: '1000',
    active_flights: '25',
    arriving_flights: '15',
    departing_flights: '10'
  });

  // Check API health on mount
  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      const response = await fetch('https://airflow-ai-b.onrender.com/health');
      const data = await response.json();
      setApiHealth(data.status === 'healthy');
    } catch (err) {
      setApiHealth(false);
      console.error('API health check failed:', err);
    }
  };

  const handleManualAnalysis = async () => {
    setLoading(true);
    setError(null);

    try {
      const requestData = {
        cctv_count: parseInt(manualInput.cctv_count),
        terminal_capacity: parseInt(manualInput.terminal_capacity),
        flight_schedule: {
          active_flights: parseInt(manualInput.active_flights),
          arriving_flights: parseInt(manualInput.arriving_flights),
          departing_flights: parseInt(manualInput.departing_flights)
        },
        timestamp: new Date().toISOString()
      };

      const response = await fetch('https://airflow-ai-b.onrender.com/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      setAnalysisData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSimulatedAnalysis = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('https://airflow-ai-b.onrender.com/simulate');
      
      if (!response.ok) {
        throw new Error('Simulation failed');
      }

      const data = await response.json();
      setAnalysisData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Simulation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: keyof ManualInput, value: string) => {
    setManualInput(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'CRITICAL': return '#ef4444';
      case 'HIGH': return '#f97316';
      case 'MEDIUM': return '#eab308';
      case 'LOW': return '#22c55e';
      default: return '#6b7280';
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1> Airport Congestion Prediction System</h1>
        <p>Real-time forecasting powered by AI and ARIMA models</p>
        <div className="api-status">
          <span className={`status-indicator ${apiHealth ? 'online' : 'offline'}`}></span>
          <span>Backend: {apiHealth ? 'Connected' : 'Disconnected'}</span>
        </div>
      </header>

      <div className="control-panel">
        <div className="input-mode-toggle">
          <button
            className={useManualInput ? 'active' : ''}
            onClick={() => setUseManualInput(true)}
          >
            Manual Input
          </button>
          <button
            className={!useManualInput ? 'active' : ''}
            onClick={() => setUseManualInput(false)}
          >
            Simulated Data
          </button>
        </div>

        {useManualInput ? (
          <div className="manual-input-section">
            <h3> Enter Operational Data</h3>
            <div className="input-grid">
              <div className="input-field">
                <label>CCTV Passenger Count</label>
                <input
                  type="number"
                  value={manualInput.cctv_count}
                  onChange={(e) => handleInputChange('cctv_count', e.target.value)}
                  placeholder="e.g., 450"
                />
              </div>
              <div className="input-field">
                <label>Terminal Capacity</label>
                <input
                  type="number"
                  value={manualInput.terminal_capacity}
                  onChange={(e) => handleInputChange('terminal_capacity', e.target.value)}
                  placeholder="e.g., 1000"
                />
              </div>
              <div className="input-field">
                <label>Active Flights</label>
                <input
                  type="number"
                  value={manualInput.active_flights}
                  onChange={(e) => handleInputChange('active_flights', e.target.value)}
                  placeholder="e.g., 25"
                />
              </div>
              <div className="input-field">
                <label>Arriving Flights</label>
                <input
                  type="number"
                  value={manualInput.arriving_flights}
                  onChange={(e) => handleInputChange('arriving_flights', e.target.value)}
                  placeholder="e.g., 15"
                />
              </div>
              <div className="input-field">
                <label>Departing Flights</label>
                <input
                  type="number"
                  value={manualInput.departing_flights}
                  onChange={(e) => handleInputChange('departing_flights', e.target.value)}
                  placeholder="e.g., 10"
                />
              </div>
            </div>
            <button
              className="analyze-button"
              onClick={handleManualAnalysis}
              disabled={loading || !apiHealth}
            >
              {loading ? ' Analyzing...' : ' Analyze Congestion'}
            </button>
          </div>
        ) : (
          <div className="simulated-section">
            <p>Using simulated real-time data from CCTV, AODB, and capacity systems</p>
            <button
              className="analyze-button"
              onClick={handleSimulatedAnalysis}
              disabled={loading || !apiHealth}
            >
              {loading ? ' Generating...' : ' Run Simulation'}
            </button>
          </div>
        )}

        {error && (
          <div className="error-message">
             {error}
          </div>
        )}
      </div>

      {analysisData && (
        <div className="results-container">
          <div className="metrics-overview">
            <div className="metric-card">
              <h4>Current Passengers</h4>
              <div className="metric-value">{analysisData.current_metrics.cctv_count}</div>
            </div>
            <div className="metric-card">
              <h4>Terminal Capacity</h4>
              <div className="metric-value">{analysisData.current_metrics.terminal_capacity}</div>
            </div>
            <div className="metric-card">
              <h4>Utilization Rate</h4>
              <div className="metric-value">{analysisData.current_metrics.utilization_rate.toFixed(1)}%</div>
            </div>
            <div className="metric-card" style={{ borderColor: getRiskColor(analysisData.risk_level) }}>
              <h4>Risk Level</h4>
              <div className="metric-value" style={{ color: getRiskColor(analysisData.risk_level) }}>
                {analysisData.risk_level}
              </div>
            </div>
          </div>

          <div className="gemini-insights">
            <h3> Gemini AI Analysis</h3>
            <div className="insights-content">
              {analysisData.gemini_insights.split('\n').map((line, idx) => (
                <p key={idx}>{line}</p>
              ))}
            </div>
          </div>

          <div className="recommendations">
            <h3>Recommendations</h3>
            <ul>
              {analysisData.recommendations.map((rec, idx) => (
                <li key={idx}>{rec}</li>
              ))}
            </ul>
          </div>

          <Visualizations forecast={analysisData.forecast} />
        </div>
      )}

      {!analysisData && !loading && (
        <div className="placeholder">
          <p> Enter data and click "Analyze" to see forecasts and AI insights</p>
        </div>
      )}
    </div>
  );
}

export default App;
