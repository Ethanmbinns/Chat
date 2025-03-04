import pytest
from app import app
import json
import uuid

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_account(client):
    # Send a POST request to the endpoint
    response = client.post('/account/new')
    
    # Check that the response is successful
    assert response.status_code == 201
    
    # Parse the response data
    data = json.loads(response.data)
    
    # Check that a UUID was returned
    assert 'uuid' in data
    
    # Check that it's a valid UUID
    try:
        uuid_obj = uuid.UUID(data['uuid'])
        assert True
    except ValueError:
        assert False, "The returned UUID is not valid"
