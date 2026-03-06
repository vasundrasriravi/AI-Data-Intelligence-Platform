import pandas as pd
import numpy as np

def validate_cleaning(original_df, cleaned_df):
    report = {}

    # Duplicates
    report["duplicates_before"] = int(original_df.duplicated().sum())
    report["duplicates_after"] = int(cleaned_df.duplicated().sum())

    # Missing values
    report["missing_before"] = original_df.isnull().sum().to_dict()
    report["missing_after"] = cleaned_df.isnull().sum().to_dict()

    # Outliers (IQR check)
    numeric_cols = original_df.select_dtypes(include=np.number).columns
    outlier_report = {}

    for col in numeric_cols:
        Q1 = original_df[col].quantile(0.25)
        Q3 = original_df[col].quantile(0.75)
        IQR = Q3 - Q1
        before = ((original_df[col] < Q1 - 1.5*IQR) | (original_df[col] > Q3 + 1.5*IQR)).sum()

        Q1_c = cleaned_df[col].quantile(0.25)
        Q3_c = cleaned_df[col].quantile(0.75)
        IQR_c = Q3_c - Q1_c
        after = ((cleaned_df[col] < Q1_c - 1.5*IQR_c) | (cleaned_df[col] > Q3_c + 1.5*IQR_c)).sum()

        outlier_report[col] = {
            "before": int(before),
            "after": int(after)
        }

    report["outliers"] = outlier_report

    return report