# Patient Length of Stay (LoS) Prediction

**Team:** Ben Lantz, Julian Ong, Katherine Schwind, Deepesh Verma, Jake Wellington
**Advisor:** Alexandria Wheeler

---

## Table of Contents

1. [Introduction](#introduction)
2. [Dataset & Data Pipeline](#dataset--data-pipeline)
3. [Exploratory Data Analysis](#exploratory-data-analysis)
4. [Modeling Approach](#modeling-approach)
5. [Results](#results)
6. [Future Work](#future-work)
7. [Description of Repository](#description-of-repository)
8. [How to Run the Models](#run-models)
---

## Introduction

In 2024, there were 35.6 million hospital admissions in the United States (AHA), with an average length of stay (LoS) of 6 days (OECD). Prolonged LoS negatively affects both patients and hospital staff, leading to avoidable health complications and increased stress respectively. The ability to accurately predict LoS could enable more effective resource planning and enhanced operational efficiency, improving inpatient outcomes while relieving pressure on healthcare workers.

The goal of this project is to develop a predictive model to determine LoS using **only admission-level data**, enabling better resource allocation and patient care before a patient's hospital course even begins.

### Stakeholders & KPIs

Our primary stakeholders — patients, hospital systems and administrators, and clinical teams — each have distinct but overlapping interests in LoS prediction:

- **Patients** benefit from more transparent care timelines and reduced risk of complications tied to prolonged stays.
- **Hospital administrators** require actionable predictions to optimize staffing, bed allocation, and discharge planning.
- **Clinical teams** need reliable estimates to effectively coordinate patient care.

Models were evaluated using **Root Mean Squared Error (RMSE)**, **Mean Absolute Error (MAE)**, **Huber Loss**, and **Quantile Loss**. 

We find it useful to briefly explain Quantile Loss in the context of our project. Quantile Loss penalizes over- and under-predictions asymmetrically, making it particularly well-suited for the right-skewed LoS distribution where a small number of patients have very long stays. By tuning the quantile parameter for prolonged stays (LoS>=30 days), the model can be trained conservatively — predicting slightly longer stays — which is preferable in a clinical context where under-allocating resources carries greater risk than over-allocating them.

A model was considered clinically and operationally viable only if it achieved meaningful improvement relative to the baseline across all four metrics.

---

## Dataset & Data Pipeline

### Data Access

The dataset was obtained from the **Texas Department of State Health Services (DSHS)** public data portal. It consists of over **7 million hospitalizations** from Texas spanning **2017–2019**, with more than 160 features per record. 

Data is available from **2010-2025**, but due to accessibility constraints and differences overtime in the features reported, we chose only to focus on **2017-2019**. Because the data is publicly accessible, it is included in a compressed form in this repository under `data/`.

### Feature Selection

To reflect a realistic prediction scenario — where a model must generate a LoS estimate at the moment of admission — we restricted the feature set strictly to **admission-only variables**: patient demographics, facility and location information, and diagnosis codes present at admission. Features that are only observable during or after a hospital stay were excluded.

### ICD-10 Code Handling

Raw ICD-10 diagnosis codes were retained but **aggregated into ICD-10 chapters** (e.g., Chapter IX: Diseases of the Circulatory System). This avoids the extreme specificity of individual codes while preserving clinical interpretability and allowing the model to learn meaningful patterns across diagnosis categories.

### Engineered Features

Four features were engineered to capture healthcare access patterns that may influence care and LoS:

- **Urban/Rural Flag:** Patient and provider ZIP codes were mapped against a reference list of rural and urban counties to assign each hospitalization a binary urban/rural indicator.
- **Patient Coordinates:** The geographic coordinates of each patient's residential ZIP code, using [`pgeocode`](https://pgeocode.readthedocs.io/en/latest/), a Python library for postal code-based geolocation.
- **Provider Coordinates:** The geographic coordinates of each providers address.
- **Patient-to-Hospital Distance:** The geographic distance between each patient's residential ZIP code and the hospital location was calculated using GoogleAPI and pgeocode.

---

## Exploratory Data Analysis

Our EDA investigated the distribution of LoS across the dataset and correlations between admission-level features and LoS. Key findings informed both our feature engineering choices and our modeling strategy.

![LoS Distribution](assets/los_distribution.png)
*Figure 1: Distribution of patient length of stay across all hospitalizations.*

![Feature Correlations](assets/feature_correlations.png)
*Figure 2: Correlation heatmap of selected admission features with LoS.*

---

## Modeling Approach

### Baseline

A **linear regression** model was established as the baseline to benchmark more complex approaches. While interpretable and computationally efficient, linear regression was limited in its ability to capture the nonlinearity inherent to hospital admission data.

### Tree-Based Models

Four tree-based models were developed and compared:

**Random Forest** leverages an ensemble of decorrelated decision trees to reduce variance and improve generalization. Hyperparameters were tuned to balance model complexity and overfitting.

**XGBoost** applies gradient boosting with regularization to iteratively correct prediction errors, offering strong performance on structured tabular data.

**LightGBM** is a highly efficient gradient boosting framework using leaf-wise tree growth, enabling faster training on large datasets while maintaining competitive accuracy.

**CatBoost** is a gradient boosting framework specifically designed to handle categorical features natively without extensive preprocessing — a key advantage given the prevalence of categorical variables (including ICD-10 chapter codes, facility type, and urban/rural flag) in our dataset.

Each model used a different hyperparameter tuning strategy; details are documented in the respective modeling notebooks under `models/`.

---

## Results

### Model Comparison

The table below reports performance across all four metrics for each model. The second table shows the delta relative to the linear regression baseline (negative = improvement over baseline).

**Absolute Metrics**

| Model | RMSE | MAE | Huber | Quantile |
|---|---|---|---|---|
| Linear Regression (Baseline) | 12.9841 | 3.5459 | 5.4670 | 1.7715 |
| Random Forest | 12.3515 | 3.2480 | 4.9660 | 1.4281 |
| LightGBM | 13.8803 | 2.7116 | 4.0105 | 1.8960 |
| XGBoost | 6.9080 | 2.9402 | 4.2265 | 1.4640 |
| CatBoost (MAE-tuned) | 13.7926 | 2.7501 | 4.1383 | 2.0405 |
| **CatBoost (RMSE-tuned)** | **13.1964** | **3.0850** | **4.6182** | **1.5405** |

**Delta vs. Baseline (negative = improvement)**

| Model | RMSE | MAE | Huber | Quantile |
|---|---|---|---|---|
| Random Forest | -0.6326 | -0.2979 | -0.5009 | -0.3434 |
| LightGBM | +0.8962 | -0.8343 | -1.4565 | +0.1245 |
| XGBoost | -6.0761 | -0.6057 | —1.2405 | —0.3075 |
| CatBoost (MAE-tuned) | +0.8085 | -0.7959 | -1.3287 | +0.2690 |
| CatBoost (RMSE-tuned) | +0.2122 | -0.4610 | -0.8488 | -0.2309 |


### Final Model: CatBoost

**CatBoost** was selected as the final model for its robust handling of categorical features and strong, consistent performance across all four KPI metrics. It was evaluated in two tuning configurations (MAE-optimized and RMSE-optimized), providing flexibility depending on the operational priority of the end user.

---

## Future Work

- **Subgroup analysis** by diagnosis category, patient demographics, and facility type to surface potential disparities in levels of care and identify cases warranting targeted model refinement.
- **Extended feature set exploration**, including procedures performed at admission or insurance/payer type, to assess whether additional admission-level signals can further reduce prediction error.
- **Live hospital validation** in a real-world environment to assess model performance outside the Texas 2017–2019 context and inform integration into clinical workflows.
- **Modernizing the dataset** to include data from 2020-2026. The difficulty here was legal hurdles that definitely were surmountable.
- Incorporate **hybrid models** that perform classification tasks and regression tasks to remove outliers more effectively
---

## Description of Repository

```
├── data/                 # Raw hospitalization data from Texas DHHS
│   ├── common_training_set/ # Raw training data after split
│   ├── common_testing_set/  # Raw testing data after split
├── models/               # All analysis and modeling notebooks
│   ├── CatBoost.ipynb
│   ├── LinearRegressor_model.ipynb
│   ├── RandomForestRegressor_model.ipynb
│   ├── XGBRegressor.ipynb
│   └── lightgbm.ipynb
├── EDA/                     # Exploratory Data Analysis (EDA) scripts
├── deliverables/            # Executive summary and presentation slides
├── assets/                  # Figures and images for the README
└── README.md
```

---

## How to Run the Models
Once the repository is cloned, run the command ./extract.sh in the terminal. This should automatically create the files the notebooks will run in the correct place, and the notebooks should run from there.
