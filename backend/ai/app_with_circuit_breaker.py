# Example FastAPI Integration with Circuit Breaker Pattern
# Add this to your app.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from gemini_insights import generate_gemini_insights, get_circuit_breaker_status
import asyncio

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint with circuit breaker status"""
    cb_status = get_circuit_breaker_status()
    return {
        "status": "healthy",
        "circuit_breaker": cb_status,
        "api_available": cb_status["state"] == "CLOSED"
    }

@app.post("/analyze")
async def analyze_airport_data(request: dict):
    """
    Analyze airport operations with intelligent fallback
    
    The circuit breaker ensures:
    - Fast response even when Gemini API is down
    - No waiting for timeout on failed API calls
    - Automatic recovery testing
    """
    try:
        current_data = request.get('current_data', {})
        forecast_data = request.get('forecast_data', [])
        
        # Get insights with circuit breaker protection
        insights = await generate_gemini_insights(current_data, forecast_data)
        
        cb_status = get_circuit_breaker_status()
        
        return {
            "status": "success",
            "insights": insights,
            "circuit_breaker": {
                "state": cb_status["state"],
                "using_fallback": cb_status["state"] != "CLOSED"
            },
            "timestamp": current_data.get('timestamp')
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/circuit-breaker/status")
async def circuit_breaker_status():
    """Monitor circuit breaker status"""
    status = get_circuit_breaker_status()
    
    return {
        "state": status["state"],
        "failure_count": status["failure_count"],
        "last_failure": status["last_failure_time"],
        "can_attempt_api": status["can_attempt"],
        "description": {
            "CLOSED": "API working normally - using Gemini 3",
            "OPEN": "API failed - using local intelligence",
            "HALF_OPEN": "Testing API recovery"
        }.get(status["state"], "Unknown state")
    }

@app.post("/circuit-breaker/reset")
async def reset_circuit_breaker():
    """Manually reset circuit breaker (admin endpoint)"""
    from gemini_insights import circuit_breaker
    
    circuit_breaker.failure_count = 0
    circuit_breaker.state = "CLOSED"
    circuit_breaker.last_failure_time = None
    
    return {
        "status": "Circuit breaker manually reset",
        "new_state": "CLOSED"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
