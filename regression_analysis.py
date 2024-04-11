import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm

def perform_regression(data, dependent_var, independent_vars, regression_type='linear', family_type=None):
    # Handle data conversions upfront
    try:
        # Apply numeric conversion to independent variables and handle exceptions
        data[independent_vars] = data[independent_vars].apply(pd.to_numeric, errors='coerce')
        # Convert dependent variable to numeric for linear regression or to categorical codes for logistic regression
        if regression_type == 'logistic':
            data[dependent_var] = data[dependent_var].astype('category').cat.codes
        else:
            data[dependent_var] = pd.to_numeric(data[dependent_var], errors='coerce')
    except Exception as e:
        return None, f"Error converting data to numeric: {e}"

    # Dropping rows with NaN values which might be introduced by conversion
    data = data.dropna(subset=[dependent_var] + independent_vars)

    if data.empty:
        return None, "Data is empty after dropping NaN values."

    # Add a constant for intercept
    X = sm.add_constant(data[independent_vars])
    y = data[dependent_var]

    try:
        if regression_type == 'linear':
            model = sm.OLS(y, X).fit()
        elif regression_type == 'logistic':
            if family_type in ["Binomial", "Poisson", "Negative Binomial"]:
                if family_type == "Binomial":
                    model = sm.Logit(y, X).fit()
                else:
                    model = sm.GLM(y, X, family=getattr(sm.families, family_type)()).fit()
            else:
                return None, "Invalid or unspecified family type for logistic regression."
    except Exception as e:
        return None, f"Regression error: {e}"

    return model.summary().as_text(), None
