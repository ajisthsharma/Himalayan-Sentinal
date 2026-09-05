# Himalayan Sentinel

A proof-of-concept flash-flood early-warning dashboard for Himalayan catchments. The FastAPI service receives sensor telemetry, evaluates node health, and combines an XGBoost hazard probability with an upstream-surge override. A browser dashboard displays current node alerts, and a simulator demonstrates a four-stage flood event.

## Components

- `app.py` — FastAPI inference API and live dashboard host.
- `train_flood_model.py` — generates synthetic catchment data and exports the model artifact.
- `simulate_mesh.py` — emits telemetry for four simulated field nodes.
- `index.html` — polling dashboard UI.

## Run locally

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python train_flood_model.py
uvicorn app:app --reload
```

In a second terminal, run:

```powershell
python simulate_mesh.py
```

Open `http://127.0.0.1:8000` to view the dashboard. The generated `himalayan_sentinel_model.joblib` is intentionally not versioned; regenerate it with the training script.
