import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_endpoint():
    """Test health check works"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_analyze_endpoint():
    """Test analysis with valid data"""
    data = {
        "cctv_count": 450,
        "terminal_capacity": 1000,
        "flight_schedule": {
            "active_flights": 25,
            "arriving_flights": 15,
            "departing_flights": 10
        },
        "timestamp": "2024-02-05T10:30:00Z"
    }
    response = client.post("/analyze", json=data)
    assert response.status_code == 200
    result = response.json()
    assert "gemini_insights" in result
    assert "forecast" in result
    assert len(result["forecast"]) > 0
@pytest.mark.asyncio

async def test_gemini_integration():
    """Test Gemini 3 is actually being used"""
    from ai.gemini_reasoning import generate_gemini_insights
    
    test_data = {"cctv_count": 500, "terminal_capacity": 1000}
    test_forecast = [{"predicted_count": 520, "timestamp": "2024-01-01T10:00:00"}]
    
    insights = await generate_gemini_insights(test_data, test_forecast)
    
    assert isinstance(insights, str)
    assert len(insights) > 50  # Real AI response, not fallback
    assert "risk" in insights.lower() or "congestion" in insights.lower()