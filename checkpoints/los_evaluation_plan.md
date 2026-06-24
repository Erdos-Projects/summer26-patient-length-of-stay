# Patient Length of Stay (LoS) Prediction – Evaluation Plan

## 1. Overview

This document describes the **model evaluation plan** for a project predicting hospital **length of stay (LoS)** in days using **admission-time data** from Texas healthcare facilities. This is a draft and will be iteratively updated as the methodology and evaluation become more finalized.

At this checkpoint:

- We focus on **admission-only features** (demographics, diagnosis codes at admission, and facility/location information).
- We use a **random 80–20 train/test split** across all facilities.
- We implement a **linear regression baseline**, with several tree-based and boosting models planned for comparison.

---

## 2. Data and Problem Definition

### 2.1 Target Variable

- **Target**: Length of stay (LoS) in days, measured per hospitalization.
- LoS is retained **only as the prediction target** and is not used as a feature.

### 2.2 Unit of Analysis

- **Unit of analysis**: A single row represents **one hospitalization**.
- For HIPAA compliance, data is anonymized; individual patients are not tracked longitudinally.
  - **Implication**: We cannot identify readmissions or multiple hospitalizations for the same person.

### 2.3 Prediction Timing and Use Case

- The model predicts LoS **at admission time**.
- Only information that is realistically available at admission is used as input features.
- Intended deployment scenario:
  - Generalization to **new patients at the same hospitals in Texas** in the future.
  - Since the Texas Department of State Health Services dataset covers a large number of healthcare providers, it should be representative of the state as a whole.

---

## 3. Data Scope and Selection

### 3.1 Facilities and Geography

- Data includes **over 600 facilities** across the state of Texas.
- Available facility location fields:
  - City
  - ZIP code
  - Coordinates (e.g., latitude/longitude)

### 3.2 Time Range

- Data spans **2006–2025**, aggregated at a **quarterly** level.
- Data pre-2016 uses a different diagnostic code (IC-09-CM) and data post-2019 has access restrictions, but is available to members of this group.

### 3.3 Dataset Size and Subset Selection

- Each quarterly dataset contains approximately 700,000 hospitalizations, with each instance including over 160 features.
- The full databse (2006-2025) exceeds 50,000,000 entries, so we plan on initially using a subset of data from 2015-2019.
  -This subset allows us to focus on pre-COVID data, while still using the most up-to-date World Health Orgnization code (ICD-10-CM).
  - For this subset, we treat all years as a **pooled dataset**.

---

## 4. Features and Leakage Handling

### 4.1 Features Used

At this checkpoint, the following feature types are used:

- **Demographics** (admission-time)
- **Diagnosis codes at admission**
  - Encoded using **one-hot encoding**.
- **Patient Residence Location** (e.g. county, ZIP)
  - We decided to focus only on patients that resided in Texas. 
- **Facility information** (e.g., city, ZIP, coordinates)

We do **not** use:

- Labs or vitals
- Post-admission observations
- Post-discharge information

### 4.2 Dropped Features to Mitigate Leakage

To reduce post-outcome leakage, we **explicitly drop**:

- **Charges / cost data** (e.g., total charges, total cost for the stay)
- Any explicit **post-discharge or end-of-stay variables** that would not be known at admission

The LoS value is kept **only** as the prediction target.

### 4.3 Planned Leakage Checks (Not Yet Implemented)

At this checkpoint:

- We have **not yet** implemented formal leakage tests such as:
  - Shuffled-target experiments
  - Systematic feature-drop evaluations beyond simple exclusions.

Planned future work includes:

1. **Shuffled-target sanity check**

2. **Feature-drop robustness tests**
   - Train models with different feature sets:
     - Full feature set (demographics + diagnoses + location).
     - Without location features (demographics + diagnoses only).
     - Without diagnosis codes (demographics + location only).
   - Purpose: Understand how dependent the model is on specific feature groups and how robust performance is to feature changes.

We will explicitly document these results when they are implemented.

---

## 5. Splitting Strategy and Leakage Concerns

### 5.1 Split Strategy

- For the current evaluation, we use a **random 80–20 train/test split** across all hospitalizations.
- Same hospitals can appear in both the training and test sets.
- Time (year/quarter) is **not** used in defining the split.

### 5.2 Temporal Leakage

- Prediction is based on **admission-time data only**.
- We **do not** use any features that are only observed after admission or at discharge.
- Given this, the main temporal leakage risk (using future information to predict the past) is intentionally minimized by feature selection.

### 5.3 Group-Level Leakage by Hospital

- At this checkpoint:
  - Train and test sets both contain hospitalizations from the same hospitals.
  - We **do not** yet enforce hospital-level separation (e.g., no GroupKFold).

- Implications:
  - The evaluation primarily measures generalization to **new patients at already-seen hospitals**.
  - It may **overestimate** or **underestimate** performance for **completely unseen hospitals**.

- Planned future work:
  - Implement **group-based splits** by hospital (e.g., GroupKFold) during model development.
  - Compare performance under:
    - Random splits.
    - Hospital-level splits (to measure generalization to unseen hospitals).

