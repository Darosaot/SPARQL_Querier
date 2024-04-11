import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import plotly.graph_objs as go
import io

def perform_regression(data, dependent_var, independent_vars):
    """
    Perform linear regression analysis.

    Args:
        data (DataFrame): Input data.
        dependent_var (str): Name of the dependent variable.
        independent_vars (list): List of names of independent variables.

    Returns:
        tuple: Tuple containing model summary as text, Plotly figure, and potentially an error message.
    """
    # Copy the original DataFrame to avoid modifying the original data
    data_copy = data.copy()

    # Apply conversion to categorical variables and handle exceptions
    try:
        for var in independent_vars:
            if pd.api.types.is_string_dtype(data_copy[var]):
                data_copy[var] = pd.Categorical(data_copy[var]).codes
    except Exception as e:
        return None, None, f"Error converting categorical data: {e}"

    # Apply numeric conversion to independent and dependent variables and handle exceptions
    try:
        data_copy[independent_vars] = data_copy[independent_vars].apply(pd.to_numeric, errors='coerce')
        data_copy[dependent_var] = pd.to_numeric(data_copy[dependent_var], errors='coerce')
    except Exception as e:
        return None, None, f"Error converting data to numeric: {e}"

    # Dropping rows with NaN values which might be introduced by conversion
    data_copy = data_copy.dropna(subset=[dependent_var] + independent_vars)
    if data_copy.empty:
        return None, None, "Data is empty after dropping NaN values."

    # Add a constant for intercept
    X = sm.add_constant(data_copy[independent_vars])
    y = data_copy[dependent_var]

    try:
        # Perform linear regression
        model = sm.OLS(y, X).fit()
        
        # Create a scatter plot of the independent variable vs the dependent variable
        scatter_trace = go.Scatter(
            x=data_copy[independent_vars[0]],
            y=y,
            mode='markers',
            marker=dict(color='blue'),
            name='Data'
        )
        
        # Plot the regression line
        line_trace = go.Scatter(
            x=data_copy[independent_vars[0]],
            y=model.predict(X),
            mode='lines',
            line=dict(color='red'),
            name='Fitted line'
        )
        
        layout = go.Layout(
            xaxis=dict(title=independent_vars[0]),
            yaxis=dict(title=dependent_var),
            legend=dict(x=0.7, y=0.9),
            title='Linear Regression Analysis'
        )

        fig = go.Figure(data=[scatter_trace, line_trace], layout=layout)

        # Return the model summary, the Plotly figure, and None for the error message
        return model.summary().as_text(), fig, None

    except Exception as e:
        return None, None, f"Regression error: {e}"

# Example usage in Streamlit app
if __name__ == "__main__":
    # Sample data
    data = pd.DataFrame({
        'X': np.random.rand(100),
        'Y': np.random.rand(100)
    })

    # Perform linear regression
    model_summary, plot_fig, error = perform_regression(data, 'Y', ['X'])

    # Display results
    if error:
        st.error(error)
    else:
        st.text(model_summary)
        st.plotly_chart(plot_fig)
