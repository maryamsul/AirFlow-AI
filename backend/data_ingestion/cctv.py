from datetime import datetime, timedelta
import random

def get_cctv_data():
    """
    Simulate CCTV passenger counting data
    
    Returns:
        Dict with passenger count and timestamp
    """
    
    # Simulate passenger count based on time of day
    current_hour = datetime.now().hour
    
    # Base passenger count varies by time
    if 6 <= current_hour <= 9:  # Morning rush
        base_count = random.randint(400, 700)
    elif 16 <= current_hour <= 19:  # Evening rush
        base_count = random.randint(450, 750)
    elif 22 <= current_hour or current_hour <= 5:  # Night
        base_count = random.randint(50, 150)
    else:  # Regular hours
        base_count = random.randint(200, 400)
    
    return {
        "count": base_count,
        "timestamp": datetime.now().isoformat(),
        "source": "CCTV_SYSTEM",
        "camera_ids": ["CAM_001", "CAM_002", "CAM_003", "CAM_004"],
        "confidence": round(random.uniform(0.85, 0.98), 2)
    }

def get_historical_cctv_data(hours: int = 24):
    """
    Generate historical CCTV data for training/analysis
    
    Args:
        hours: Number of hours of historical data
    
    Returns:
        List of historical data points
    """
    historical_data = []
    
    for i in range(hours):
        timestamp = datetime.now() - timedelta(hours=hours - i)
        hour = timestamp.hour
        
        if 6 <= hour <= 9:
            count = random.randint(400, 700)
        elif 16 <= hour <= 19:
            count = random.randint(450, 750)
        elif 22 <= hour or hour <= 5:
            count = random.randint(50, 150)
        else:
            count = random.randint(200, 400)
        
        historical_data.append({
            "count": count,
            "timestamp": timestamp.isoformat()
        })
    
    return historical_data