### 5.4 Geographic Leakage and Planned Analyses

- We have facility-level fields: **city, ZIP code, coordinates**.

- We **have not yet** performed geographic grouping or explicit geographic leakage checks.

Planned geographic checks:

1. **Descriptive analyses by city**
   - Compute, per city:
     - Number of facilities
     - Number of hospitalizations
     - Average LoS and distribution (mean, median, standard deviation)
   - Purpose: Identify cities with structurally different LoS patterns.

2. **Performance breakdown by city on the random split**
   - After training the model on the 80–20 split, compute metrics per city on the test set.
   - Purpose: Identify cities/regions where model performance is substantially better or worse.

3. **Future region-aware strategy (if warranted)**
   - If strong geographic variation is observed, we will consider:
     - Grouping hospitals by city or broader region when splitting.
     - Explicitly reporting metrics by geography.

These geographic analyses are **planned but not yet implemented** as of now.

---

## 6. Models and Preprocessing

### 6.1 Baseline and Candidate Models

- **Baseline model**:
  - Linear regression.

- **Additional models (planned for comparison)**:
  - RandomForest
  - XGBoost
  - CatBoost
  - LightGBM

At this checkpoint:

- Linear regression with the random 80–20 split is considered the **baseline**.
- The various tree-based and boosting models are planned for performance comparison.

### 6.2 Model Comparison 

The primary objective is to build a model that predicts inpatient LoS at the time of admission using information available at or near admission. Our model must be able to handle large-scale, high-dimensional data, capture nonlinear relationships, be robust to missing data, support interpretability, and be computationally efficient. 

| Model | Speed/Efficiency | Categorical Features | Flexibility |
| :---- | :---- | :---- | :---- |
| Linear Regression | Fast, scales easily | Needs encoding | Linear, not flexible |
| RandomForest | Slower on large datasets | Needs encoding | Nonlinear tree ensemble, flexible  |
| XGBoost | Fast up to very large datasets | Categorical support | Nonlinear boost trees, very flexible |
| LightGBM | Fastest on large datasets  | Needs encoding | Nonlinear boost trees, very flexible |
| CatBoost | Fast up to very large datasets | Needs encoding | Nonlinear boost trees, very flexible |

---

## 7. Classification Variant (Long vs Short LoS)

In addition to the regression task, we will consider a binary classification formulation:

- **Classification task**: Identify **long LoS** vs **non-long LoS** at admission.
- **Threshold** for long LoS:
  - LoS > **14 days**.

At this checkpoint:

Detailed **classification metrics** (e.g., accuracy, precision/recall, ROC/PR curves) are **not yet defined**.

The classification formulation and its evaluation will be documented in more detail in future updates to this plan.

---

## 8. Robustness and Sensitivity

### 8.1 Time-Based Robustness

- The dataset spans 2016–2019, but all years are treated as a **pooled dataset**.

- Future work may include year-based or quarter-based evaluations to detect temporal drift or seasonal differences in LoS. 

- Additional work may also include years pre-2016 and post-2019.

### 8.2 Hospital-Based Cohorts

- We plan to compute some performance breakdowns by hospital or hospital-type cohorts, such as urban vs rural facilities.
- These are **planned** but not yet fully implemented.

### 8.3 Sensitivity 

- We plan to check model sensitivity to outliers (e.g.low or high LoS).

---

## 9. Summary

### 9.1 Analysis Summary

- **Problem**: Predict LoS in days at admission for hospitalizations across >600 Texas facilities (2016–2019).
- **Unit of Analysis**: Hospitalization-level, anonymized.
- **Features**: Admission-time demographics, diagnosis codes, facility information.
- **Target**: LoS in days.
- **Split**: Random 80–20 train/test across all hospitalizations.
- **Models**: Linear regression (baseline), RandomForest, XGBoost, CatBoost, LightGBM

### 9.2 Key Limitations

- **No temporal split** yet:
  - Time order (year/quarter) is not used in partitioning.
- **No group-level split by hospital** yet:
  - Hospitals appear in both train and test sets.
  - Generalization to unseen hospitals is therefore not directly measured.
- **No geographic grouping/splitting** yet:
  - City/region-aware evaluation is planned but not implemented.
- **No formal adversarial leakage checks** yet:
  - Shuffled-target and feature-drop tests remain planned work.
- **No formal stress-testing protocol** yet:
  - Robustness across cohorts and distributions is not systematically assessed.
- **Classification metrics and decision costs** for the long-LoS task (LoS > 14 days) are not yet defined.

### 9.3 Future Interations

Future versions of this document and the accompanying codebase will aim to close these gaps by:

- Introducing group-based and time-based splits.
- Defining and computing appropriate regression and classification metrics.
- Implementing robustness and stress-testing workflows.
- Incorporating advisor feedback on methodological choices.

### 9.4 Deliverables 

Our finalized project will include the following deliverables:

- Performance metrics between our selected models.
- Interactive map showing LoS in different locations across Texas.
  - May be implemented using Tableau or Folium.
