import pandas as pd
from sklearn.ensemble import IsolationForest

print("ML Anomaly Detection Started")

# Load risk data
df = pd.read_csv("data/mplads_risk_results.csv")

# Select features for ML
features = [
    "Final Amount (₹)",
    "Project Count",
    "Pending Percentage"
]

X = df[features].fillna(0)

# Create ML model
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

# Train model
model.fit(X)

# Predict anomalies
df["ML Prediction"] = model.predict(X)

# -1 = anomaly, 1 = normal
df["ML Anomaly"] = df["ML Prediction"].apply(
    lambda x: "Potential Anomaly" if x == -1 else "Normal"
)

# Save ML results
df.to_csv(
    "data/mplads_ml_results.csv",
    index=False
)

# Show results
print("\nML Anomaly Results:")
print(df["ML Anomaly"].value_counts())

print("\nML Anomaly Detection Completed!")
print("Results saved to data/mplads_ml_results.csv")