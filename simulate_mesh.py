import requests
import time
import random
from datetime import datetime

# FastAPI Backend URL
API_URL = "http://127.0.0.1:8000/api/v1/telemetry"

# Base telemetry profiles for each node type
NODES = {
    "N1_CRYOSPHERE": {"battery_v": 4.1, "rssi": -85, "water_level": 0, "soil_moisture": 0},
    "N2_SLOPE":      {"battery_v": 3.9, "rssi": -70, "water_level": 0, "upstream_anomaly_score": 0},
    "N3_RIVER":      {"battery_v": 4.0, "rssi": -65, "soil_moisture": 0, "upstream_anomaly_score": 0},
    "N4_DOWNSTREAM": {"battery_v": 4.2, "rssi": -60, "soil_moisture": 0, "upstream_anomaly_score": 0}
}

def generate_payload(node_id, phase):
    """Generates hydrologically realistic telemetry based on the disaster phase."""
    base = NODES[node_id]
    
    payload = {
        "node_id": node_id,
        "timestamp": datetime.utcnow().isoformat(),
        "battery_v": base["battery_v"] - random.uniform(0.0, 0.05),
        "rssi": base["rssi"] + random.randint(-5, 5),
        "rain_1h": 0.0,
        "rain_3h": 0.0,
        "rain_24h": 0.0,
        "soil_moisture": base.get("soil_moisture", 0.0),
        "delta_soil_1h": 0.0,
        "water_level": base.get("water_level", 0.5),
        "water_rise_rate": 0.0,
        "water_rise_accel": 0.0,
        "upstream_anomaly_score": base.get("upstream_anomaly_score", 0.0),
        "imu_tilt_deg": random.uniform(0.0, 1.5)
    }

    # PHASE 1: Normal Operations
    if phase == "NORMAL":
        if node_id == "N2_SLOPE":
            payload["soil_moisture"] = random.uniform(30.0, 40.0)
        if node_id in ["N3_RIVER", "N4_DOWNSTREAM"]:
            payload["water_level"] = random.uniform(1.0, 1.2)

    # PHASE 2: Heavy Catchment Rain (Soil saturates, river hasn't spiked yet)
    elif phase == "HEAVY_RAIN":
        if node_id == "N2_SLOPE":
            payload["rain_1h"] = random.uniform(25.0, 35.0)
            payload["rain_3h"] = payload["rain_1h"] + 15.0
            payload["soil_moisture"] = random.uniform(75.0, 85.0)
            payload["delta_soil_1h"] = random.uniform(15.0, 20.0)
        if node_id in ["N3_RIVER", "N4_DOWNSTREAM"]:
            payload["water_level"] = random.uniform(1.3, 1.6)
            payload["water_rise_rate"] = random.uniform(0.1, 0.2)

    # PHASE 3: Upstream Surge & River Spike (The Flash Flood)
    elif phase == "UPSTREAM_SURGE":
        if node_id == "N1_CRYOSPHERE":
            payload["upstream_anomaly_score"] = random.uniform(0.75, 0.95)
            payload["imu_tilt_deg"] = random.uniform(5.0, 8.0) # Ground rumble
        if node_id == "N2_SLOPE":
            payload["soil_moisture"] = random.uniform(90.0, 98.0) # Saturated
        if node_id == "N3_RIVER":
            payload["water_level"] = random.uniform(4.0, 5.5)
            payload["water_rise_rate"] = random.uniform(1.2, 2.0)
            payload["water_rise_accel"] = random.uniform(0.4, 0.8)

    # PHASE 4: Downstream Impact & N2 Battery Failure
    elif phase == "DOWNSTREAM_IMPACT_AND_FAILURE":
        if node_id == "N2_SLOPE":
            # Simulate a dead battery / washed out node
            payload["battery_v"] = random.uniform(2.8, 3.1) 
            payload["rssi"] = -120
            payload["imu_tilt_deg"] = random.uniform(30.0, 45.0) # Node knocked over
        if node_id == "N4_DOWNSTREAM":
            payload["water_level"] = random.uniform(5.0, 6.5)
            payload["water_rise_rate"] = random.uniform(1.5, 2.5)

    return payload

def run_simulation():
    timeline = [
        ("NORMAL", 5),                         # 5 ticks of normal weather
        ("HEAVY_RAIN", 5),                     # 5 ticks of storm buildup
        ("UPSTREAM_SURGE", 5),                 # 5 ticks of flash flood cascade
        ("DOWNSTREAM_IMPACT_AND_FAILURE", 5)   # 5 ticks of downstream hit and node loss
    ]

    print("=== Starting Himalayan Sentinel Multi-Node Simulation ===")
    
    for phase, ticks in timeline:
        print(f"\n---> ENTERING PHASE: {phase} <---")
        for tick in range(ticks):
            for node_id in NODES.keys():
                payload = generate_payload(node_id, phase)
                
                try:
                    response = requests.post(API_URL, json=payload, timeout=2)
                    result = response.json()
                    
                    # FIXED KEYS HERE
                    alert = result.get('alert', 'UNKNOWN')
                    health = result.get('health', 'UNKNOWN')
                    prob = result.get('probability', 0.0)
                    
                    color = '\033[92m' if alert == "NORMAL" else '\033[93m' if alert == "WATCH" else '\033[91m'
                    reset = '\033[0m'
                    
                    print(f"[{node_id}] Health: {health} | Risk: {prob:.2f} | Alert: {color}{alert}{reset}")
                
                except requests.exceptions.RequestException as e:
                    print(f"[!] Connection failed for {node_id}. Is the FastAPI server running?")
            
            time.sleep(1.5) # Wait between network pulses

if __name__ == "__main__":
    run_simulation()