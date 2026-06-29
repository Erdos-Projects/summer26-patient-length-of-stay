import pandas as pd

def extract_data():
    df1 = pd.read_csv("../cleaned_data/unzipped_data/PUDF_base1_4q2019_cleaned.csv", low_memory=False)
    df2 = pd.read_csv("../cleaned_data/unzipped_data/PUDF_base1_3q2019_cleaned.csv", low_memory=False)
    df3 = pd.read_csv("../cleaned_data/unzipped_data/PUDF_base1_2q2019_cleaned.csv", low_memory=False)
    df4 = pd.read_csv("../cleaned_data/unzipped_data/PUDF_base1_1q2019_cleaned.csv", low_memory=False)
    df5 = pd.read_csv("../cleaned_data/unzipped_data/PUDF_base1_4q2018_cleaned.csv", low_memory=False)
    df6 = pd.read_csv("../cleaned_data/unzipped_data/PUDF_base1_3q2018_cleaned.csv", low_memory=False)
    df7 = pd.read_csv("../cleaned_data/unzipped_data/PUDF_base1_2q2018_cleaned.csv", low_memory=False)
    df8 = pd.read_csv("../cleaned_data/unzipped_data/PUDF_base1_1q2018_cleaned.csv", low_memory=False)
    df9 = pd.read_csv("../cleaned_data/unzipped_data/PUDF_base1_4q2017_cleaned.csv", low_memory=False)
    df10 = pd.read_csv("../cleaned_data/unzipped_data/PUDF_base1_3q2017_cleaned.csv", low_memory=False)
    df11 = pd.read_csv("../cleaned_data/unzipped_data/PUDF_base1_2q2017_cleaned.csv", low_memory=False)
    df12 = pd.read_csv("../cleaned_data/unzipped_data/PUDF_base1_1q2017_cleaned.csv", low_memory=False)
    
    
    df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12], ignore_index=True)
    
    return df

def extract_data_mini():
    df = pd.read_csv("../cleaned_data/unzipped_data/PUDF_base1_4q2019_cleaned.csv", low_memory=False)
    
    return df