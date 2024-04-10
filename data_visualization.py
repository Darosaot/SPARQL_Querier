import pandas as pd
import plotly.express as px
import streamlit as st

def visualize_data(data, columns, viz_type):
    df = pd.DataFrame(data, columns=columns)
    
    # Dynamically generate axis selection based on visualization type
    if viz_type in ["Line Chart", "Bar Chart", "Pie Chart"]:
        x_axis = st.selectbox("Choose the X-axis variable:", columns, key="x_axis")
        if viz_type != "Pie Chart":
            y_axis = st.selectbox("Choose the Y-axis variable:", columns, index=1 if len(columns) > 1 else 0, key="y_axis")
        else:
            y_axis = None
    else:
        x_axis, y_axis = None, None
    
    # Generate the appropriate plot based on the visualization type and selected axes
    if viz_type == "Table":
        st.table(df)
    elif viz_type == "Line Chart" and x_axis and y_axis:
        fig = px.line(df, x=x_axis, y=y_axis)
        st.plotly_chart(fig)
    elif viz_type == "Bar Chart" and x_axis and y_axis:
        fig = px.bar(df, x=x_axis, y=y_axis)
        st.plotly_chart(fig)
    elif viz_type == "Pie Chart" and x_axis:
        fig = px.pie(df, names=x_axis, values=df.columns[1])  # Assuming the second column as default for values
        st.plotly_chart(fig)
    elif not viz_type == "Table":
        st.warning("Please select variables for the axes.")

def export_to_csv(data, columns):
    if data and columns:
        df = pd.DataFrame(data, columns=columns)
        csv = df.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name="query_results.csv", mime='text/csv')
