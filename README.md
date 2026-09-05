# Himalayan Sentinel — SIH 2026 PS 192

Himalayan Sentinel is an early-warning-system prototype for flash floods in hilly regions. This repository includes both a local-first Vite/TypeScript command-centre UI and a Python/FastAPI telemetry-inference service with a reproducible XGBoost model and mesh simulator.

## Frontend prototype

```powershell
npm install
npm run dev
```

Run `npm test`, `npm run lint`, and `npm run build` for release checks. The deterministic risk demo is implemented in `src/risk.ts`; its scenario UI is in `src/App.tsx`.

## FastAPI telemetry service

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python train_flood_model.py
uvicorn app:app --reload
```

In another terminal, run `python simulate_mesh.py`. Open `http://127.0.0.1:8000` for the Python service's live dashboard.

## Components

- `src/` — command-centre frontend and deterministic risk-engine prototype.
- `app.py` — FastAPI telemetry ingestion, node-health assessment, and ML inference API.
- `train_flood_model.py` — synthetic catchment-data generation and model training.
- `simulate_mesh.py` — four-node flood-event telemetry simulation.
- `dashboard.html` — live dashboard served by the FastAPI application.

The `himalayan_sentinel_model.joblib` artifact is intentionally unversioned; regenerate it using the training script. This is a proof of concept and not a validated hydrological forecasting system.
