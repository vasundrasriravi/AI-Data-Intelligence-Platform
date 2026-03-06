import numpy as np
import pandas as pd

def apply_cleaning(df, strategy, round_values=False, normalize_values=False):
    cleaned_df = df.copy()
    explanation = []

    # Remove duplicates
    if strategy["remove_duplicates"]:
        before = len(cleaned_df)
        cleaned_df = cleaned_df.drop_duplicates()
        after = len(cleaned_df)
        explanation.append(f"Removed {before-after} duplicate rows.")

    # Handle missing values (only NaN)
    for col in strategy["handle_missing"]:
        if col not in cleaned_df.columns:
            continue

        if pd.api.types.is_numeric_dtype(cleaned_df[col]):
            mean_val = cleaned_df[col].mean()
            cleaned_df[col] = cleaned_df[col].fillna(mean_val)
            explanation.append(f"Filled missing values in {col} using mean.")
        else:
            mode_val = cleaned_df[col].mode()[0]
            cleaned_df[col] = cleaned_df[col].fillna(mode_val)
            explanation.append(f"Filled missing values in {col} using mode.")

    # Outlier clipping (IQR)
    numeric_cols = cleaned_df.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        Q1 = cleaned_df[col].quantile(0.25)
        Q3 = cleaned_df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        cleaned_df[col] = cleaned_df[col].clip(lower, upper)
        explanation.append(f"Clipped outliers in {col} using IQR.")

    # Normalize (optional)
    if normalize_values:
        for col in numeric_cols:
            min_val = cleaned_df[col].min()
            max_val = cleaned_df[col].max()
            if max_val != min_val:
                cleaned_df[col] = (cleaned_df[col] - min_val) / (max_val - min_val)
        explanation.append("Normalized numeric columns using Min-Max scaling.")

    # Round values (optional)
    if round_values:
        for col in numeric_cols:
            cleaned_df[col] = cleaned_df[col].round(2)
        explanation.append("Rounded numeric columns to 2 decimal places.")

    # Normalize text
    for col in strategy["normalize_text"]:
        if col in cleaned_df.columns:
            cleaned_df[col] = cleaned_df[col].astype(str).str.lower().str.strip()
            explanation.append(f"Normalized text in {col}.")

    return cleaned_df, explanation