import pytest
from app import app
import json
import uuid
import unittest.mock as mock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_openai():
    # Mock the openai API call
    with mock.patch('openai.ChatCompletion.create') as mock_create:
        # Create a mock response structure
        mock_response = mock.MagicMock()
        mock_response.choices = [mock.MagicMock()]
        mock_response.choices[0].message.content = "This is a mock AI response"
        mock_create.return_value = mock_response
        yield mock_create

def test_new_message(client, mock_openai):
    # First create a user account
    account_response = client.post('/account/new')
    account_data = json.loads(account_response.data)
    user_uuid = account_data['uuid']
    
    # Now test the chat message endpoint
    response = client.post('/chat/new-message', 
                           json={
                               'user_uuid': user_uuid,
                               'message': 'Hello, AI!'
                           },
                           content_type='application/json')
    
    # Check that the response is successful
    assert response.status_code == 201
    
    # Parse the response data
    data = json.loads(response.data)
    
    # Check that we got the expected fields
    assert 'response' in data
    assert 'thread_uuid' in data
    assert 'message_uuid' in data
    assert 'is_new_thread' in data
    
    # Check that it's a new thread
    assert data['is_new_thread'] == True
    
    # Check that we got the mock response
    assert data['response'] == "This is a mock AI response"
    
    # Try sending another message to the same thread
    thread_uuid = data['thread_uuid']
    response2 = client.post('/chat/new-message', 
                           json={
                               'user_uuid': user_uuid,
                               'message': 'Second message',
                               'thread_uuid': thread_uuid
                           },
                           content_type='application/json')
    
    # Check that the response is successful
    assert response2.status_code == 201
    
    # Parse the response data
    data2 = json.loads(response2.data)
    
    # Check that we're using the same thread
    assert data2['thread_uuid'] == thread_uuid
    assert data2['is_new_thread'] == False

def test_new_message_invalid_user(client):
    # Test with an invalid user UUID
    invalid_uuid = str(uuid.uuid4())  # Generate a random UUID that won't be in the database
    
    response = client.post('/chat/new-message', 
                          json={
                              'user_uuid': invalid_uuid,
                              'message': 'Hello, AI!'
                          },
                          content_type='application/json')
    
    # Check that we get a 404 error
    assert response.status_code == 404
    
    # Parse the response data
    data = json.loads(response.data)
    
    # Check the error message
    assert 'error' in data
    assert 'Invalid user_uuid' in data['error']

def test_new_message_invalid_thread(client):
    # First create a user account
    account_response = client.post('/account/new')
    account_data = json.loads(account_response.data)
    user_uuid = account_data['uuid']
    
    # Test with an invalid thread UUID
    invalid_thread = str(uuid.uuid4())  # Generate a random UUID that won't be in the database
    
    response = client.post('/chat/new-message', 
                          json={
                              'user_uuid': user_uuid,
                              'message': 'Hello, AI!',
                              'thread_uuid': invalid_thread
                          },
                          content_type='application/json')
    
    # Check that we get a 404 error
    assert response.status_code == 404
    
    # Parse the response data
    data = json.loads(response.data)
    
    # Check the error message
    assert 'error' in data
    assert 'Invalid thread_uuid' in data['error']

def test_new_message_missing_parameters(client):
    # Test with missing user_uuid
    response = client.post('/chat/new-message', 
                          json={
                              'message': 'Hello, AI!'
                          },
                          content_type='application/json')
    
    # Check that we get a 400 error
    assert response.status_code == 400
    
    # Test with missing message
    response = client.post('/chat/new-message', 
                          json={
                              'user_uuid': str(uuid.uuid4())
                          },
                          content_type='application/json')
    
    # Check that we get a 400 error
    assert response.status_code == 400