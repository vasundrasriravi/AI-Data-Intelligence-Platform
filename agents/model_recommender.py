def recommend_model(dataset_type):

    models = []
    metrics = []
    preprocessing = []

    if dataset_type == "Classification":

        models = [
            "Logistic Regression",
            "Random Forest Classifier",
            "XGBoost",
            "Support Vector Machine"
        ]

        metrics = [
            "Accuracy",
            "F1 Score",
            "Precision",
            "Recall",
            "ROC-AUC"
        ]

        preprocessing = [
            "Handle missing values",
            "Encode categorical variables (Label Encoding)",
            "Feature scaling (StandardScaler)"
        ]

    elif dataset_type == "Regression":

        models = [
            "Linear Regression",
            "Random Forest Regressor",
            "Gradient Boosting",
            "XGBoost Regressor"
        ]

        metrics = [
            "MSE",
            "RMSE",
            "MAE",
            "R² Score"
        ]

        preprocessing = [
            "Normalize numerical features",
            "Remove multicollinearity",
            "Feature scaling"
        ]

    elif dataset_type == "Time-Series":

        models = [
            "ARIMA",
            "SARIMA",
            "Prophet",
            "LSTM"
        ]

        metrics = [
            "MAE",
            "RMSE",
            "MAPE"
        ]

        preprocessing = [
            "Resample time intervals",
            "Handle seasonality",
            "Create lag features"
        ]

    return models, metrics, preprocessing