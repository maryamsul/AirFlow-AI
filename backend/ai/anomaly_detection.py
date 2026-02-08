# backend/ai/anomaly_detection.py

async def detect_anomalies_with_gemini(current_data, historical_pattern):
    """Use Gemini to detect unusual patterns"""
    
    prompt = f"""
    You are an airport operations expert. Analyze if this situation is anomalous:
    
    Current situation: {current_data}
    Normal pattern for this time: {historical_pattern}
    
    Is this anomalous? Why? What could cause it?
    Rate urgency 1-10.
    """
    
    response = model.generate_content(prompt)
    
    # Add to alerts
    if "anomalous" in response.text.lower():
        return {
            "is_anomaly": True,
            "explanation": response.text,
            "urgency": extract_urgency(response.text)
        }