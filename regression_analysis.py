import pandas as pd
import numpy as np
import statsmodels.api as sm

def perform_regression(data, dependent_var, independent_var):
    # Check and convert data types
    if data[dependent_var].dtype not in [np.float64, np.int64]:
        data[dependent_var] = pd.to_numeric(data[dependent_var], errors='coerce')
    
    if data[independent_var].dtype not in [np.float64, np.int64]:
        data[independent_var] = pd.to_numeric(data[independent_var], errors='coerce')
    
    # Drop any rows with NaN values that might have resulted from the conversion
    data = data.dropna(subset=[independent_var, dependent_var])
    
    # Ensure there is enough data to perform regression
    if data.shape[0] < 2:
        raise ValueError("Not enough data to perform regression after cleaning.")
    
    # Add a constant term for the intercept in the model
    X = sm.add_constant(data[independent_var])
    y = data[dependent_var]

    # Fit the regression model
    model = sm.OLS(y, X).fit()
    
    return model.summary()
