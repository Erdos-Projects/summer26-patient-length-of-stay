import pandas as pd

def load_train_data():
    #loads in the data
    for year in range(2017,2020):
        for quarter in range(1,5):    
            fname = "../common_training_data/unzipped_data/PUDF_base1_" + str(quarter) + "q" + str(year) + "_cleaned_train.csv"
            #print(fname)
            df_tmp = pd.read_csv(fname, low_memory=False)

            df_tmp['SOURCE_OF_ADMISSION'] = df_tmp['SOURCE_OF_ADMISSION'].astype(str) # Remove rows with SOURCE_OF_ADMISSION = "`" (invalid value)
            df_tmp.drop(df_tmp[df_tmp["SOURCE_OF_ADMISSION"]=="`"].index,inplace=True)

            if quarter==1 and year==2017:
                df = df_tmp
            else:
                df = pd.concat([df, df_tmp], ignore_index=True) 
            del df_tmp
    df.reset_index(drop=True, inplace=True)
    
    #This bit is datacleaning
    
    #Sets the datatype of the following features      
    df["TYPE_OF_ADMISSION"] = df["TYPE_OF_ADMISSION"].astype(int).astype(str)
    df["PUBLIC_HEALTH_REGION"] = df["PUBLIC_HEALTH_REGION"].astype(int).astype(str)
    df["RACE"] = df["RACE"].astype(int).astype(str)
    df["ETHNICITY"] = df["ETHNICITY"].astype(int).astype(str)
    df["ADMIT_WEEKDAY"] = df["ADMIT_WEEKDAY"].astype(int).astype(str)

    #Adds these two features
    df["PROLONGED"] = [1 if los >= 30 else 0 for los in df["LENGTH_OF_STAY"]] # Create prolonged stay indicator variable
    df["NUM_CODES"] = df[["CODE_"+str(n) for n in range(1,22)]].sum(axis=1) # Count number of diagnosis codes for each patient
    
    
    #Drops the list of redundant features
    redundant_features = ["RECORD_ID", "THCIC_ID", "PAT_ZIP", "PAT_STATE", "PAT_COUNTRY","PAT_COUNTY", "DIAG_CODES_OA", "PROVIDER_ZIP", "CODE_22","PAT_STATUS"]
    for feature in redundant_features:
        if feature in df.columns:
            df.drop(columns=[feature], inplace=True)
            
            
    #merge the two lowest age groups       
    df.loc[df["PAT_AGE"]==0,"PAT_AGE"] = 1
    
    #One-hot encodes emergency dept flag
    df["EMERGENCY_DEPT_FLAG"] = df["EMERGENCY_DEPT_FLAG"].map({"Y":1,"N":0})
    
    
    return df

def load_data_mini():
    #loads in the data
    for year in range(2017,2018):
        for quarter in range(1,2):    
            fname = "../common_training_data/unzipped_data/PUDF_base1_" + str(quarter) + "q" + str(year) + "_cleaned_train.csv"
            #print(fname)
            df_tmp = pd.read_csv(fname, low_memory=False)

            df_tmp['SOURCE_OF_ADMISSION'] = df_tmp['SOURCE_OF_ADMISSION'].astype(str) # Remove rows with SOURCE_OF_ADMISSION = "`" (invalid value)
            df_tmp.drop(df_tmp[df_tmp["SOURCE_OF_ADMISSION"]=="`"].index,inplace=True)

            if quarter==1 and year==2017:
                df = df_tmp
            else:
                df = pd.concat([df, df_tmp], ignore_index=True) 
            del df_tmp
    df.reset_index(drop=True, inplace=True)
    
    #This bit is datacleaning
    
    #Sets the datatype of the following features      
    df["TYPE_OF_ADMISSION"] = df["TYPE_OF_ADMISSION"].astype(int).astype(str)
    df["PUBLIC_HEALTH_REGION"] = df["PUBLIC_HEALTH_REGION"].astype(int).astype(str)
    df["RACE"] = df["RACE"].astype(int).astype(str)
    df["ETHNICITY"] = df["ETHNICITY"].astype(int).astype(str)
    df["ADMIT_WEEKDAY"] = df["ADMIT_WEEKDAY"].astype(int).astype(str)

    #Adds these two features
    df["PROLONGED"] = [1 if los >= 30 else 0 for los in df["LENGTH_OF_STAY"]] # Create prolonged stay indicator variable
    df["NUM_CODES"] = df[["CODE_"+str(n) for n in range(1,22)]].sum(axis=1) # Count number of diagnosis codes for each patient
    
    
    #Drops the list of redundant features
    redundant_features = ["RECORD_ID", "THCIC_ID", "PAT_ZIP", "PAT_STATE", "PAT_COUNTRY","PAT_COUNTY", "DIAG_CODES_OA", "PROVIDER_ZIP", "CODE_22","PAT_STATUS"]
    for feature in redundant_features:
        if feature in df.columns:
            df.drop(columns=[feature], inplace=True)
            
            
    #merge the two lowest age groups       
    df.loc[df["PAT_AGE"]==0,"PAT_AGE"] = 1
    
    #One-hot encodes emergency dept flag
    df["EMERGENCY_DEPT_FLAG"] = df["EMERGENCY_DEPT_FLAG"].map({"Y":1,"N":0})
    
    
    return df

