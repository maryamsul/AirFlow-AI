def forecast_congestion(merged_state):
    """
    Lightweight ARIMA-like forecast
    (Deterministic for hackathon stability)
    """
    current_load = merged_state["load_ratio"]
    inbound_pressure = merged_state["inbound_flights"] * 0.03

    predicted = min(current_load + inbound_pressure, 1.0)

    return {
        "predicted_load_15min": round(predicted, 2),
        "trend": "increasing" if predicted > current_load else "stable"
    }
