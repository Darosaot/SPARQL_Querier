import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
# Use the following imports for data visualization and export
from data_visualization import visualize_data, export_to_csv


# Default credentials
DEFAULT_USER = "ppds"
DEFAULT_PASS = "ppds"

# Function to check login credentials
def check_login(username, password):
    return username == DEFAULT_USER and password == DEFAULT_PASS

# Initialize session state for login status and query results
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'query_results' not in st.session_state:
    st.session_state['query_results'] = None
if 'columns' not in st.session_state:
    st.session_state['columns'] = None

# SPARQL endpoint
sparql_endpoint = "http://ppds-test-lb-1379769313.eu-central-1.elb.amazonaws.com:8890/sparql"


# Predefined query templates
query_templates = {
    "Select a template": "",
    "Count the number of notices": """
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX epo: <http://data.europa.eu/a4g/ontology#>
PREFIX cccev: <http://data.europa.eu/m8g/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX locn: <http://www.w3.org/ns/locn#>
PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX euvoc: <http://publications.europa.eu/ontology/euvoc#>

SELECT (COUNT(DISTINCT ?notice) AS ?numberOfNotices)
WHERE {
    ?notice a epo:Notice .
}
""",
    "Count the number of notices per month":"""
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX epo: <http://data.europa.eu/a4g/ontology#>
PREFIX cccev: <http://data.europa.eu/m8g/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX locn: <http://www.w3.org/ns/locn#>
PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX euvoc: <http://publications.europa.eu/ontology/euvoc#>

SELECT ?monthName (COUNT(DISTINCT ?notice) AS ?numberOfNotices)
WHERE {
    ?notice a epo:Notice .


# YEAR AND MONTH
    OPTIONAL {
        ?notice epo:hasDispatchDate ?date .
    }
    BIND(IF(BOUND(?date),year(xsd:date(?date)),"") AS ?year)
    FILTER(?year=2022)
    BIND(IF(BOUND(?date),month(xsd:date(?date)),"") AS ?month)
    BIND(IF(!BOUND(?month), "",
        IF(?month = 1, "January",
        IF(?month = 2, "February",
        IF(?month = 3, "March",
        IF(?month = 4, "April",
        IF(?month = 5, "May",
        IF(?month = 6, "June",
        IF(?month = 7, "July",
        IF(?month = 8, "August",
        IF(?month = 9, "September",
        IF(?month = 10, "October",
        IF(?month = 11, "November", "December")))))))))))) AS ?monthName)
} group by ?monthName
"""
}

# User login form
with st.sidebar:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

# Attempt login on button click
if login_button:
    st.session_state['logged_in'] = check_login(username, password)

# Function to export data to CSV
def export_to_csv(data, columns):
    if data and columns:
        df = pd.DataFrame(data, columns=columns)
        csv = df.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name="query_results.csv", mime='text/csv')

# Visualization options
viz_options = ["Table", "Line Chart", "Bar Chart", "Pie Chart"]

# Show main application if logged in
if st.session_state['logged_in']:
    st.title('SPARQL Editor & Querier')

    # Input for manually setting the SPARQL endpoint
    st.session_state['sparql_endpoint'] = st.text_input("SPARQL Endpoint", value=st.session_state.get('sparql_endpoint', ''))
    
    # Dropdown for selecting query templates
    template_selection = st.selectbox("Query Templates:", list(query_templates.keys()))

    # Text area for inputting or modifying the SPARQL query
    query_text = st.text_area("SPARQL Query:", height=300, value=query_templates.get(template_selection, ""))

    # Execute query button
    if st.button('Execute Query') and st.session_state['sparql_endpoint']:
        try:
            sparql = SPARQLWrapper(st.session_state['sparql_endpoint'])
            sparql.setQuery(query_text)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()

            if 'results' in results and 'bindings' in results['results']:
                rows = results['results']['bindings']
                if rows:
                    columns = list(results['head']['vars'])
                    data = [[row[col]['value'] if col in row else "" for col in columns] for row in rows]

                    # Store results in session state
                    st.session_state['query_results'] = data
                    st.session_state['columns'] = columns
                else:
                    st.write("No results found.")
            else:
                st.write("No results found.")
        except Exception as e:
            st.error(f"An error occurred during query execution: {str(e)}")

    # Visualization selection and rendering if query results exist
    if 'query_results' in st.session_state and st.session_state['query_results'] is not None:
        selected_viz = st.selectbox("Select visualization type:", viz_options)
        
        # Replace direct DataFrame creation and Plotly visualization with a call to visualize_data
        visualize_data(st.session_state['query_results'], st.session_state['columns'], selected_viz)

        # Replace the CSV export functionality with a call to export_to_csv from data_visualization.py
        export_to_csv(st.session_state['query_results'], st.session_state['columns'])

