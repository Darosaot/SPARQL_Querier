import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer

def professional_styled_table(df, page_size=100):
    """
    Applies advanced styling to a DataFrame for a professional look and displays it in the Streamlit app with pagination.
    
    Parameters:
    - df: The DataFrame to display.
    - page_size: Number of rows to display per page.
    """
    # Determine the total number of pages
    total_pages = len(df) // page_size + (1 if len(df) % page_size > 0 else 0)
    
    # Initialize or update the current page number in the session state
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 1  # Start with the first page
    
    # Display current page number and total pages
    st.write(f"Page {st.session_state['current_page']} of {total_pages}")
    
    # Pagination controls
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button('Previous'):
            if st.session_state['current_page'] > 1:
                st.session_state['current_page'] -= 1
    with col3:
        if st.button('Next'):
            if st.session_state['current_page'] < total_pages:
                st.session_state['current_page'] += 1
    
    # Determine the portion of the DataFrame to display
    start_idx = (st.session_state['current_page'] - 1) * page_size
    end_idx = start_idx + page_size
    df_subset = df.iloc[start_idx:end_idx]
    
    # Display the styled DataFrame (subset)
    st.dataframe(df_subset)  # You may apply styling here as needed

def visualize_data(data, columns, viz_type):
    df = pd.DataFrame(data, columns=columns)
    
    # Generate the appropriate plot based on the visualization type and selected axes
    if viz_type == "Table":
        filtered_df = dataframe_explorer(df, case=False)
        st.dataframe(filtered_df, use_container_width=True)
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
