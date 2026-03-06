def decide_strategy(issues):
    """
    Decide the best cleaning strategy based on detected issues.
    Supports hybrid anomaly detection methods.
    """

    strategy = {
        "remove_duplicates": False,
        "handle_missing": {},
        "handle_outliers": {},
        "handle_anomalies": False,
        "normalize_text": []
    }

    # -----------------------------
    # Handle duplicates
    # -----------------------------
    if issues.get("duplicates", 0) > 0:
        strategy["remove_duplicates"] = True


    # -----------------------------
    # Handle missing values
    # -----------------------------
    missing = issues.get("missing_values", {})

    for col, count in missing.items():

        if count > 0:

            # numeric columns → median
            strategy["handle_missing"][col] = "auto"


    # -----------------------------
    # Handle IQR outliers
    # -----------------------------
    iqr_outliers = issues.get("iqr_outliers", {})

    for col, count in iqr_outliers.items():

        if count > 0:
            strategy["handle_outliers"][col] = "clip"


    # -----------------------------
    # Handle Z-score outliers
    # -----------------------------
    zscore_outliers = issues.get("zscore_outliers", {})

    for col, count in zscore_outliers.items():

        if count > 0:
            strategy["handle_outliers"][col] = "clip"


    # -----------------------------
    # Handle ML anomaly detection
    # -----------------------------
    if issues.get("isolation_forest_outliers", 0) > 0:
        strategy["handle_anomalies"] = True

    if issues.get("lof_outliers", 0) > 0:
        strategy["handle_anomalies"] = True


    # -----------------------------
    # Normalize text columns
    # -----------------------------
    text_columns = issues.get("text_columns", [])

    for col in text_columns:
        strategy["normalize_text"].append(col)


    return strategy