
## Features for training

- Data is taken from https://www.dshs.texas.gov/center-health-statistics/texas-health-care-information-collection/download-and-purchase-data/texas-inpatient-public-use-data-file-pudf/hospital-discharge-data-public-use-data-file

- We have up to 86 features/descriptors that can be unambiguously known at the point of admission of the patient.

- The **LENGTH_OF_STAY** is used for the target.

- Some of the features can be combined. For instance, We can combine **PRINC_DIAG_CODE** and **POA_PRINC_DIAG_CODE** into a new feature **ADMIT_PRINC_DIAG_CODE** which describes the principal diagnostic code *on admission*. 

- This yields the new features **ADMIT_OTH_DIAG_CODE_1** to **ADMIT_OTH_DIAG_CODE_24**, and **ADMIT_E_CODE_1** to **ADMIT_E_CODE_10**.

- The diagnostic codes can be simplified by truncating them to the first three characters, such as  "R2740" -> "R27".

- Even after truncating the diagnostic codes, there are stil 2600 possible diagnostic codes. Instead of describing the patients by their individual diagnostic codes (e.g. "R27", "E99"), it may be more useful to group their diagnostic codes (e.g. "F01-F99"), like in https://ftp.cdc.gov/pub/health_statistics/nchs/publications/ICD10CM/2022/icd10cm-tabular-2022-April-1.pdf where codes are grouped by "chapters" or body systems.

## Table of features

| Choice of feature | Description | Comments |
|---|---|---|
| TYPE_OF_ADMISSION | Code indicating the type of admission | None |
| SOURCE_OF_ADMISSION | Code indicating the source of admission | None |
| PAT_STATE | State of the patient’s mailing address in Texas and contiguous states | None |
| PAT_ZIP | Patient’s five-digit ZIP code | May not be necessary if we have county |
| PAT_COUNTRY | Country of patient’s residential address | To filter out non-US patients |
| PAT_COUNTY | FIPS code of patient’s county | May also be used to categorize rural vs. urban county |
| PUBLIC_HEALTH_REGION | Public Health Region of patient’s address | None |
| SEX_CODE | Gender of the patient as recorded at date of admission or start of care | None |
| RACE | Code indicating the patient’s race | None |
| ETHNICITY | Code indicating the Hispanic origin of the patient | Not very useful possibly | 
| ADMIT_WEEKDAY | Code indicating day of week patient is admitted | None |
| LENGTH_OF_STAY | Length of stay in days | None |
| PAT_AGE | Code indicating age of patient in days or years on date of discharge | None |
| ADMITTING_DIAGNOSIS | ICD-10-CM diagnosis code, including the 4th, 5th, 6th and 7th digits if applicable. Decimal is implied following the third character | None |
| PRINC_DIAG_CODE | ICD-10-CM diagnosis code for the principal diagnosis, including the 4th, 5th, 6th and 7th digits if applicable. Decimal is implied following the third character | None |
| POA_PRINC_DIAG_CODE | Code identifying whether Principal Diagnosis code was present at the time the patient was admitted to the hospital | None |
| OTH_DIAG_CODE_1 | ICD-10-CM diagnosis code, including the 4th, 5th, 6th and 7th digits if applicable. Decimal is implied following the third character | Up to 24 more additional diagnostic codes |
| POA_OTH_DIAG_CODE_1 | Code identifying whether Oth_Diag_Code_1 code was present at the time the patient was admitted to the hospital | None |
| ... | ... | ... |
| OTH_DIAG_CODE_24 | ICD-10-CM diagnosis code, including the 4th, 5th, 6th and 7th digits if applicable. Decimal is implied following the third character | None |
| POA_OTH_DIAG_CODE_24 | Code identifying whether Oth_Diag_Code_24 code was present at the time the patient was admitted to the hospital | None |
| E_CODE_1 | ICD-10-CM diagnosis code, including the 4th, 5th, 6th and 7th digits if applicable, of the primary external cause of morbidity. A decimal is implied following the third character. | None |
| POA_E_CODE_1 | Code identifying whether E_Code_1 code was present at the time the patient was admitted to the hospital | None |
| ... | ... | ... |
| E_CODE_10 | ICD-10-CM diagnosis code, including the 4th, 5th, 6th and 7th digits if applicable, of an additional external cause of morbidity. Decimal is implied following the third character. | None |
| POA_E_CODE_10 | Code identifying whether E_Code_10 code was present at the time the patient was admitted to the hospital | None |
| PROVIDER_NAME | Hospital name provided by the hospital. | None |
| EMERGENCY_DEPT_FLAG | Indicator of emergency department visit. | None |


