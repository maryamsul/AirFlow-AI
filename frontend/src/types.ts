export interface CurrentMetrics {
  cctv_count: number;
  terminal_capacity: number;
  utilization_rate: number;
  timestamp: string;
  active_flights?: number;
  arriving_flights?: number;
  departing_flights?: number;
}

export interface ConfidenceInterval {
  lower: number;
  upper: number;
}

export interface ForecastPoint {
  timestamp: string;
  predicted_count: number;
  utilization_rate: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  confidence_interval: ConfidenceInterval;
}

export interface AnalysisResponse {
  current_metrics: CurrentMetrics;
  forecast: ForecastPoint[];
  gemini_insights: string;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  recommendations: string[];
}

export interface ManualDataInput {
  cctv_count: number;
  terminal_capacity: number;
  flight_schedule: {
    active_flights: number;
    arriving_flights: number;
    departing_flights: number;
  };
  timestamp: string;
}

export interface ApiHealthResponse {
  status: string;
  gemini_configured: boolean;
}