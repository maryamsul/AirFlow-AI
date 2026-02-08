import { useEffect, useState } from 'react';

interface ForecastPoint {
  timestamp: string;
  predicted_count: number;
  utilization_rate: number;
  risk_level: string;
}

interface HeatmapProps {
  forecast: ForecastPoint[];
  terminalCapacity: number;
}

export function CongestionHeatmap({ forecast, terminalCapacity }: HeatmapProps) {
  const [animatedCells, setAnimatedCells] = useState<Set<string>>(new Set());

  // Generate time labels from forecast data
  const getTimeLabel = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { 
      hour: 'numeric',
      hour12: true 
    });
  };

  // Get first 12 forecast points (3 hours with 15-min intervals)
  const timeSlots = forecast.slice(0, 12).map(f => getTimeLabel(f.timestamp));
  
  // Terminal zones
  const zones = [
    { name: 'Security Checkpoints', multiplier: 1.2 },
    { name: 'Check-in Counters', multiplier: 0.9 },
    { name: 'Departure Gates', multiplier: 1.0 },
    { name: 'Arrival Hall', multiplier: 0.7 },
    { name: 'Baggage Claim', multiplier: 0.8 }
  ];

  // Calculate zone-specific congestion
  const getZoneCongestion = (baseUtilization: number, zoneMultiplier: number) => {
    const adjusted = baseUtilization * zoneMultiplier;
    return Math.min(100, Math.max(0, adjusted));
  };

  // Color based on utilization
  const getColor = (utilization: number) => {
    if (utilization > 90) return '#ef4444'; // Red - Critical
    if (utilization > 75) return '#f97316'; // Orange - High
    if (utilization > 50) return '#eab308'; // Yellow - Medium
    if (utilization > 25) return '#84cc16'; // Light Green
    return '#22c55e'; // Green - Low
  };

  // Get emoji for critical levels
  const getEmoji = (utilization: number) => {
    if (utilization > 95) return '🔥';
    if (utilization > 90) return '⚠️';
    if (utilization > 80) return '📈';
    return '';
  };

  // Animation effect on mount
  useEffect(() => {
    const cells = new Set<string>();
    zones.forEach((zone, zoneIdx) => {
      timeSlots.forEach((_, timeIdx) => {
        setTimeout(() => {
          cells.add(`${zoneIdx}-${timeIdx}`);
          setAnimatedCells(new Set(cells));
        }, (zoneIdx * timeSlots.length + timeIdx) * 30);
      });
    });
  }, [forecast]);

  return (
    <div className="heatmap-visualization">
      <div className="heatmap-header">
        <h4>🗺️ Real-Time Congestion Heatmap</h4>
        <p className="heatmap-subtitle">Next 3 hours - 15-minute intervals</p>
      </div>

      <div className="heatmap-container">
        <div className="heatmap-grid">
          {/* Header row with time labels */}
          <div className="heatmap-row header-row">
            <div className="zone-label-cell header-cell">Terminal Zones</div>
            {timeSlots.map((time, idx) => (
              <div key={idx} className="time-label-cell header-cell">
                {time}
              </div>
            ))}
          </div>

          {/* Zone rows */}
          {zones.map((zone, zoneIdx) => (
            <div key={zone.name} className="heatmap-row">
              <div className="zone-label-cell">
                <span className="zone-name">{zone.name}</span>
              </div>
              {forecast.slice(0, 12).map((point, timeIdx) => {
                const zoneCongestion = getZoneCongestion(
                  point.utilization_rate, 
                  zone.multiplier
                );
                const cellKey = `${zoneIdx}-${timeIdx}`;
                const isAnimated = animatedCells.has(cellKey);

                return (
                  <div
                    key={timeIdx}
                    className={`heatmap-cell ${isAnimated ? 'animated' : ''}`}
                    style={{ 
                      backgroundColor: getColor(zoneCongestion),
                      opacity: isAnimated ? 1 : 0
                    }}
                    title={`${zone.name} at ${timeSlots[timeIdx]}\n${zoneCongestion.toFixed(1)}% capacity\nRisk: ${point.risk_level}`}
                  >
                    <span className="cell-value">{zoneCongestion.toFixed(0)}%</span>
                    <span className="cell-emoji">{getEmoji(zoneCongestion)}</span>
                  </div>
                );
              })}
            </div>
          ))}
        </div>

        {/* Legend */}
        <div className="heatmap-legend">
          <h5>Legend:</h5>
          <div className="legend-items">
            <div className="legend-item">
              <div className="legend-color" style={{ backgroundColor: '#22c55e' }}></div>
              <span>0-25% Low</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{ backgroundColor: '#84cc16' }}></div>
              <span>25-50% Normal</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{ backgroundColor: '#eab308' }}></div>
              <span>50-75% Medium</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{ backgroundColor: '#f97316' }}></div>
              <span>75-90% High</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{ backgroundColor: '#ef4444' }}></div>
              <span>90%+ Critical</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}