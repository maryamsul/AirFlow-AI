from typing import Dict, List, Any
from datetime import datetime, timedelta
import numpy as np

def forecast_congestion(current_data: Dict[str, Any], hours: int = 6) -> List[Dict[str, Any]]:
    """
    Generate ARIMA-based congestion forecast
    
    Args:
        current_data: Current operational state
        hours: Number of hours to forecast
    
    Returns:
        List of forecasted data points
    """
    
    base_count = current_data.get("cctv_count", 100)
    capacity = current_data.get("terminal_capacity", 1000)
    current_time = datetime.fromisoformat(current_data.get("timestamp", datetime.now().isoformat()))
    
    # Simulate ARIMA forecast with realistic patterns
    forecast_points = []
    
    for i in range(hours * 4):  # 15-minute intervals
        time_offset = timedelta(minutes=15 * i)
        forecast_time = current_time + time_offset
        
        # Simulate daily patterns (peak hours: 6-9 AM, 4-7 PM)
        hour = forecast_time.hour
        
        # Base trend with noise
        trend_factor = 1.0
        if 6 <= hour <= 9:  # Morning peak
            trend_factor = 1.3 + np.random.normal(0, 0.1)
        elif 16 <= hour <= 19:  # Evening peak
            trend_factor = 1.4 + np.random.normal(0, 0.1)
        elif 22 <= hour or hour <= 5:  # Night low
            trend_factor = 0.5 + np.random.normal(0, 0.05)
        else:
            trend_factor = 1.0 + np.random.normal(0, 0.08)
        
        # Calculate predicted count with constraints
        predicted_count = int(base_count * trend_factor)
        predicted_count = max(0, min(predicted_count, capacity))
        
        # Calculate utilization
        utilization = (predicted_count / capacity) * 100 if capacity > 0 else 0
        
        # Determine risk level
        if utilization > 90:
            risk = "CRITICAL"
        elif utilization > 75:
            risk = "HIGH"
        elif utilization > 50:
            risk = "MEDIUM"
        else:
            risk = "LOW"
        
        forecast_points.append({
            "timestamp": forecast_time.isoformat(),
            "predicted_count": predicted_count,
            "utilization_rate": round(utilization, 2),
            "risk_level": risk,
            "confidence_interval": {
                "lower": max(0, predicted_count - int(predicted_count * 0.15)),
                "upper": min(capacity, predicted_count + int(predicted_count * 0.15))
            }
        })
    
    return forecast_points

def calculate_trend(forecast_data: List[Dict[str, Any]]) -> str:
    """
    Calculate overall trend from forecast data
    """
    if len(forecast_data) < 2:
        return "stable"
    
    first_val = forecast_data[0]["predicted_count"]
    last_val = forecast_data[-1]["predicted_count"]
    
    change = ((last_val - first_val) / first_val * 100) if first_val > 0 else 0
    
    if change > 15:
        return "increasing"
    elif change < -15:
        return "decreasing"
    else:
        return "stable"