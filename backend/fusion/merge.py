from typing import Dict, Any
from datetime import datetime

def merge_data(
    cctv_data: Dict[str, Any],
    aodb_data: Dict[str, Any],
    capacity_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Merge data from different sources into unified state snapshot
    
    Args:
        cctv_data: CCTV passenger count data
        aodb_data: Airport Operations Database (flight schedules)
        capacity_data: Terminal capacity information
    
    Returns:
        Dict: Unified operational state
    """
    
    merged = {
        "timestamp": cctv_data.get("timestamp", datetime.now().isoformat()),
        "cctv_count": cctv_data.get("count", 0),
        "terminal_capacity": capacity_data.get("terminal_capacity", 1000),
        "active_flights": aodb_data.get("active_flights", 0),
        "arriving_flights": aodb_data.get("arriving_flights", 0),
        "departing_flights": aodb_data.get("departing_flights", 0),
        "utilization_rate": 0.0,
        "congestion_level": "UNKNOWN"
    }
    
    # Calculate utilization rate
    if merged["terminal_capacity"] > 0:
        merged["utilization_rate"] = (
            merged["cctv_count"] / merged["terminal_capacity"]
        ) * 100
    
    # Determine congestion level
    util_rate = merged["utilization_rate"]
    if util_rate > 90:
        merged["congestion_level"] = "CRITICAL"
    elif util_rate > 75:
        merged["congestion_level"] = "HIGH"
    elif util_rate > 50:
        merged["congestion_level"] = "MEDIUM"
    else:
        merged["congestion_level"] = "LOW"
    
    # Add flight density score
    merged["flight_density"] = (
        merged["arriving_flights"] + merged["departing_flights"]
    ) / 2 if merged["terminal_capacity"] > 0 else 0
    
    return merged

def validate_merged_data(data: Dict[str, Any]) -> bool:
    """
    Validate merged data for completeness
    """
    required_fields = [
        "timestamp", 
        "cctv_count", 
        "terminal_capacity", 
        "utilization_rate"
    ]
    
    return all(field in data for field in required_fields)