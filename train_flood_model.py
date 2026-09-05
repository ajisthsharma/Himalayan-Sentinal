import numpy as np
import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score, recall_score
from sklearn.calibration import CalibratedClassifierCV

def generate_synthetic_mountain_catchment_data(n_samples=20000, random_seed=42):
    """
    Generates synthetic dynamic catchment telemetry mimicking Himalayan flash flood triggers:
    1. Rainfall-runoff cascades
    2. Cryosphere / upstream surge triggers
    3. Benign rain vs dangerous saturation
    """
    np.random.seed(random_seed)
    
    # 1. Base meteorology
    rain_1h = np.random.exponential(scale=5.0, size=n_samples) # mm
    rain_3h = rain_1h * np.random.uniform(1.2, 2.8, size=n_samples)
    rain_24h = rain_3h * np.random.uniform(1.5, 4.0, size=n_samples)
    
    # 2. Catchment wetness
    soil_moisture = np.clip(np.random.beta(a=2, b=2, size=n_samples) * 100, 5, 98) # %
    delta_soil_1h = np.random.normal(loc=rain_1h * 0.4, scale=2.0)
    
    # 3. Stream dynamics
    water_level = np.clip(np.random.gamma(shape=2, scale=1.2, size=n_samples), 0.2, 12.0) # meters
    water_rise_rate = np.random.normal(loc=(rain_3h * 0.05 * (soil_moisture / 100)), scale=0.15) # m/hr
    water_rise_accel = np.random.normal(loc=water_rise_rate * 0.2, scale=0.08)
    
    # 4. Upstream / Cryosphere precursor (0 to 1 score)
    upstream_anomaly_score = np.clip(np.random.beta(a=0.5, b=5.0, size=n_samples), 0.0, 1.0)
    
    # 5. Physics-grounded hazard formulation (Ground Truth Definition)
    # A flood occurs when:
    # (A) Rapid water rise occurs on high base level, OR
    # (B) Extreme rain on saturated soil, OR
    # (C) Upstream surge (GLOF / rock-ice collapse) cascades downstream
    hazard_score = (
        (water_rise_rate > 0.8).astype(int) * 35 +
        (water_level > 4.5).astype(int) * 20 +
        ((rain_1h > 35) & (soil_moisture > 75)).astype(int) * 30 +
        ((upstream_anomaly_score > 0.75) & (water_rise_rate > 0.4)).astype(int) * 40 +
        np.random.normal(0, 5, size=n_samples)
    )
    
    y = (hazard_score > 40).astype(int)
    
    df = pd.DataFrame({
        'rain_1h': np.round(rain_1h, 2),
        'rain_3h': np.round(rain_3h, 2),
        'rain_24h': np.round(rain_24h, 2),
        'soil_moisture': np.round(soil_moisture, 2),
        'delta_soil_1h': np.round(delta_soil_1h, 2),
        'water_level': np.round(water_level, 2),
        'water_rise_rate': np.round(water_rise_rate, 3),
        'water_rise_accel': np.round(water_rise_accel, 3),
        'upstream_anomaly_score': np.round(upstream_anomaly_score, 2),
        'hazard_label': y
    })
    return df

def train_and_export_model():
    print("[+] Generating catchment training data...")
    data = generate_synthetic_mountain_catchment_data(n_samples=25000)
    
    features = [
        'rain_1h', 'rain_3h', 'rain_24h', 
        'soil_moisture', 'delta_soil_1h', 
        'water_level', 'water_rise_rate', 'water_rise_accel', 
        'upstream_anomaly_score'
    ]
    target = 'hazard_label'
    
    # Chronological / event-aware train-test split (80-20)
    split_idx = int(len(data) * 0.8)
    X_train, y_train = data[features].iloc[:split_idx], data[target].iloc[:split_idx]
    X_test, y_test = data[features].iloc[split_idx:], data[target].iloc[split_idx:]
    
    print(f"[+] Training dataset size: {len(X_train)}, Test size: {len(X_test)}")
    print(f"[+] Flood event balance in training: {y_train.mean():.2%}")
    
    base_xgb = XGBClassifier(
        n_estimators=150,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=3.0, # Heavily penalize false negatives (missed floods)
        random_state=42,
        eval_metric='logloss'
    )
    
    # Calibrated probability output
    calibrated_model = CalibratedClassifierCV(estimator=base_xgb, method='sigmoid', cv=3)
    calibrated_model.fit(X_train, y_train)
    
    # Evaluation
    preds_proba = calibrated_model.predict_proba(X_test)[:, 1]
    # Use alert threshold 0.40 to favor High Recall
    preds = (preds_proba >= 0.40).astype(int)
    
    print("\n--- Evaluation on Test Horizon ---")
    print(classification_report(y_test, preds))
    print(f"ROC-AUC Score: {roc_auc_score(y_test, preds_proba):.4f}")
    print(f"Hazard Event Recall (Sensitivity): {recall_score(y_test, preds):.4f}")
    
    # Save model and feature contract
    model_artifact = {
        'model': calibrated_model,
        'features': features,
        'alert_thresholds': {
            'WATCH': 0.35,
            'WARNING': 0.65,
            'CRITICAL': 0.85
        }
    }
    joblib.dump(model_artifact, 'himalayan_sentinel_model.joblib')
    print("[✓] Model artifact saved to himalayan_sentinel_model.joblib")

if __name__ == "__main__":
    train_and_export_model()