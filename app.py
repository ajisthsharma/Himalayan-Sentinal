from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd
from datetime import datetime
import os

app = FastAPI(title="Himalayan Sentinel - Inference Engine")

# Allow frontend to talk to backend
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

try:
    artifact = joblib.load('himalayan_sentinel_model.joblib')
    model = artifact['model']
    THRESHOLDS = artifact['alert_thresholds']
except Exception as e:
    model = None
    print(f"[!] Warning: Run train_flood_model.py first! ({e})")

class TelemetryPayload(BaseModel):
    node_id: str
    battery_v: float
    rssi: int
    rain_1h: float = 0.0
    rain_3h: float = 0.0
    rain_24h: float = 0.0
    soil_moisture: float = 0.0
    delta_soil_1h: float = 0.0
    water_level: float = 0.0
    water_rise_rate: float = 0.0
    water_rise_accel: float = 0.0
    upstream_anomaly_score: float = 0.0
    imu_tilt_deg: float = 0.0

NODE_REGISTRY = {}
DASHBOARD_STATE = {} # New: Stores the latest alerts for the frontend

def assess_node_health(payload: TelemetryPayload) -> str:
    if payload.battery_v < 3.3: return "BATTERY_CRITICAL"
    if payload.rssi < -115: return "LINK_MARGINAL"
    if payload.imu_tilt_deg > 25.0: return "PHYSICAL_DISPLACEMENT"
    return "HEALTHY"

@app.post("/api/v1/telemetry")
async def ingest_telemetry(data: TelemetryPayload):
    if model is None: raise HTTPException(status_code=500, detail="ML Model not loaded")
    
    health_status = assess_node_health(data)
    NODE_REGISTRY[data.node_id] = {'last_seen': datetime.utcnow(), 'health': health_status}
    
    df_in = pd.DataFrame({
        'rain_1h': [data.rain_1h], 'rain_3h': [data.rain_3h], 'rain_24h': [data.rain_24h],
        'soil_moisture': [data.soil_moisture], 'delta_soil_1h': [data.delta_soil_1h],
        'water_level': [data.water_level], 'water_rise_rate': [data.water_rise_rate],
        'water_rise_accel': [data.water_rise_accel], 'upstream_anomaly_score': [data.upstream_anomaly_score]
    })
    
    hazard_prob = float(model.predict_proba(df_in)[0, 1])
    
    # Fusion Rule Override
    if data.upstream_anomaly_score > 0.70 and data.water_rise_rate > 0.3:
        hazard_prob = max(hazard_prob, 0.72)
    
    if hazard_prob >= THRESHOLDS['CRITICAL']: alert = "CRITICAL"
    elif hazard_prob >= THRESHOLDS['WARNING']: alert = "WARNING"
    elif hazard_prob >= THRESHOLDS['WATCH']: alert = "WATCH"
    else: alert = "NORMAL"
        
    result = {
        "node_id": data.node_id,
        "health": health_status,
        "probability": round(hazard_prob, 4),
        "alert": alert,
        "timestamp": datetime.utcnow().strftime("%H:%M:%S")
    }
    
    # Save for frontend
    DASHBOARD_STATE[data.node_id] = result
    return result

# New endpoint for the frontend to fetch data
@app.get("/api/v1/dashboard")
async def get_dashboard():
    return DASHBOARD_STATE

# Serve the HTML UI on the root URL
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    if os.path.exists("index.html"):
        with open("index.html", "r") as f:
            return f.read()
    return "<h1>index.html not found! Please create it in the same folder.</h1>"