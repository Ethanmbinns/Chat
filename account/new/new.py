from flask import Blueprint, jsonify
import uuid
from database import initialize_database, execute_query

# Create a blueprint for account/new endpoint
account_new_bp = Blueprint('account_new', __name__)

def generate_unique_uuid():
    """
    Generate a UUID and check if it already exists in the database.
    If it does, generate a new one until a unique UUID is found.
    """
    while True:
        # Generate a new UUID
        new_uuid = str(uuid.uuid4())
        
        # Check if it exists in the database
        result = execute_query(
            "SELECT uuid FROM accounts WHERE uuid = ?", 
            (new_uuid,), 
            fetch_one=True
        )
        
        # If the UUID is unique, add it to the database and return it
        if result is None:
            execute_query(
                "INSERT INTO accounts (uuid) VALUES (?)", 
                (new_uuid,)
            )
            return new_uuid

@account_new_bp.route('/new', methods=['POST'])
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
