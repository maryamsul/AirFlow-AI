import random

def get_capacity_data():
    """
    Get terminal capacity information
    
    Returns:
        Dict with capacity metrics
    """
    
    # Simulate terminal capacity data
    terminal_capacity = 1000  # Base capacity
    
    # Simulate varying operational capacity based on factors
    operational_capacity = terminal_capacity * random.uniform(0.85, 1.0)
    
    return {
        "terminal_capacity": int(terminal_capacity),
        "operational_capacity": int(operational_capacity),
        "security_lanes_active": random.randint(8, 12),
        "security_lanes_total": 12,
        "check_in_counters_active": random.randint(15, 25),
        "check_in_counters_total": 30,
        "waiting_areas": {
            "departure_lounge": 500,
            "arrival_hall": 300,
            "security_queue": 200
        },
        "accessibility_status": "normal",
        "maintenance_areas": random.randint(0, 2)
    }

def get_capacity_constraints():
    """
    Get current capacity constraints and limitations
    
    Returns:
        Dict with constraint information
    """
    
    constraints = {
        "max_hourly_throughput": 850,
        "security_bottleneck": random.choice([True, False]),
        "check_in_bottleneck": random.choice([True, False]),
        "parking_availability": random.randint(60, 95),  # percentage
        "current_restrictions": []
    }
    
    # Add random restrictions
    possible_restrictions = [
        "Gate maintenance in progress",
        "Security lane temporarily closed",
        "Baggage system running at reduced capacity"
    ]
    
    if random.random() > 0.7:
        constraints["current_restrictions"].append(
            random.choice(possible_restrictions)
        )
    
    return constraints