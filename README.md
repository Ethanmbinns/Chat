# UUID Account Generator and Chat API

A Flask REST API for generating unique UUIDs for new accounts and providing AI-powered chat functionality.

## Project Structure

```
project_root/
├── app.py                 # Main entry point and route definitions
├── config.py              # Configuration settings
├── database.py            # Database utilities
├── account/               # Account-related endpoints
│   ├── __init__.py        # Makes account a package
│   └── new/
│       ├── __init__.py    # Makes new a package
│       └── new.py         # Implementation for account/new endpoint
├── chat/                  # Chat-related endpoints
│   ├── __init__.py        # Makes chat a package
│   └── new_message/
│       ├── __init__.py    # Makes new_message a package
│       └── new_message.py # Implementation for chat/new-message endpoint
├── middleware/            # For request handling middleware
├── services/              # Business logic services
├── models/                # Data models
├── utils/                 # Utility functions and classes
├── config/                # Configuration management
├── tests/                 # Test suite
└── docs/                  # Documentation
```

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set your OpenAI API key:
   ```
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. Run the application:
   ```
   python app.py
   ```

## API Endpoints

- `POST /account/new` - Create a new account and receive a UUID
- `POST /chat/new-message` - Send a message to the AI and get a response

## Documentation

For comprehensive documentation, see the docs/ directory.