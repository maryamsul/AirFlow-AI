from datetime import datetime, timedelta
import random

def get_aodb_data():
    """
    Simulate Airport Operations Database (AODB) data - flight schedules
    
    Returns:
        Dict with flight information
    """
    
    current_hour = datetime.now().hour
    
    # Simulate flight activity based on time of day
    if 6 <= current_hour <= 10:  # Morning peak
        arriving = random.randint(15, 25)
        departing = random.randint(12, 20)
    elif 14 <= current_hour <= 18:  # Afternoon/Evening peak
        arriving = random.randint(18, 28)
        departing = random.randint(15, 25)
    elif 22 <= current_hour or current_hour <= 5:  # Night
        arriving = random.randint(2, 5)
        departing = random.randint(1, 4)
    else:
        arriving = random.randint(8, 15)
        departing = random.randint(6, 12)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "active_flights": arriving + departing,
        "arriving_flights": arriving,
        "departing_flights": departing,
        "delayed_flights": random.randint(0, 3),
        "cancelled_flights": random.randint(0, 1),
        "gates_occupied": random.randint(8, 24),
        "total_gates": 30,
        "source": "AODB_SYSTEM"
    }

def get_flight_schedule(hours_ahead: int = 6):
    """
    Get simulated flight schedule for upcoming hours
    
    Args:
        hours_ahead: Number of hours to look ahead
    
    Returns:
        List of scheduled flights
    """
    flights = []
    
    for i in range(hours_ahead * 2):  # 2 flights per hour average
        scheduled_time = datetime.now() + timedelta(minutes=30 * i)
        flight_type = random.choice(["arrival", "departure"])
        
        flight = {
            "flight_number": f"FL{random.randint(1000, 9999)}",
            "type": flight_type,
            "scheduled_time": scheduled_time.isoformat(),
            "gate": f"G{random.randint(1, 30)}",
            "status": random.choice(["on_time", "on_time", "on_time", "delayed"]),
            "passenger_capacity": random.randint(150, 350)
        }
        
        flights.append(flight)
    
    return flights