import sqlite3
import os.path
from config import DB_PATH

def initialize_database():
    """
    Check if the database exists, and create it if it doesn't.
    """
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create accounts table
        cursor.execute('''
        CREATE TABLE accounts (
            uuid TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
        print(f"Database {DB_PATH} created successfully.")
    else:
        print(f"Database {DB_PATH} already exists.")

def execute_query(query, params=(), fetch_one=False):
    """
    Execute a SQL query and return the results.
    
    Args:
        query (str): SQL query to execute
        params (tuple): Parameters for the query
        fetch_one (bool): If True, return only one result
        
    Returns:
        The query results
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(query, params)
    
    if fetch_one:
        result = cursor.fetchone()
    else:
        result = cursor.fetchall()
    
    conn.commit()
    conn.close()
    
    return result
