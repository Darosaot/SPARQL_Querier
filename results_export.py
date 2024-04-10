import pandas as pd
import streamlit as st
import xlsxwriter
from io import BytesIO

def export_to_csv(data, columns):
    df = pd.DataFrame(data, columns=columns)
    csv = df.to_csv(index=False)
    st.download_button(label="Download as CSV", data=csv, file_name="query_results.csv", mime='text/csv')

def export_to_json(data, columns):
    df = pd.DataFrame(data, columns=columns)
    json = df.to_json(orient='records')
    st.download_button(label="Download as JSON", data=json, file_name="query_results.json", mime='application/json')

def export_to_excel(data, columns):
    df = pd.DataFrame(data, columns=columns)
    # Create a BytesIO buffer
    output = BytesIO()
    # Use ExcelWriter, specifying the engine and buffer
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    # Important: Seek to the start of the stream
    output.seek(0)
    # Use the buffer in Streamlit's download_button
    st.download_button(label="Download as Excel", data=output, file_name="query_results.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
