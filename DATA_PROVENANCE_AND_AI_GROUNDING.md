Data Provenance & AI Grounding
AODB-Aligned Digital Twin for Airport Operations
Project Intent

This project demonstrates a credible, explainable airport decision-support system by modeling its data structures, thresholds, and AI reasoning after real-world airport operational standards.

Although numeric values are simulated for hackathon purposes, the logic, schemas, and operational constraints are grounded in how real airports operate.

### 1. Data Provenance (Source of Truth)
Industry Standard Alignment

The system’s data model is based on the Airport Operational Database (AODB) standard, which is used by airports globally to manage:

1. Flight schedules and status

2. Passenger flow and congestion

3. Gate, terminal, and resource allocation

4. Event-driven operational updates

Even when data values are synthetic, the format, relationships, and decision flows match real airport systems.

##### Key Standards Referenced
AODB (Airport Operational Database)
IATA Level of Service (LoS C)
FAA / TSA operational constraints
LAWA historical traffic baselines (October reference period)
Synthetic data is used only where live airport feeds are unavailable.
Operational logic remains industry-accurate.

### 2. Use Case: Operational Estimation (Why AI Is Needed) 
##### Problem
Airport operators must estimate near-future conditions, not just observe current ones:
1. Passenger congestion
   
2. Terminal capacity breaches

3. Arrival-induced surges

Safety and security risks

##### Solution

This system uses real-world aviation performance patterns to:
Estimate passenger flow 15–30 minutes ahead
Detect when a normal rush becomes a safety risk
Recommend mitigation actions before thresholds are breached

##### 3. Digital Twin Scenario 
LAX Terminal 6 — “Holiday Surge” Simulation
Objective
Validate the AI’s ability to distinguish between:
A normal peak rush
A capacity-driven safety breach
using realistic LAX operational baselines.

3.1 Simulated Input Data (Grounded in Reality)
Field	Value	Real-World Mapping
CCTV Passenger Count	1,550	Exceeds T6 mean hourly flow
Terminal Capacity	1,500	IATA LoS C calculation
Active Departures	12	Peak morning wave
Arriving Flights	4	Includes NAS-delayed inbound
3.2 Expected AI Reasoning Path

**Step 1 — Trend Analysis**

Passenger flow shows a +15% increase over 15 minutes
Forecast projects ~1,700+ passengers in 20 minutes

**Step 2 — Capacity Comparison**
1,700 projected vs. 1,500 capacity
Utilization exceeds 113%

**Step 3 — Context Awareness**

NAS delay indicates inbound congestion is external
Bottleneck is arrival-driven, not terminal processing

**Step 4 — Operational Recommendation**

Initiate arrival gate-hold to prevent terminal overflow
Prioritizes safety without violating FAA/TSA rules
This mirrors how real airport operations centers reason under pressure.

**4. Risk Threshold Mapping (Proof of Accuracy)**
UI Risk Level	Real-World Interpretation (LAX T6)
Low Risk	< 1,260 passengers (average flow)
High Risk	1,261–1,500 passengers (approaching limit)
Critical	> 1,500 passengers (IATA safety breach)

These thresholds are not arbitrary — they are mapped to real operational limits.

**5. AI Prompt Grounding (Reasoning Engine)**
Master System Constraint
The AI is not allowed to “freestyle.”
It is grounded with explicit operational rules:
You are the Lead Terminal Operations Decision-Support AI for LAX Airport.

**Inputs include:**
- Passenger volume from CCTV
- Terminal capacity based on IATA LoS C
- Short-term flow trends (ARIMA-style)
- Flight activity and NAS delay context

**Decision Priority:**
1. Life Safety
2. Security & Sterile Area Integrity
3. Operational Efficiency

Rules:
- If utilization exceeds 100%, prioritize crowd safety.
- Do not recommend actions that violate FAA or TSA policy.
- Base recommendations on calibrated LAX Terminal 6 baselines.

**6. Structured Input Protocol**

When a user clicks Analyze, GEMINI receives a deterministic payload:

{
  "terminal": "LAX_T6",
  "current_passengers": 1550,
  "terminal_capacity": 1500,
  "trend_15min": "+15%",
  "active_departures": 12,
  "arriving_flights": 4,
  "nas_delay_indicator": true
}


This mirrors AODB-style event ingestion used in real airport systems.

**7. Validation Methodology**

To prevent hallucination, GEMINI is validated using few-shot operational scenarios:

Scenario	Passenger Volume	Expected Outcome
Normal Operations	~1,100 PAX	Maintain flow
Peak Rush	~1,450 PAX	Open auxiliary lanes
Safety Breach	>1,500 PAX	Level 4 mitigation

