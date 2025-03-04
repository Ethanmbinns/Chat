# UUID Account Generator and Chat API Documentation

## Project Overview

The UUID Account Generator and Chat API is a lightweight Flask-based RESTful service designed to generate and manage unique identifiers for account creation, and provide chat functionality with AI responses. It provides a reliable way to create universally unique identifiers (UUIDs) while ensuring no duplicates exist in the system.

### Key Features

- Generation of unique UUIDs for new accounts
- AI-powered chat functionality using OpenAI
- Thread-based conversation history tracking
- Persistence of UUIDs, threads, and messages in SQLite database
- Automatic database initialization
- Modular and extensible architecture

## API Reference

### Account Endpoints

#### Create New Account

```
POST /account/new
```

Creates a new account by generating a unique UUID.

**Response**:
- Status Code: 201 Created
- Content Type: application/json
- Body:
  ```json
  {
    "uuid": "550e8400-e29b-41d4-a716-446655440000"
  }
  ```

### Chat Endpoints

#### Create New Message

```
POST /chat/new-message
```

Creates a new chat message, sends it to OpenAI for a response, and stores both in the database.

**Request**:
- Content Type: application/json
- Body:
  ```json
  {
    "user_uuid": "550e8400-e29b-41d4-a716-446655440000",
    "message": "Hello, AI!",
    "thread_uuid": "662f8500-f39c-51e5-b827-556755551111" // Optional, if not provided, a new thread will be created
  }
  ```

**Response**:
- Status Code: 201 Created
- Content Type: application/json
- Body:
  ```json
  {
    "response": "Hello! How can I assist you today?",
    "thread_uuid": "662f8500-f39c-51e5-b827-556755551111",
    "message_uuid": "773e9600-g49d-61f6-c938-667855662222",
    "is_new_thread": false
  }
  ```

## Database Schema

### Tables

#### accounts

| Column Name | Type | Description |
|-------------|------|-------------|
| uuid | TEXT | Primary key, the generated UUID |
| created_at | TIMESTAMP | When the UUID was created, auto-generated |

#### threads

| Column Name | Type | Description |
|-------------|------|-------------|
| uuid | TEXT | Primary key, the generated UUID |
| user_uuid | TEXT | Foreign key to accounts table |
| created_at | TIMESTAMP | When the thread was created, auto-generated |

#### messages

| Column Name | Type | Description |
|-------------|------|-------------|
| uuid | TEXT | Primary key, the generated UUID |
| thread_uuid | TEXT | Foreign key to threads table |
| user_message | TEXT | The message sent by the user |
| ai_response | TEXT | The response from the AI |
| timestamp | TIMESTAMP | When the message was created, auto-generated |

## Setup & Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key (set as environment variable OPENAI_API_KEY)

### Local Development Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set your OpenAI API key: `export OPENAI_API_KEY="your-api-key-here"`
4. Run the application: `python app.py`
5. The API will be available at http://127.0.0.1:5000

## Testing

Run the test suite with pytest:

```
pytest
```