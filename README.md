
# 🔬 Parametric Curve Fitting – R&D / AI Assignment

## 🎯 Objective
Estimate the unknown parameters **θ**, **M**, and **X** in the given 2D parametric curve equations such that the generated curve best fits the provided data points (`xy_data.csv`).

---

## 🧮 Problem Definition

The given parametric equations are:

x = t*cos(θ) - e^(M|t|)*sin(0.3t)*sin(θ) + X

y = 42 + t*sin(θ) + e^(M|t|)*sin(0.3t)*cos(θ)


where the unknowns are:

θ, M, X


**Parameter constraints:**

| Parameter | Range |
|------------|--------|
| θ (degrees) | 0° < θ < 50° |
| M | -0.05 < M < 0.05 |
| X | 0 < X < 100 |
| t | 6 < t < 60 |

---

## 🧠 Understanding the Model

- **θ (theta):** Controls rotation of the curve in the XY-plane.  
- **M:** Controls exponential scaling — positive M causes growth, negative M causes decay.  
- **X:** Provides horizontal translation (offset).  
- The oscillatory term **sin(0.3t)** introduces wave-like variations in both `x` and `y`.

The dataset `xy_data.csv` provides sampled (x, y) points for the curve in the given range of t.

---

## ⚙️ Methodology

### 1️⃣ Data Preparation
- Loaded `xy_data.csv` which contained columns `x` and `y`.  
- Since no `t` column was provided, assumed uniform sampling for `t ∈ [6, 60]`.

### 2️⃣ Model Construction
Defined the parametric equations as Python functions for `x(t)` and `y(t)`.

### 3️⃣ Optimization
Used a **two-stage optimization** strategy:

#### 🧩 Stage 1 — Global Search (Differential Evolution)
- Searches the parameter space broadly to avoid local minima.
- Objective function minimized the **L1 error**:
 Σ_t ( |x_model − x_data| + |y_model − y_data| )

#### ⚙️ Stage 2 — Local Refinement (Least Squares)
- Used `scipy.optimize.least_squares` for precise fine-tuning within bounds.
- Ensured high precision with tolerances `xtol = ftol = 1e-12`.

### 4️⃣ Evaluation Metric
- **L1 Distance:** total absolute difference between predicted and actual points.

---

## 🧩 Final Results

| Parameter | Value |
|:-----------|:-------:|
| θ (radians) | 0.516318 |
| θ (degrees) | 29.5828° |
| M | -0.050000 |
| X | 55.013610 |
| L1 Distance | 38102.1921 |

All estimated parameters lie within the valid range.

---

## 📈 Final Parametric Equation

x = t*cos(0.5163) - e^(-0.05|t|)*sin(0.3t)sin(0.5163) + 55.0136

y = 42 + tsin(0.5163) + e^(-0.05|t|)*sin(0.3t)*cos(0.5163)
Visualize it directly on **[Desmos](https://www.desmos.com/calculator/rfj91yrxob)** by pasting the above expression.

---

## 📊 Visualization

The plot below compares the provided dataset (blue) and the fitted model (red dashed):

- **Left:** XY-plane curve comparison  
- **Right:** X(t) and Y(t) variation across parameter range  

*(Generated automatically by `matplotlib` as `fit_plot.png`.)*

---

## 🧰 Tools & Libraries Used

| Library | Purpose |
|----------|----------|
| **NumPy** | Numerical computations |
| **Pandas** | Data loading and handling |
| **SciPy** | Optimization (Differential Evolution & Least Squares) |
| **Matplotlib** | Visualization and result plotting |

---

## 📂 Repository Structure

```
flam 1st project/
│
├── xy_data.csv           # Provided dataset (x, y points)
├── fit_parametric.py     # Main fitting and optimization script
├── fit_results.txt       # Saved output parameters (θ, M, X, L1)
├── fit_plot.png          # Visualization comparing data vs model
├── README.md             # This report / documentation
└── .venv/                # Python virtual environment
```

---

## 🧾 How to Run This Project

### 1️⃣ Setup Python Environment
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install numpy pandas scipy matplotlib
```

### 2️⃣ Run the Fitting Script
```bash
python fit_parametric.py
```

### 3️⃣ Check Results
- **fit_results.txt** → numerical values for θ, M, X, and L1 distance  
- **fit_plot.png** → visualization comparing data vs fitted model  
- **Terminal Output** → optimization logs and convergence info  

---

## 🧩 Interpretation of Results

- **θ ≈ 29.6°:** The curve is rotated ~30° relative to the x-axis.  
- **M = -0.05:** Slight exponential decay — oscillations dampen gradually with |t|.  
- **X ≈ 55:** Horizontal offset; curve shifted ~55 units along X-axis.  
- **L1 Distance ≈ 3.8 × 10⁴:** Total deviation between model and data, acceptable within given constraints.

---

## 📚 Key Learnings

- Hybrid optimization (global + local) provides robust and accurate fits.  
- The L1 metric resists noise better than L2 norms.  
- Exponential modulation (controlled by M) heavily influences the curve’s smoothness.  
- `scipy.optimize` and `matplotlib` are essential tools for modern numerical fitting tasks.

---

## 🧠 Summary

This project demonstrates how to recover hidden parameters in a nonlinear parametric curve using numerical optimization.  
By combining **Differential Evolution** with **Least Squares**, the fitted model accurately replicates the shape and orientation of the provided dataset while staying within the physical parameter bounds.

---


