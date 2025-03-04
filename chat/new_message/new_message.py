from flask import Blueprint, jsonify, request
import openai
import uuid
from database import initialize_database, execute_query

# Create a blueprint for chat/new-message endpoint
chat_new_message_bp = Blueprint('chat_new_message', __name__)

def get_ai_response(message):
    """
    Send a message to OpenAI API and get a response.
    
    Args:
        message (str): The user's message
        
    Returns:
        str: The AI response from OpenAI
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can change the model as needed
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        # Log the error (in a production environment)
        print(f"Error calling OpenAI API: {str(e)}")
        return "I'm sorry, I couldn't process your request at this time."

def create_new_thread(user_uuid):
    """
    Create a new thread for a user.
    
    Args:
        user_uuid (str): The UUID of the user
        
    Returns:
        str: The UUID of the new thread
    """
    # Check if user exists
    user_exists = execute_query(
        "SELECT uuid FROM accounts WHERE uuid = ?",
        (user_uuid,),
        fetch_one=True
    )
    
    if not user_exists:
        return None
    
    # Generate a new UUID for the thread
    thread_uuid = str(uuid.uuid4())
    
    # Create the thread in the database
    execute_query(
        "INSERT INTO threads (uuid, user_uuid) VALUES (?, ?)",
        (thread_uuid, user_uuid)
    )
    
    return thread_uuid

def save_message(thread_uuid, user_message, ai_response):
    """
    Save a message and its response to the database.
    
    Args:
        thread_uuid (str): The UUID of the thread
        user_message (str): The user's message
        ai_response (str): The AI's response
        
    Returns:
        str: The UUID of the message
    """
    # Generate a new UUID for the message
    message_uuid = str(uuid.uuid4())
    
    # Save the message and response to the database
    execute_query(
        "INSERT INTO messages (uuid, thread_uuid, user_message, ai_response) VALUES (?, ?, ?, ?)",
        (message_uuid, thread_uuid, user_message, ai_response)
    )
    
    return message_uuid

@chat_new_message_bp.route('/new-message', methods=['POST'])
def new_message():
    """
    Endpoint to create a new chat message and get an AI response.
    
    Required JSON parameters:
    - user_uuid: The UUID of the user
    - message: The user's message
    
    Optional JSON parameters:
    - thread_uuid: The UUID of an existing thread (if continuing a conversation)
    
    Returns:
        JSON with the AI response and thread information
    """
    # Ensure database exists with all required tables
    initialize_database()
    
    # Get data from the request
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Check for required fields
    if 'user_uuid' not in data:
        return jsonify({"error": "Missing user_uuid parameter"}), 400
    
    if 'message' not in data:
        return jsonify({"error": "Missing message parameter"}), 400
    
    user_uuid = data['user_uuid']
    user_message = data['message']
    
    # Check if the user exists
    user_exists = execute_query(
        "SELECT uuid FROM accounts WHERE uuid = ?",
        (user_uuid,),
        fetch_one=True
    )
    
    if not user_exists:
        return jsonify({"error": "Invalid user_uuid"}), 404
    
    # Get or create a thread
    thread_uuid = data.get('thread_uuid')
    is_new_thread = False
    
    if not thread_uuid:
        # Create a new thread
        thread_uuid = create_new_thread(user_uuid)
        is_new_thread = True
    else:
        # Verify the thread exists and belongs to this user
        thread_exists = execute_query(
            "SELECT uuid FROM threads WHERE uuid = ? AND user_uuid = ?",
            (thread_uuid, user_uuid),
            fetch_one=True
        )
        
        if not thread_exists:
            return jsonify({"error": "Invalid thread_uuid or thread doesn't belong to this user"}), 404
    
    # Get AI response from OpenAI
    ai_response = get_ai_response(user_message)
    
    # Save the message and response to the database
    message_uuid = save_message(thread_uuid, user_message, ai_response)
    
    # Prepare and return the response
    response_data = {
        "response": ai_response,
        "thread_uuid": thread_uuid,
        "message_uuid": message_uuid,
        "is_new_thread": is_new_thread
    }
    
    return jsonify(response_data), 201