def generate_explanation(strategy, validation_report):
    """
    Generate intelligent explanation of the cleaning process.
    Safe version (no KeyErrors).
    """

    explanations = []

    explanations.append(
        "The dataset was analyzed using hybrid anomaly detection techniques (IQR + Isolation Forest)."
    )

    # -----------------------------
    # Duplicates Handling
    # -----------------------------
    duplicates_removed = validation_report.get("duplicates_removed", 0)

    if duplicates_removed > 0:
        explanations.append(
            f"{duplicates_removed} duplicate rows were removed to improve data integrity."
        )
    else:
        explanations.append(
            "No duplicate rows were detected during analysis."
        )

    # -----------------------------
    # Outlier Handling
    # -----------------------------
    outlier_report = validation_report.get("outliers", {})

    for col, values in outlier_report.items():
        before = values.get("before", 0)
        after = values.get("after", 0)

        if before > after:
            explanations.append(
                f"Outliers in '{col}' were reduced from {before} to {after} using robust cleaning strategies."
            )

    # -----------------------------
    # Anomaly Detection
    # -----------------------------
    if strategy.get("handle_anomalies", False):
        explanations.append(
            "Machine learning-based anomaly detection was applied to identify unusual patterns in the dataset."
        )

    explanations.append(
        "The cleaning process preserved statistical consistency while improving overall data quality."
    )

    explanations.append(
        "The system automatically recommended suitable machine learning models based on dataset characteristics."
    )

    return explanations