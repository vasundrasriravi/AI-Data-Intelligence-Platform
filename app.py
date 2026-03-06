import streamlit as st
import pandas as pd
import os

from agents.issue_detector import detect_issues
from agents.strategy_agent import decide_strategy
from agents.cleaning_agent import apply_cleaning
from agents.validation_agent import validate_cleaning
from agents.explanation_agent import generate_explanation
from agents.dataset_analyzer import detect_dataset_type
from agents.model_recommender import recommend_model
from agents.report_generator import generate_pdf_report


st.set_page_config(page_title="AI Data Intelligence Platform", layout="wide")

st.title("🧠 AI Data Intelligence Platform")

st.write("Upload a dataset to automatically detect issues, clean data, and get ML recommendations.")


# File Upload
file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])


if file:

    # Read dataset
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    original_df = df.copy()

    # -------------------------
    # Show Original Dataset
    # -------------------------
    st.subheader("📊 Original Dataset")
    st.dataframe(df.head(10))


    # -------------------------
    # Detect Issues
    # -------------------------
    issues = detect_issues(df)


    # -------------------------
    # Cleaning Strategy
    # -------------------------
    strategy = decide_strategy(issues)

    cleaned_df, _ = apply_cleaning(df, strategy)

    validation_report = validate_cleaning(original_df, cleaned_df)

    explanations = generate_explanation(strategy, validation_report)


    # -------------------------
    # Show Cleaned Dataset
    # -------------------------
    st.subheader("🧹 Cleaned Dataset")
    st.dataframe(cleaned_df.head(10))


    # -------------------------
    # Target Column Selection
    # -------------------------
    target_column = st.selectbox(
        "Select Target Column for Model Recommendation",
        cleaned_df.columns
    )


    # -------------------------
    # Detect Dataset Type
    # -------------------------
    dataset_type = detect_dataset_type(cleaned_df, target_column)

    models, metrics, preprocessing = recommend_model(dataset_type)


    # -------------------------
    # Dashboard Metrics
    # -------------------------
    st.subheader("⚡ Data Quality Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Duplicates", issues["duplicates"])

    total_iqr = sum(issues["iqr_outliers"].values())
    col2.metric("IQR Outliers", total_iqr)

    col3.metric("Isolation Forest", issues["isolation_forest_outliers"])

    col4.metric("Dataset Type", dataset_type)


    # -------------------------
    # Missing Values Chart
    # -------------------------
    st.subheader("📈 Missing Values")

    missing = pd.Series(issues["missing_values"])

    st.bar_chart(missing)


    # -------------------------
    # Correlation Matrix
    # -------------------------
    st.subheader("🔥 Correlation Matrix")

    corr = cleaned_df.select_dtypes("number").corr()

    st.dataframe(corr)


    # -------------------------
    # Model Recommendation
    # -------------------------
    st.subheader("🤖 Model Recommendation")

    st.write("**Recommended Models:**")
    for m in models:
        st.write("-", m)

    st.write("**Evaluation Metrics:**")
    for m in metrics:
        st.write("-", m)

    st.write("**Preprocessing Suggestions:**")
    for p in preprocessing:
        st.write("-", p)


    # -------------------------
    # Cleaning Explanation
    # -------------------------
    st.subheader("📝 Cleaning Explanation")

    for e in explanations:
        st.write("•", e)


    # -------------------------
    # Generate AI Report
    # -------------------------
    report_path = "AI_Data_Report.pdf"

    generate_pdf_report(
        report_path,
        explanations,
        dataset_type,
        models,
        metrics
    )


    # -------------------------
    # Download Buttons
    # -------------------------
    st.subheader("⬇ Download Results")

    col1, col2 = st.columns(2)

    # Download Cleaned Dataset
    with col1:
        st.download_button(
            label="Download Cleaned Dataset",
            data=cleaned_df.to_csv(index=False),
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )

    # Download AI Report
    with col2:
        if os.path.exists(report_path):
            with open(report_path, "rb") as f:
                st.download_button(
                    label="Download AI Report",
                    data=f,
                    file_name="AI_Data_Report.pdf",
                    mime="application/pdf"
                )