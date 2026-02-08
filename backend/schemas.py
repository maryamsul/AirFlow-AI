from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

class FlightSchedule(BaseModel):
    """Flight schedule information"""
    active_flights: int = Field(ge=0, description="Number of active flights")
    arriving_flights: int = Field(ge=0, description="Number of arriving flights")
    departing_flights: int = Field(ge=0, description="Number of departing flights")

class ManualDataInput(BaseModel):
    """Input model for manual data entry"""
    cctv_count: int = Field(ge=0, description="Current passenger count from CCTV")
    terminal_capacity: int = Field(gt=0, description="Maximum terminal capacity")
    flight_schedule: FlightSchedule
    timestamp: str = Field(description="ISO format timestamp")

class ConfidenceInterval(BaseModel):
    """Confidence interval for predictions"""
    lower: int
    upper: int

class ForecastPoint(BaseModel):
    """Single forecast data point"""
    timestamp: str
    predicted_count: int
    utilization_rate: float
    risk_level: str
    confidence_interval: ConfidenceInterval

class CurrentMetrics(BaseModel):
    """Current operational metrics"""
    cctv_count: int
    terminal_capacity: int
    utilization_rate: float
    timestamp: str
    active_flights: Optional[int] = None
    arriving_flights: Optional[int] = None
    departing_flights: Optional[int] = None

class ForecastResponse(BaseModel):
    """Complete analysis response"""
    current_metrics: CurrentMetrics
    forecast: List[ForecastPoint]
    gemini_insights: str
    risk_level: str
    recommendations: List[str]

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    gemini_configured: bool