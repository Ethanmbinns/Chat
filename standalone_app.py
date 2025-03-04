from flask import Flask, jsonify
import sqlite3
import uuid
import os.path

app = Flask(__name__)

# Database configuration
DB_NAME = 'accounts.db'

def initialize_database():
    """
    Check if the database exists, and create it if it doesn't.
    """
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
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
        print(f"Database {DB_NAME} created successfully.")
    else:
        print(f"Database {DB_NAME} already exists.")

def generate_unique_uuid():
    """
    Generate a UUID and check if it already exists in the database.
    If it does, generate a new one until a unique UUID is found.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    while True:
        # Generate a new UUID
        new_uuid = str(uuid.uuid4())
        
        # Check if it exists in the database
        cursor.execute("SELECT uuid FROM accounts WHERE uuid = ?", (new_uuid,))
        result = cursor.fetchone()
        
        # If the UUID is unique, add it to the database and return it
        if result is None:
            cursor.execute("INSERT INTO accounts (uuid) VALUES (?)", (new_uuid,))
            conn.commit()
            conn.close()
            return new_uuid

@app.route('/account/new', methods=['POST'])
def create_account():
    """
    Endpoint to create a new account with a unique UUID.
    """
    # Ensure database exists
    initialize_database()
    
    # Generate a unique UUID
    new_uuid = generate_unique_uuid()
    
    # Return the new UUID
    return jsonify({"uuid": new_uuid}), 201

@app.route('/', methods=['GET'])
def index():
    """
    Basic route for testing the API
    """
    return "UUID Account Generator API is running"

if __name__ == '__main__':
    app.run(debug=True)
