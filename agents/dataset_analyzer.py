import pandas as pd

def detect_dataset_type(df, target_column):
    """
    Detect whether dataset is Classification, Regression, or Time-Series
    """

    if target_column not in df.columns:
        return "Unknown"

    # -------------------------
    # Check Time-Series
    # -------------------------
    for col in df.columns:
        col_lower = col.lower()
        if "date" in col_lower or "time" in col_lower:
            return "Time-Series"

    # -------------------------
    # Classification
    # -------------------------
    if df[target_column].dtype == "object":
        return "Classification"

    if df[target_column].nunique() < 10:
        return "Classification"

    # -------------------------
    # Regression
    # -------------------------
    return "Regression"