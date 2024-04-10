import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
# Use the following imports for data visualization and export
from data_visualization import visualize_data
from query_executor import execute_query  # Import the execute_query function
from query_templates import query_templates
from results_export import export_to_csv, export_to_json, export_to_excel
import xlsxwriter

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

def is_valid_sparql(query):
    required_keywords = ['SELECT', 'WHERE', '{', '}']  # Basic elements of a query
    return all(keyword in query for keyword in required_keywords)

# User login form
# with st.sidebar:
#     st.title("Login")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     login_button = st.button("Login")

# Attempt login on button click
# if login_button:
#     st.session_state['logged_in'] = check_login(username, password)

# Assume logged in for the purpose of this temporary adaptation
st.session_state['logged_in'] = True

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
    query_text = st.text_area("SPARQL Query:", height=300, value=query_templates.get(template_selection, ""), help="Enter your SPARQL query here. Make sure to include PREFIX declarations if necessary.")

    # Execute query button
    if st.button('Execute Query') and st.session_state['sparql_endpoint']:
        if not is_valid_sparql(query_text):
            st.error("The SPARQL query seems to be invalid. Please check the syntax.")
        else:
            result = execute_query(st.session_state['sparql_endpoint'], query_text)  # Now we get a dictionary back
            
            if result['success']:
                if result['data']:
                    # Store results in session state
                    st.session_state['query_results'] = result['data']
                    st.session_state['columns'] = result['columns']
                    # Informing the user about successful execution and execution time
                    st.success(f"Query executed successfully, retrieved {len(result['data'])} results in {result['execution_time']:.2f} seconds.")
                else:
                    st.write("No results found.")
            else:
                # Handle errors more gracefully
                st.error(f"An error occurred during query execution: {result['error']}")
    # Visualization selection and rendering if query results exist
    if 'query_results' in st.session_state and st.session_state['query_results'] is not None:
        selected_viz = st.selectbox("Select visualization type:", ["Table", "Line Chart", "Bar Chart", "Pie Chart"])
        
        # Assuming visualize_data now internally handles everything including:
        # - Dynamic UI elements for axis selection
        # - Any data filtering UI
        # - Chart customization options
        # Therefore, you just call it with the data, columns, and selected viz type.
        visualize_data(st.session_state['query_results'], st.session_state['columns'], selected_viz)
        # Export options
        export_format = st.selectbox("Select export format:", ["CSV", "JSON", "Excel"])
        
        if export_format == "CSV":
            export_to_csv(st.session_state['query_results'], st.session_state['columns'])
        elif export_format == "JSON":
            export_to_json(st.session_state['query_results'], st.session_state['columns'])
        elif export_format == "Excel":
            export_to_excel(st.session_state['query_results'], st.session_state['columns'])