def load_test_data():
    #loads in the data
    for year in range(2017,2020):
        for quarter in range(1,5):    
            fname = "../common_testing_data/unzipped_data/PUDF_base1_" + str(quarter) + "q" + str(year) + "_cleaned_train.csv"
            #print(fname)
            df_tmp = pd.read_csv(fname, low_memory=False)

            df_tmp['SOURCE_OF_ADMISSION'] = df_tmp['SOURCE_OF_ADMISSION'].astype(str) # Remove rows with SOURCE_OF_ADMISSION = "`" (invalid value)
            df_tmp.drop(df_tmp[df_tmp["SOURCE_OF_ADMISSION"]=="`"].index,inplace=True)

            if quarter==1 and year==2017:
                df = df_tmp
            else:
                df = pd.concat([df, df_tmp], ignore_index=True) 
            del df_tmp
    df.reset_index(drop=True, inplace=True)
    
    #This bit is datacleaning
    
    #Sets the datatype of the following features      
    df["TYPE_OF_ADMISSION"] = df["TYPE_OF_ADMISSION"].astype(int).astype(str)
    df["PUBLIC_HEALTH_REGION"] = df["PUBLIC_HEALTH_REGION"].astype(int).astype(str)
    df["RACE"] = df["RACE"].astype(int).astype(str)
    df["ETHNICITY"] = df["ETHNICITY"].astype(int).astype(str)
    df["ADMIT_WEEKDAY"] = df["ADMIT_WEEKDAY"].astype(int).astype(str)

    #Adds these two features
    df["PROLONGED"] = [1 if los >= 30 else 0 for los in df["LENGTH_OF_STAY"]] # Create prolonged stay indicator variable
    df["NUM_CODES"] = df[["CODE_"+str(n) for n in range(1,22)]].sum(axis=1) # Count number of diagnosis codes for each patient
    
    
    #Drops the list of redundant features
    redundant_features = ["RECORD_ID", "THCIC_ID", "PAT_ZIP", "PAT_STATE", "PAT_COUNTRY","PAT_COUNTY", "DIAG_CODES_OA", "PROVIDER_ZIP", "CODE_22","PAT_STATUS"]
    for feature in redundant_features:
        if feature in df.columns:
            df.drop(columns=[feature], inplace=True)
            
            
    #merge the two lowest age groups       
    df.loc[df["PAT_AGE"]==0,"PAT_AGE"] = 1
    
    #One-hot encodes emergency dept flag
    df["EMERGENCY_DEPT_FLAG"] = df["EMERGENCY_DEPT_FLAG"].map({"Y":1,"N":0})
    
    
    return df

cat_features = ['TYPE_OF_ADMISSION',
    'SOURCE_OF_ADMISSION',
    'PUBLIC_HEALTH_REGION',
    'SEX_CODE',
    'RACE',
    'ETHNICITY',
    'ADMIT_WEEKDAY',
    'EMERGENCY_DEPT_FLAG',
    'QUARTER']

num_feats = ['LENGTH_OF_STAY', 'PAT_AGE', 'PAT2PROV_DISTANCE', 'YEAR', 'PAT_LATITUDE', 'PAT_LONGITUDE', 'PROVIDER_LATITUDE', 'PROVIDER_LONGITUDE', 'NUM_CODES']

    