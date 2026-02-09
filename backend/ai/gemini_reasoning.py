import os
import json
import time
from typing import Dict, List, Any
from google import genai
from datetime import datetime, timedelta

# Circuit Breaker Configuration
class CircuitBreaker:
    """
    Circuit Breaker pattern for Gemini API calls
    Prevents repeated calls to failing API and provides fast fallback
    """
    def __init__(self, failure_threshold=3, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout  # seconds before resetting
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED = normal, OPEN = circuit broken, HALF_OPEN = testing
    
    def call_failed(self):
        """Record a failed API call"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            print(f" Circuit breaker OPEN - API failures: {self.failure_count}")
    
    def call_succeeded(self):
        """Record a successful API call"""
        self.failure_count = 0
        self.state = "CLOSED"
        print(" Circuit breaker CLOSED - API recovered")
    
    def can_attempt(self):
        """Check if we should attempt an API call"""
        if self.state == "CLOSED":
            return True
        
        if self.state == "OPEN":
            # Check if timeout has passed
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
                print(" Circuit breaker HALF_OPEN - Testing API")
                return True
            return False
        
        # HALF_OPEN state - allow one attempt
        return True
    
    def get_state(self):
        return self.state

# Initialize Gemini client and circuit breaker
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=60)

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    client = None
    print("Warning: GEMINI_API_KEY not found in environment variables")

async def generate_gemini_insights(
    current_data: Dict[str, Any],
    forecast_data: List[Dict[str, Any]]
) -> str:
    """
    Generate AI-powered insights using Gemini 3 with Circuit Breaker pattern
    
    Strategy:
    1. If circuit is OPEN (API failing), immediately use fallback
    2. If circuit is CLOSED/HALF_OPEN, try Gemini 3 with thinking mode
    3. On 503 (overload) or repeated failures, open circuit and use fallback
    4. Fallback provides intelligent local analysis
    """
    
    # Check if we should even attempt the API call
    if not client or not circuit_breaker.can_attempt():
        print(f"🔌 Circuit breaker {circuit_breaker.get_state()} - Using local analysis")
        return generate_fallback_insights(current_data, forecast_data)
    
    try:
        utilization = (current_data.get('cctv_count', 0) / current_data.get('terminal_capacity', 1)) * 100
        
        prompt = f"""
You are an expert airport operations AI analyst with deep knowledge of passenger flow dynamics, security operations, and resource optimization.

CURRENT OPERATIONAL DATA:
- CCTV Passenger Count: {current_data.get('cctv_count', 'N/A')}
- Terminal Capacity: {current_data.get('terminal_capacity', 'N/A')}
- Utilization Rate: {utilization:.2f}%
- Active Flights: {current_data.get('active_flights', 'N/A')}
- Timestamp: {current_data.get('timestamp', 'N/A')}

FORECAST DATA (Next 6 hours):
{json.dumps(forecast_data, indent=2)}

ANALYSIS REQUIRED:
Provide a comprehensive operational analysis including:

1. **Situation Assessment** (2-3 sentences)
   - Current capacity status and trends
   - Immediate operational concerns
   
2. **Risk Analysis**
   - Primary risk factors based on current and forecasted data
   - Likelihood and impact assessment
   
3. **Peak Congestion Forecast**
   - Specific time windows when congestion will peak
   - Expected passenger volumes
   
4. **Operational Recommendations** (prioritized)
   - Immediate actions (next 30 minutes)
   - Short-term actions (next 2 hours)
   - Medium-term preparations (2-6 hours)
   
5. **Resource Allocation Strategy**
   - Staff deployment recommendations
   - Infrastructure optimization
   - Contingency protocols

Focus on actionable, specific recommendations that airport operations can implement immediately.
"""
        
        # Try Gemini 3 Flash with extended thinking for better insights
        print(" Calling Gemini 3 Flash Preview with deep reasoning...")
        
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=prompt,
            config={
                'temperature': 0.3,  # Lower temperature for more consistent operational advice
                'top_p': 0.95,
                'top_k': 40,
            }
        )
        
        if response and hasattr(response, 'text') and response.text:
            circuit_breaker.call_succeeded()
            print(" Gemini 3 analysis completed successfully")
            return response.text
        
        # No response text - treat as failure
        circuit_breaker.call_failed()
        return generate_fallback_insights(current_data, forecast_data)
    
    except Exception as e:
        error_msg = str(e)
        print(f" Gemini API Error: {error_msg}")
        
        # Check for specific error types
        if '503' in error_msg or 'UNAVAILABLE' in error_msg or 'overloaded' in error_msg.lower():
            print("  Google servers overloaded (503) - Opening circuit breaker")
            circuit_breaker.call_failed()
        elif '404' in error_msg or 'NOT_FOUND' in error_msg:
            print("  Model not available - Check API access for Gemini 3")
            circuit_breaker.call_failed()
        elif '429' in error_msg or 'RESOURCE_EXHAUSTED' in error_msg:
            print("  Rate limit exceeded - Opening circuit breaker")
            circuit_breaker.call_failed()
        else:
            # Generic error
            circuit_breaker.call_failed()
        
        return generate_fallback_insights(current_data, forecast_data)

def generate_fallback_insights(
    current_data: Dict[str, Any],
    forecast_data: List[Dict[str, Any]]
) -> str:
    """
    Generate intelligent local analysis when Gemini API is unavailable
    Uses rule-based expert system for airport operations
    """
    
    # Calculate key metrics
    cctv_count = current_data.get('cctv_count', 0)
    capacity = current_data.get('terminal_capacity', 1)
    utilization = (cctv_count / capacity) * 100
    active_flights = current_data.get('active_flights', 0)
    
    # Analyze forecast trend
    trend = analyze_congestion_trend(forecast_data)
    peak_periods = identify_peak_periods(forecast_data)
    
    # Determine risk level
    if utilization > 95:
        risk_level = "CRITICAL"
        risk_desc = "Terminal at maximum capacity - immediate intervention required"
    elif utilization > 85:
        risk_level = "SEVERE"
        risk_desc = "Terminal approaching capacity limits - proactive measures needed"
    elif utilization > 70:
        risk_level = "ELEVATED"
        risk_desc = "Terminal experiencing high volume - enhanced monitoring required"
    elif utilization > 50:
        risk_level = "MODERATE"
        risk_desc = "Terminal operating normally with moderate passenger flow"
    else:
        risk_level = "LOW"
        risk_desc = "Terminal operating well below capacity"
    
    # Build comprehensive analysis
    insights = f"""
═══════════════════════════════════════════════════════════════
 AIRPORT OPERATIONS ANALYSIS - LOCAL INTELLIGENCE MODE
═══════════════════════════════════════════════════════════════

 SITUATION ASSESSMENT
Current terminal utilization is at {utilization:.1f}% ({cctv_count:,} passengers / {capacity:,} capacity).
Based on ARIMA forecasting models and historical patterns, we anticipate a {trend} congestion trend over the next 6 hours.
{risk_desc}

!!! RISK ANALYSIS
Risk Level: {risk_level}
"""
    
    # Add specific risk factors
    risk_factors = []
    if utilization > 80:
        risk_factors.append(f"• Critical capacity utilization at {utilization:.1f}%")
    if trend == "increasing":
        risk_factors.append(f"• Upward trend forecasted - passenger volumes expected to rise")
    if len(peak_periods) > 0:
        risk_factors.append(f"• {len(peak_periods)} peak congestion periods identified in forecast window")
    if active_flights > 20:
        risk_factors.append(f"• High flight activity with {active_flights} active operations")
    
    if risk_factors:
        insights += "\n".join(risk_factors) + "\n"
    else:
        insights += "• No significant risk factors identified at current utilization levels\n"
    
    # Peak congestion forecast
    insights += "\n PEAK CONGESTION FORECAST\n"
    if peak_periods:
        for i, period in enumerate(peak_periods, 1):
            insights += f"{i}. {period}\n"
    else:
        insights += "• No significant peaks forecasted in the next 6 hours\n"
    
    # Operational recommendations (prioritized)
    insights += "\n OPERATIONAL RECOMMENDATIONS\n\n"
    
    # Immediate actions (next 30 minutes)
    insights += " IMMEDIATE ACTIONS (Next 30 minutes):\n"
    if utilization > 85:
        insights += "• Deploy all available security personnel to active checkpoints\n"
        insights += "• Activate emergency overflow processing lanes\n"
        insights += "• Initiate crowd control protocols at high-density zones\n"
    elif utilization > 70:
        insights += "• Position standby staff near peak-volume checkpoints\n"
        insights += "• Verify all processing lanes are operational\n"
    else:
        insights += "• Maintain standard operational posture\n"
        insights += "• Continue routine monitoring of passenger flow\n"
    
    # Short-term actions (next 2 hours)
    insights += "\n  SHORT-TERM ACTIONS (Next 2 hours):\n"
    if trend == "increasing" or utilization > 70:
        insights += "• Prepare additional staff for anticipated peak periods\n"
        insights += "• Pre-position mobile customer service units\n"
        insights += "• Brief airline partners on expected congestion\n"
    else:
        insights += "• Optimize staff rotation schedules\n"
        insights += "• Conduct routine equipment checks during low-volume windows\n"
    
    # Medium-term preparations (2-6 hours)
    insights += "\n MEDIUM-TERM PREPARATIONS (2-6 hours):\n"
    if peak_periods:
        insights += f"• Schedule reinforcement teams for peak windows: {', '.join(peak_periods[:2])}\n"
    insights += "• Coordinate with ground transportation providers\n"
    insights += "• Update digital signage with wait time estimates\n"
    insights += "• Ensure backup systems are ready for high-volume periods\n"
    
    # Resource allocation strategy
    insights += "\n RESOURCE ALLOCATION STRATEGY\n"
    
    if utilization > 85:
        insights += "• Security Personnel: Deploy 100% of available staff immediately\n"
        insights += "• Processing Lanes: All lanes must be operational\n"
        insights += "• Customer Service: Position roaming agents in congested areas\n"
        insights += "• Contingency: Activate overflow protocols and emergency procedures\n"
    elif utilization > 70:
        insights += "• Security Personnel: Increase to 85% staffing levels\n"
        insights += "• Processing Lanes: Open additional lanes proactively\n"
        insights += "• Customer Service: Enhanced presence at information desks\n"
        insights += "• Contingency: Standby teams on 15-minute alert\n"
    else:
        insights += "• Security Personnel: Maintain standard staffing (65-75%)\n"
        insights += "• Processing Lanes: Operate core lanes with flex capacity available\n"
        insights += "• Customer Service: Standard service level\n"
        insights += "• Contingency: Regular protocols in place\n"
    
    insights += f"""
═══════════════════════════════════════════════════════════════
 Analysis Mode: Local Intelligence (Rule-Based Expert System)
 Generated: {current_data.get('timestamp', 'N/A')}
 Forecast Window: 6 hours | Data Points: {len(forecast_data)}
═══════════════════════════════════════════════════════════════

Note: This analysis uses advanced rule-based algorithms and ARIMA forecasting.
For enhanced AI-powered insights with deep reasoning, Gemini 3 integration 
is available when API services are operational.
"""
    
    return insights.strip()

def analyze_congestion_trend(forecast_data: List[Dict[str, Any]]) -> str:
    """
    Analyze trend from forecast data with sophisticated logic
    """
    if not forecast_data or len(forecast_data) < 2:
        return "stable"
    
    # Use multiple data points for better trend analysis
    first_third = forecast_data[:len(forecast_data)//3] if len(forecast_data) >= 3 else [forecast_data[0]]
    last_third = forecast_data[-len(forecast_data)//3:] if len(forecast_data) >= 3 else [forecast_data[-1]]
    
    avg_early = sum(d.get('predicted_count', 0) for d in first_third) / len(first_third)
    avg_late = sum(d.get('predicted_count', 0) for d in last_third) / len(last_third)
    
    change_pct = ((avg_late - avg_early) / avg_early * 100) if avg_early > 0 else 0
    
    if change_pct > 15:
        return "increasing"
    elif change_pct < -15:
        return "decreasing"
    else:
        return "stable"

def identify_peak_periods(forecast_data: List[Dict[str, Any]]) -> List[str]:
    """
    Identify peak congestion periods from forecast with intelligent thresholds
    """
    peaks = []
    if not forecast_data:
        return peaks
    
    # Calculate dynamic threshold (1.3x average for better peak detection)
    avg_count = sum(d.get('predicted_count', 0) for d in forecast_data) / len(forecast_data)
    threshold = avg_count * 1.3
    
    for item in forecast_data:
        if item.get('predicted_count', 0) > threshold:
            peaks.append(item.get('timestamp', 'Unknown time'))
    
    return peaks[:3]  # Return top 3 peaks

def get_circuit_breaker_status() -> Dict[str, Any]:
    """
    Get current circuit breaker status for monitoring
    """
    return {
        "state": circuit_breaker.get_state(),
        "failure_count": circuit_breaker.failure_count,
        "last_failure_time": circuit_breaker.last_failure_time,
        "can_attempt": circuit_breaker.can_attempt()
    }
