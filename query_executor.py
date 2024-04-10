from SPARQLWrapper import SPARQLWrapper, JSON
import logging
import time  # Import the time module

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def execute_query(endpoint, query):
    """
    Executes a SPARQL query against a specified endpoint and returns the results along with execution time.
    
    Parameters:
    - endpoint: The SPARQL endpoint URL as a string.
    - query: The SPARQL query as a string.
    
    Returns:
    A dictionary with the following keys:
    - 'success': A boolean indicating if the query was executed successfully.
    - 'columns': A list of column names from the query results (empty if unsuccessful).
    - 'data': A list of rows with each row being a list of values corresponding to the columns (empty if unsuccessful or no results).
    - 'error': An error message if the query execution was unsuccessful (None if successful).
    - 'execution_time': The execution time of the query in seconds.
    """
    start_time = time.time()  # Capture start time
    try:
        sparql = SPARQLWrapper(endpoint)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        end_time = time.time()  # Capture end time after query execution

        if 'results' in results and 'bindings' in results['results']:
            rows = results['results']['bindings']
            if rows:
                columns = list(results['head']['vars'])
                data = [[row[col]['value'] if col in row else "" for col in columns] for row in rows]
                return {
                    'success': True, 
                    'columns': columns, 
                    'data': data, 
                    'error': None,
                    'execution_time': end_time - start_time  # Calculate execution time
                }
            else:
                return {
                    'success': True, 
                    'columns': [], 
                    'data': [], 
                    'error': None,
                    'execution_time': end_time - start_time
                }
        else:
            return {
                'success': False, 
                'columns': [], 
                'data': [], 
                'error': 'No results returned from the query.',
                'execution_time': end_time - start_time
            }
    except Exception as e:
        end_time = time.time()  # Ensure end time is captured even on exception
        logging.error(f"Query execution failed: {str(e)}")
        return {
            'success': False, 
            'columns': [], 
            'data': [], 
            'error': str(e),
            'execution_time': end_time - start_time
        }
