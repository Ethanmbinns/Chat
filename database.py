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
        
        # Create threads table
        cursor.execute('''
        CREATE TABLE threads (
            uuid TEXT PRIMARY KEY,
            user_uuid TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_uuid) REFERENCES accounts(uuid)
        )
        ''')
        
        # Create messages table
        cursor.execute('''
        CREATE TABLE messages (
            uuid TEXT PRIMARY KEY,
            thread_uuid TEXT NOT NULL,
            user_message TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (thread_uuid) REFERENCES threads(uuid)
        )
        ''')
        
        conn.commit()
        conn.close()
        print(f"Database {DB_PATH} created successfully.")
    else:
        # Check if our tables exist, and if not, create them
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if threads table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='threads'")
        if not cursor.fetchone():
            cursor.execute('''
            CREATE TABLE threads (
                uuid TEXT PRIMARY KEY,
                user_uuid TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_uuid) REFERENCES accounts(uuid)
            )
            ''')
            print("Threads table created.")
        
        # Check if messages table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
        if not cursor.fetchone():
            cursor.execute('''
            CREATE TABLE messages (
                uuid TEXT PRIMARY KEY,
                thread_uuid TEXT NOT NULL,
                user_message TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (thread_uuid) REFERENCES threads(uuid)
            )
            ''')
            print("Messages table created.")
            
        conn.commit()
        conn.close()
        print(f"Database {DB_PATH} already exists, ensured all tables are present.")

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