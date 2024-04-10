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
    # Use BytesIO as an in-memory buffer
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        writer.save()  # Save the data to the buffer
    output.seek(0)  # Rewind the buffer
    # Use the buffer's contents for the download button
    st.download_button(label="Download as Excel", data=output, file_name="query_results.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# For XML and RDF, you will need specific libraries and formatting. 
# These examples are more complex and depend on your data's structure.
