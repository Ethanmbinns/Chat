# UUID Account Generator API

A Flask REST API for generating unique UUIDs for new accounts.

## Project Structure

```
project_root/
├── app.py                 # Main entry point and route definitions
├── config.py              # Configuration settings
├── database.py            # Database utilities
├── account/
│   ├── __init__.py        # Makes account a package
│   └── new/
│       ├── __init__.py    # Makes new a package
│       └── new.py         # Implementation for account/new endpoint
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

2. Run the application:
   ```
   python app.py
   ```

## API Endpoints

- `POST /account/new` - Create a new account and receive a UUID

## Documentation

For comprehensive documentation, see the docs/ directory.
