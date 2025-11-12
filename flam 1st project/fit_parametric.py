import os
import numpy as np
import pandas as pd
from scipy.optimize import least_squares, differential_evolution
import matplotlib.pyplot as plt

# Load your CSV file
DATA_PATH = "xy_data.csv"

df = pd.read_csv(DATA_PATH)
print("Loaded data columns:", df.columns)

# Detect t automatically
if 't' in df.columns:
    t = df['t'].values
    x_data = df['x'].values
    y_data = df['y'].values
elif len(df.columns) >= 3:
    cols = df.columns
    t = df[cols[0]].values
    x_data = df[cols[1]].values
    y_data = df[cols[2]].values
else:
    cols = df.columns
    x_data = df[cols[0]].values
    y_data = df[cols[1]].values
    t = np.linspace(6, 60, len(x_data))
    print("No 't' column found — assuming uniform t in [6, 60].")

# Define model
def model(params, t):
    theta, M, X = params
    exp_term = np.exp(M * np.abs(t))
    x = t * np.cos(theta) - exp_term * np.sin(0.3 * t) * np.sin(theta) + X
    y = 42 + t * np.sin(theta) + exp_term * np.sin(0.3 * t) * np.cos(theta)
    return x, y

# Define error function
def residuals(params, t, x_data, y_data):
    x_model, y_model = model(params, t)
    return np.concatenate([x_model - x_data, y_model - y_data])

# Global optimization bounds
bounds = [
    (np.deg2rad(0.0001), np.deg2rad(50.0)),  # theta in radians
    (-0.05, 0.05),                            # M
    (0.0, 100.0)                              # X
]

def obj_func(p):
    x_m, y_m = model(p, t)
    return np.sum(np.abs(x_m - x_data) + np.abs(y_m - y_data))

print("Running global optimization (this may take 1–2 minutes)...")
de_result = differential_evolution(obj_func, bounds, maxiter=50, popsize=15, tol=1e-6)
print("Global optimization result:", de_result.x)

# Local refinement
print("Running local least-squares refinement...")
ls_result = least_squares(
    residuals, de_result.x,
    bounds=([b[0] for b in bounds], [b[1] for b in bounds]),
    args=(t, x_data, y_data),
    verbose=1, xtol=1e-12, ftol=1e-12
)

theta, M, X = ls_result.x
theta_deg = np.rad2deg(theta)
print("\n=== Final Fitted Parameters ===")
print(f"θ = {theta:.6f} rad = {theta_deg:.4f}°")
print(f"M = {M:.6f}")
print(f"X = {X:.6f}")

x_pred, y_pred = model(ls_result.x, t)
L1_distance = np.sum(np.abs(x_pred - x_data) + np.abs(y_pred - y_data))
print(f"L1 Distance = {L1_distance:.6f}")

# Save results
with open("fit_results.txt", "w") as f:
    f.write(f"theta_rad,{theta}\n")
    f.write(f"theta_deg,{theta_deg}\n")
    f.write(f"M,{M}\n")
    f.write(f"X,{X}\n")
    f.write(f"L1,{L1_distance}\n")
print("Saved results to fit_results.txt")

# Plot
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.scatter(x_data, y_data, s=10, label="data")
plt.plot(x_pred, y_pred, "r--", label="model")
plt.legend()
plt.title("XY plane")

plt.subplot(1, 2, 2)
plt.plot(t, x_data, label="x_data")
plt.plot(t, x_pred, "--", label="x_model")
plt.plot(t, y_data, label="y_data")
plt.plot(t, y_pred, "--", label="y_model")
plt.legend()
plt.title("X,Y vs t")
plt.tight_layout()
plt.savefig("fit_plot.png")
plt.show()
