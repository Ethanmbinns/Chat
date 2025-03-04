# UUID Account Generator API Documentation

## Project Overview

The UUID Account Generator API is a lightweight Flask-based RESTful service designed to generate and manage unique identifiers for account creation. It provides a reliable way to create universally unique identifiers (UUIDs) while ensuring no duplicates exist in the system.

### Key Features

- Generation of unique UUIDs for new accounts
- Persistence of UUIDs in SQLite database
- Automatic database initialization
- Modular and extensible architecture

## API Reference

### Endpoints

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

## Database Schema

### Tables

#### accounts

| Column Name | Type | Description |
|-------------|------|-------------|
| uuid | TEXT | Primary key, the generated UUID |
| created_at | TIMESTAMP | When the UUID was created, auto-generated |

## Setup & Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Local Development Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. The API will be available at http://127.0.0.1:5000
