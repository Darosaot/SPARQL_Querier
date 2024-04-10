import pandas as pd
import streamlit as st
import xlsxwriter

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
    towrite = pd.ExcelWriter("query_results.xlsx", engine='xlsxwriter')
    df.to_excel(towrite, index=False)
    towrite.save()
    towrite.close()
    with open("query_results.xlsx", "rb") as file:
        st.download_button(label="Download as Excel", data=file, file_name="query_results.xlsx", mime='application/vnd.ms-excel')

# For XML and RDF, you will need specific libraries and formatting. 
# These examples are more complex and depend on your data's structure.
