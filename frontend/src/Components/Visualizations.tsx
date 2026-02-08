import { LineChart, Line, BarChart, Bar, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

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

interface VisualizationsProps {
  forecast: ForecastPoint[];
}

function Visualizations({ forecast }: VisualizationsProps) {
  // Format timestamp for display
  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: false 
    });
  };

  // Prepare data for charts
  const chartData = forecast.map(point => ({
    time: formatTime(point.timestamp),
    passengers: point.predicted_count,
    utilization: point.utilization_rate,
    lower: point.confidence_interval.lower,
    upper: point.confidence_interval.upper,
    risk: point.risk_level
  }));

  // Get risk level counts for distribution
  const riskDistribution = forecast.reduce((acc, point) => {
    acc[point.risk_level] = (acc[point.risk_level] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const riskData = Object.entries(riskDistribution).map(([level, count]) => ({
    level,
    count
  }));

  return (
    <div className="visualizations">
      <h3>Forecast Visualizations</h3>

      <div className="chart-container">
        <h4>Predicted Passenger Count (Next 6 Hours)</h4>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="time" 
              tick={{ fontSize: 12 }}
              interval="preserveStartEnd"
            />
            <YAxis />
            <Tooltip />
            <Legend />
            <Area 
              type="monotone" 
              dataKey="upper" 
              stackId="1"
              stroke="#93c5fd" 
              fill="#dbeafe" 
              name="Upper Bound"
            />
            <Area 
              type="monotone" 
              dataKey="passengers" 
              stackId="2"
              stroke="#3b82f6" 
              fill="#60a5fa" 
              name="Predicted Count"
            />
            <Area 
              type="monotone" 
              dataKey="lower" 
              stackId="3"
              stroke="#93c5fd" 
              fill="#dbeafe" 
              name="Lower Bound"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-container">
        <h4>Terminal Utilization Rate (%)</h4>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="time" 
              tick={{ fontSize: 12 }}
              interval="preserveStartEnd"
            />
            <YAxis domain={[0, 100]} />
            <Tooltip />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="utilization" 
              stroke="#8b5cf6" 
              strokeWidth={2}
              dot={{ fill: '#8b5cf6' }}
              name="Utilization %"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-container">
        <h4>Risk Level Distribution</h4>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={riskData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="level" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar 
              dataKey="count" 
              fill="#6c35ed" 
              name="Number of Periods"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="forecast-table">
        <h4>Detailed Forecast Data</h4>
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Time</th>
                <th>Predicted Count</th>
                <th>Utilization %</th>
                <th>Risk Level</th>
                <th>Confidence Range</th>
              </tr>
            </thead>
            <tbody>
              {forecast.slice(0, 12).map((point, idx) => (
                <tr key={idx}>
                  <td>{formatTime(point.timestamp)}</td>
                  <td>{point.predicted_count}</td>
                  <td>{point.utilization_rate.toFixed(1)}%</td>
                  <td>
                    <span className={`risk-badge ${point.risk_level.toLowerCase()}`}>
                      {point.risk_level}
                    </span>
                  </td>
                  <td>
                    {point.confidence_interval.lower} - {point.confidence_interval.upper}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Visualizations;