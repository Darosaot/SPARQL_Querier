import pandas as pd
import plotly.express as px
import streamlit as st

def visualize_data(data, columns, viz_type):
    df = pd.DataFrame(data, columns=columns)
    if viz_type == "Table":
        st.table(df)
    elif viz_type == "Line Chart":
        fig = px.line(df, x=df.columns[0], y=df.columns[1:])
        st.plotly_chart(fig)
    elif viz_type == "Bar Chart":
        fig = px.bar(df, x=df.columns[0], y=df.columns[1:])
        st.plotly_chart(fig)
    elif viz_type == "Pie Chart":
        fig = px.pie(df, names=df.columns[0], values=df.columns[1])
        st.plotly_chart(fig)
    else:
        st.warning("Selected visualization type is not supported for the current data.")

def export_to_csv(data, columns):
    if data and columns:
        df = pd.DataFrame(data, columns=columns)
        csv = df.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name="query_results.csv", mime='text/csv')
