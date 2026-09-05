# HIMALAYAN SENTINEL — SIH 2026 PS 192

An interactive, local-first command-centre prototype for the submitted **HIMALAYAN SENTINEL** concept: a distributed IoT and Edge-AI early-warning system for flash floods in hilly regions.

## Run it

```powershell
npm install
npm run dev
```

Open the local address printed by Vite. For release checks, run `npm test`, `npm run lint`, and `npm run build`.

## 2–3 minute demo story

1. Start at **Reset / Normal**. Explain that the GIS view uses simulated terrain, the mesh is healthy, and the risk engine is deterministic for a reliable demo.
2. Click **Rainfall escalation**. Show rain intensity, soil saturation, and risk contribution increasing.
3. Click **Upstream flood cascade**. Follow the event chain from Kedar upstream to the bridge and Ward 03. The map changes to an evacuation zone and the warning release becomes available.
4. Click **Node HS-02 outage**. Highlight that the bridge node is explicitly OFFLINE, mesh rerouting occurs, and confidence falls. The system never treats an offline node as flood evidence.
5. Return to **Reset / Normal**. This represents recovery and normal edge monitoring.

## Architecture represented

`telemetry inputs → validation / node health → feature aggregation → fused risk + confidence → severity → recommended action`

The UI models 3–5 heterogeneous ESP32/LoRa logical nodes, an edge layer, local buffering, a gateway, cross-node evidence fusion, and dashboard/alert delivery. It intentionally uses no credentials, live map service, hardware, or paid feed.

## Simulated data and limitations

Scenario fixtures supply rainfall rate, soil moisture, river-level trend, slope movement, historical susceptibility, and fusion confidence. `src/risk.ts` is a small, inspectable risk engine: weighted environmental factors are scaled by confidence, then mapped to Normal / Watch / Warning / Critical. This is **not** a calibrated hydrological or ML prediction model and must not be presented as validated accuracy.

To connect real deployment data, replace scenario fixtures with a standard telemetry ingestion adapter (node ID, timestamp, rainfall accumulations, soil moisture, water level/rise rate, temperature/pressure, tilt/vibration, battery, RSSI, local anomaly, node health). Keep health inference independent from hazard inference; an offline node is not flood evidence.

## Project structure

- `src/App.tsx` — responsive control-room demo and scenario controls
- `src/risk.ts` — modular, deterministic fusion engine
- `src/risk.test.ts` — risk escalation and confidence tests
- `src/styles.css` — local GIS-style visual system with no external map key

The application is intentionally a polished front-end prototype rather than an overbuilt distributed backend. A production rollout should calibrate thresholds by basin, validate models using time-aware data splits, add authenticated ingestion, persistence, GIS layers, alert delivery integration, and field-tested safety policy.
