import pandas as pd

def profile_data(df):
    profile = {}
    profile["rows"] = df.shape[0]
    profile["columns"] = df.shape[1]
    profile["missing"] = df.isnull().sum().to_dict()
    profile["duplicates"] = int(df.duplicated().sum())
    profile["dtypes"] = df.dtypes.astype(str).to_dict()
    return profile