import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from scipy.stats import zscore

def detect_issues(df):

    issues = {}

    # -----------------------------
    # 1. Duplicate rows
    # -----------------------------
    issues["duplicates"] = int(df.duplicated().sum())

    # -----------------------------
    # 2. Missing values
    # -----------------------------
    issues["missing_values"] = df.isnull().sum().to_dict()

    # -----------------------------
    # 3. Numeric columns
    # -----------------------------
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    # -----------------------------
    # IQR OUTLIER DETECTION
    # -----------------------------
    iqr_outliers = {}

    for col in numeric_cols:

        if df[col].dropna().empty:
            iqr_outliers[col] = 0
            continue

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        if IQR == 0:
            iqr_outliers[col] = 0
        else:
            outlier_count = (
                (df[col] < Q1 - 1.5 * IQR) |
                (df[col] > Q3 + 1.5 * IQR)
            ).sum()

            iqr_outliers[col] = int(outlier_count)

    issues["iqr_outliers"] = iqr_outliers


    # -----------------------------
    # Z-SCORE OUTLIER DETECTION
    # -----------------------------
    zscore_outliers = {}

    for col in numeric_cols:

        if df[col].dropna().empty:
            zscore_outliers[col] = 0
            continue

        z_scores = zscore(df[col].dropna())
        count = (np.abs(z_scores) > 3).sum()

        zscore_outliers[col] = int(count)

    issues["zscore_outliers"] = zscore_outliers


    # -----------------------------
    # ISOLATION FOREST (ML)
    # -----------------------------
    if len(numeric_cols) > 0:

        df_numeric = df[numeric_cols].dropna()

        if not df_numeric.empty:

            model = IsolationForest(
                contamination=0.05,
                random_state=42
            )

            preds = model.fit_predict(df_numeric)

            isolation_outliers = int((preds == -1).sum())

        else:
            isolation_outliers = 0

    else:
        isolation_outliers = 0

    issues["isolation_forest_outliers"] = isolation_outliers


    # -----------------------------
    # LOCAL OUTLIER FACTOR (ML)
    # -----------------------------
    if len(numeric_cols) > 0:

        df_numeric = df[numeric_cols].dropna()

        if len(df_numeric) > 20:

            lof = LocalOutlierFactor(n_neighbors=20)
            preds = lof.fit_predict(df_numeric)

            lof_outliers = int((preds == -1).sum())

        else:
            lof_outliers = 0

    else:
        lof_outliers = 0

    issues["lof_outliers"] = lof_outliers


    # -----------------------------
    # Text columns
    # -----------------------------
    issues["text_columns"] = df.select_dtypes(include="object").columns.tolist()

    return issues