import pandas as pd
import plotly.express as px
import streamlit as st

def visualize_data(data, columns, viz_type):
    df = pd.DataFrame(data, columns=columns)
    
    if viz_type == "Table":
        st.table(df)
    elif viz_type in ["Line Chart", "Bar Chart"]:
        x_axis = st.selectbox("Choose the X-axis variable:", columns, key="x_axis_" + viz_type)
        y_axis = st.selectbox("Choose the Y-axis variable:", columns, index=1 if len(columns) > 1 else 0, key="y_axis_" + viz_type)
        
        if st.checkbox('Customize Chart Color?', key='color_' + viz_type):
            color = st.color_picker('Pick a color', '#00f900')  # Default to neon green
        else:
            color = None
        
        if viz_type == "Line Chart":
            fig = px.line(df, x=x_axis, y=y_axis, line_shape='linear', color_discrete_sequence=[color] if color else None)
            st.plotly_chart(fig)
        elif viz_type == "Bar Chart":
            fig = px.bar(df, x=x_axis, y=y_axis, color_discrete_sequence=[color] if color else None)
            st.plotly_chart(fig)
    elif viz_type == "Pie Chart":
        x_axis = st.selectbox("Choose the segment names column:", columns, key="x_axis_pie")
        # Automatically use the second column as values if available, for the pie chart
        if len(columns) > 1:
            values_col = columns[1]  # Assumes the second column is appropriate for values
            fig = px.pie(df, names=x_axis, values=values_col)
            st.plotly_chart(fig)
        else:
            st.warning("Not enough columns for a pie chart. Please select a different visualization type.")
    else:
        st.warning("Unsupported visualization type selected.")

def export_to_csv(data, columns):
    df = pd.DataFrame(data, columns=columns)
    csv = df.to_csv(index=False)
    st.download_button(label="Download CSV", data=csv, file_name="query_results.csv", mime='text/csv')
