# Group 3
# Advanced Bank Loan Creditworthiness Prediction

A team project focused on predicting whether a bank loan application will be **approved or rejected** using machine learning, rigorous evaluation, and a production-minded roadmap. The current source code implements a strong **baseline** using **Logistic Regression**, and this README describes how to elevate it into a best-in-class, portfolio-grade project.

---

## Team Members
- **Kian Akbari (Team Lead)**
- Mohammad ebrahimi
- Nima Rahnavard
- elika taheri
- User 4  
- Farbod Sedighi 

---

## Table of Contents
- [1) Project Overview](#1-project-overview)
- [2) Problem Statement & Objectives](#2-problem-statement--objectives)
- [3) Dataset](#3-dataset)
- [4) Approach & Pipeline](#4-approach--pipeline)
- [5) Models & Algorithms Used](#5-models--algorithms-used)
- [6) Evaluation & Metrics](#6-evaluation--metrics)
- [7) Challenges & Risks](#7-challenges--risks)
- [8) Advanced Roadmap (Making It Exceptional)](#8-advanced-roadmap-making-it-exceptional)
- [9) Setup & Running the Project](#9-setup--running-the-project)
- [10) Recommended Repository Structure](#10-recommended-repository-structure)
- [11) Team Workflow & Ownership](#11-team-workflow--ownership)


---

## 1) Project Overview

Banks must make fast, defensible decisions about loan approvals while controlling default risk. This project builds a **creditworthiness prediction model** to estimate the probability of loan approval (or rejection) from applicant features such as income, credit history, employment status, and property area.

The output can be used as:
- a **binary decision** (approve/reject), or
- a **probability score** for decision support and risk-based thresholds.

---

## 2) Problem Statement & Objectives

**Task type:** Binary classification  
**Target:** `Loan_Status` (Approved = Y / Rejected = N)

Primary objectives:
- Deliver a reliable and reproducible baseline (currently: Logistic Regression)
- Build a clean data pipeline (preprocessing → training → evaluation) with leakage prevention
- Upgrade to advanced tabular ML models with hyperparameter tuning and explainability
- Address real-world risks: missing data, class imbalance, fairness, and governance

---

## 3) Dataset

Dataset file: `loan.csv`

Key columns (typical schema):
- `Loan_ID` (identifier; removed from modeling)
- `Gender`, `Married`, `Dependents`, `Education`, `Self_Employed`, `Property_Area` (categorical)
- `ApplicantIncome`, `CoapplicantIncome`, `LoanAmount`, `Loan_Amount_Term`, `Credit_History` (numeric/ordinal)
- `Loan_Status` (label)

---

## 4) Approach & Pipeline

### 4.1 Exploratory Data Analysis (EDA)
The current notebook includes:
- dtype inspection
- basic frequency plots (e.g., `Gender`)
- correlation matrix + heatmap

### 4.2 Preprocessing (Current Baseline)
Implemented in the current code:
- Drop `Loan_ID`
- Encode categorical columns using **Label Encoding**:
  - `Gender`, `Married`, `Education`, `Self_Employed`, `Property_Area`, `Loan_Status`
- Fill missing values using **mean imputation**

Important note:
- Label Encoding on **nominal** categories can introduce artificial ordering. The advanced version should migrate to **One-Hot Encoding** (or model-native encoders like CatBoost).

### 4.3 Train/Test Split & Training
- `train_test_split(test_size=0.2, random_state=42)`
- Model: `LogisticRegression(max_iter=10000)`

---

## 5) Models & Algorithms Used

### 5.1 Algorithms Used in the Current Source (Baseline)
- Label Encoding (categorical encoding)
- Mean Imputation (missing values)
- Logistic Regression (classification)
- Train/Test Split (holdout evaluation)
- Primary metric: Accuracy

### 5.2 AI Model Used
The AI/ML model used in the current source code is:
- **Logistic Regression (scikit-learn)**

Why it matters:
- It is fast, strong for baselines, interpretable, and provides calibrated probability outputs after proper calibration.

---

## 6) Evaluation & Metrics

In a reproducible baseline run (with `random_state=42`), accuracy is typically observed in the **~80–85%** range depending on preprocessing and data splits.

To make evaluation professional-grade, add:
- Confusion Matrix
- Precision / Recall / F1-score
- ROC-AUC
- PR-AUC (especially if the classes are imbalanced)
- Probability Calibration (Brier score / calibration curves)
- Threshold tuning based on business costs:
  - False Positive cost (approving risky loans)
  - False Negative cost (rejecting good applicants)

---

## 7) Challenges & Risks

Common real-world issues in credit modeling (some already appear in the current implementation):
1. **Missing values** in important fields (e.g., `LoanAmount`, `Credit_History`)
2. **Categorical encoding choices** can distort patterns and reduce generalization
3. **Class imbalance** can make Accuracy misleading
4. **Data leakage** if preprocessing is performed outside a strict Pipeline
5. **Explainability requirements** in financial decision systems
6. **Fairness / bias risk** for sensitive attributes (e.g., gender)

---

## 8) Advanced Roadmap (Making It Exceptional)

This is where the project becomes “portfolio-level” instead of “just a notebook”.

### 8.1 Data Quality & Feature Engineering
- Replace mean imputation with:
  - Median/Most-frequent
  - KNNImputer
  - IterativeImputer (where appropriate)
- Use **ColumnTransformer + Pipeline** end-to-end (prevents leakage)
- Use **One-Hot Encoding** for nominal categories
- Feature engineering ideas:
  - `TotalIncome = ApplicantIncome + CoapplicantIncome`
  - Debt-to-income proxy (e.g., `LoanAmount / TotalIncome`)
  - Binning for linear models (income bands, loan amount bands)
- Outlier handling:
  - RobustScaler, clipping/winsorization, or model-robust methods

### 8.2 Strong Tabular Models to Compare
- Random Forest
- Gradient Boosting:
  - XGBoost / LightGBM / CatBoost (best-in-class for tabular)
- SVM (with scaling and careful tuning)
- MLP (simple neural network for tabular baselines)
- Ensembles:
  - Stacking / blending (with leakage-safe cross-validation)

### 8.3 Hyperparameter Tuning & Validation
- Stratified K-Fold cross-validation
- RandomizedSearchCV / Optuna
- Select models by ROC-AUC / PR-AUC rather than Accuracy alone

### 8.4 Explainability & Reporting
- SHAP for global + local explanations
- Permutation Importance
- Partial Dependence / ICE plots
- Produce an HTML/PDF report summarizing:
  - model choice, metrics, plots, feature importance, fairness checks

### 8.5 Production Readiness (MLOps)
- Serialize the model (`joblib`)
- Serve predictions with FastAPI:
  - `/predict`
  - `/health`
- Dockerize the service (Dockerfile + docker-compose)
- Unit tests (pytest) + CI (GitHub Actions)
- Monitor data quality and drift (advanced)

### 8.6 Fairness & Compliance
- Evaluate fairness metrics across groups (e.g., Gender)
- Consider excluding sensitive attributes if required by policy
- Create a **Model Card** documenting:
  - data, intended use, limitations, risks, monitoring plan

---

## 9) Setup & Running the Project

### 9.1 Requirements
- Python 3.10+ recommended
- Core libraries:
  - pandas, numpy
  - scikit-learn
  - matplotlib, seaborn

### 9.2 Install dependencies
```bash
pip install -r requirements.txt
```

If you do not have a `requirements.txt`, install:
```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

### 9.3 Run the advanced pipeline (recommended)
This repository includes an upgraded, leakage-safe training pipeline:

- Notebook: `advanced_loan.ipynb`
- Script: `advanced_loan_pipeline.py`

Run the script:
```bash
python advanced_loan_pipeline.py --data loan.csv --out models/loan_model.joblib
```

Then you can open and run the advanced notebook:
```bash
jupyter notebook advanced_loan.ipynb
```

### 9.3 Run the baseline notebook
1) Ensure `loan.csv` is available.  
2) Launch Jupyter:
```bash
jupyter notebook
```
3) Run all cells to obtain the baseline accuracy and plots.

---

## 10) Recommended Repository Structure

To evolve into a professional-grade ML project:

```
.
├── data/
│   ├── raw/loan.csv
│   └── processed/
├── notebooks/
│   └── baseline.ipynb
├── src/
│   ├── data_prep.py
│   ├── features.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
├── models/
│   └── model.joblib
├── reports/
│   ├── figures/
│   └── model_report.html
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 11) Team Workflow & Ownership

Recommended ownership model (parallel work without conflicts):
1. **Data/EDA Owner:** data cleaning, EDA, feature engineering, data documentation  
2. **Modeling Owner:** baseline + advanced models, tuning, model selection  
3. **MLOps Owner:** pipelines, packaging, serialization, API, Docker, CI  
4. **Explainability/Reporting Owner:** SHAP, fairness checks, report + model card  
5. **Project Management & QA (Team Lead):** integration, code review standards, final validation, presentation package  

---
