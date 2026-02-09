from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

from data_ingestion.cctv import get_cctv_data
from data_ingestion.aodb import get_aodb_data
from data_ingestion.capacity import get_capacity_data
from fusion.merge import merge_data
from forecasting.arima import forecast_congestion
from ai.gemini_reasoning import generate_gemini_insights

load_dotenv()

app = FastAPI(title="Airport Congestion Prediction API")
origins = [
    "https://airflow-ai.onrender.com",
    "http://localhost:5173",
    "http://localhost:3000",
]
# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ManualDataInput(BaseModel):
    cctv_count: int
    terminal_capacity: int
    flight_schedule: Dict[str, Any]
    timestamp: str

class ForecastResponse(BaseModel):
    current_metrics: Dict[str, Any]
    forecast: List[Dict[str, Any]]
    gemini_insights: str
    risk_level: str
    recommendations: List[str]

@app.get("/")
async def root():
    return {"message": "Airport Congestion Prediction API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "gemini_configured": bool(os.getenv("GEMINI_API_KEY"))}

@app.post("/analyze", response_model=ForecastResponse)
async def analyze_congestion(data: ManualDataInput):
    """
    Main endpoint to analyze congestion with manual data input
    """
    try:
        # Step 1: Process manual input data
        cctv_data = {"count": data.cctv_count, "timestamp": data.timestamp}
        aodb_data = data.flight_schedule
        capacity_data = {"terminal_capacity": data.terminal_capacity}

        # Step 2: Merge data
        merged_data = merge_data(cctv_data, aodb_data, capacity_data)

        # Step 3: Generate forecast
        forecast_result = forecast_congestion(merged_data)

        # Step 4: Get Gemini AI insights
        gemini_insights = await generate_gemini_insights(merged_data, forecast_result)

        # Step 5: Calculate risk level
        risk_level = calculate_risk_level(merged_data, forecast_result)

        # Step 6: Generate recommendations
        recommendations = generate_recommendations(risk_level, forecast_result)

        return ForecastResponse(
            current_metrics={
                "cctv_count": data.cctv_count,
                "terminal_capacity": data.terminal_capacity,
                "utilization_rate": (data.cctv_count / data.terminal_capacity) * 100,
                "timestamp": data.timestamp
            },
            forecast=forecast_result,
            gemini_insights=gemini_insights,
            risk_level=risk_level,
            recommendations=recommendations
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/simulate")
async def get_simulated_data():
    """
    Endpoint to get simulated data for demo purposes
    """
    try:
        # Simulate data collection
        cctv_data = get_cctv_data()
        aodb_data = get_aodb_data()
        capacity_data = get_capacity_data()

        # Merge
        merged_data = merge_data(cctv_data, aodb_data, capacity_data)

        # Forecast
        forecast_result = forecast_congestion(merged_data)

        # Gemini insights
        gemini_insights = await generate_gemini_insights(merged_data, forecast_result)

        risk_level = calculate_risk_level(merged_data, forecast_result)
        recommendations = generate_recommendations(risk_level, forecast_result)

        return ForecastResponse(
            current_metrics=merged_data,
            forecast=forecast_result,
            gemini_insights=gemini_insights,
            risk_level=risk_level,
            recommendations=recommendations
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def calculate_risk_level(current_data: Dict, forecast: List[Dict]) -> str:
    """Calculate risk level based on current and forecasted data"""
    utilization = (current_data.get("cctv_count", 0) /
                   current_data.get("terminal_capacity", 1)) * 100

    if utilization > 90:
        return "CRITICAL"
    elif utilization > 75:
        return "HIGH"
    elif utilization > 50:
        return "MEDIUM"
    else:
        return "LOW"

def generate_recommendations(risk_level: str, forecast: List[Dict]) -> List[str]:
    """Generate actionable recommendations based on risk level"""
    recommendations = []

    if risk_level == "CRITICAL":
        recommendations.extend([
            "Immediately activate overflow protocols",
            "Deploy additional security personnel",
            "Consider flight gate reassignments",
            "Implement crowd control measures"
        ])
    elif risk_level == "HIGH":
        recommendations.extend([
            "Alert staff to prepare for increased passenger flow",
            "Monitor queues closely at security checkpoints",
            "Prepare backup resources"
        ])
    elif risk_level == "MEDIUM":
        recommendations.extend([
            "Continue standard monitoring procedures",
            "Be prepared to scale up resources if needed"
        ])
    else:
        recommendations.append("Normal operations - continue monitoring")

    return recommendations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
