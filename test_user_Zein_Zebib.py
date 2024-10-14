import pytest
from app import app
from databasy import insert_user, delete_user
import json

# From Flask documentation https://flask.palletsprojects.com/en/3.0.x/tutorial/tests/
@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    user_1 = {
        'name' : 'Alice Johnson',
        'email' : 'alice.j@example.com',
        'phone' : '123-456-7890',
        'address' : '123 Maple St, Cityville',
        'country' : 'USA'
    }
    inserted_user_1 = insert_user(user_1)

    user_2 = {
        'name' : 'Bob Smith',
        'email' : 'bob.s@example.com',
        'phone' : '987-654-3210',
        'address' : '456 Oak Ave, Townsville',
        'country' : 'Canada'
    }
    inserted_user_2 = insert_user(user_2)

    user_3 = {
        'name' : 'Charlie Brown',
        'email' : 'charlie.b@example.com',
        'phone' : '555-123-4567',
        'address' : '789 Pine Blvd, Villagetown',
        'country' : 'UK'
    }
    inserted_user_3 = insert_user(user_3)

    yield client

    delete_user(inserted_user_1['user_id'])
    delete_user(inserted_user_2['user_id'])
    delete_user(inserted_user_3['user_id'])

def test_get_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 3

def test_get_user(client):
    user_id = 1
    response = client.get(f'/api/users/{user_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert 'user_id' in data
    # Check when getting non existent user
    user_id = 5
    response = client.get(f'/api/users/{user_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert 'user_id' not in data

def test_add_user(client):
    new_user = {
        'name' : 'John Doe',
        'email' : 'john.d@example.com',
        'phone' : '789-456-1230',
        'address' : '123 Grape St, Grapeville',
        'country' : 'USA'
    }
    response = client.post('/api/users/add',
                           data=json.dumps(new_user),
                           content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert 'user_id' in data

def test_update_user(client):
    updated_user = {
        'user_id' : 4,
        'name' : 'John Doe',
        'email' : 'john.d@example.com',
        'phone' : '789-456-1230',
        'address' : '123 Melon St, Melonville',
        'country' : 'Canada'
    }
    response = client.put('/api/users/update',
                          data=json.dumps(updated_user),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert 'user_id' in data
    # Check when updating non existent user
    updated_user = {
        'user_id' : 10,
        'name' : 'John Doe',
        'email' : 'john.d@example.com',
        'phone' : '789-456-1230',
        'address' : '123 Melon St, Melonville',
        'country' : 'Canada'
    }
    response = client.put('/api/users/update',
                          data=json.dumps(updated_user),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert 'user_id' not in data

def test_delete_user(client):
    user_id = 4
    response = client.delete(f'/api/users/delete/{user_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'User deleted successfully' == data['status']
    # Check when deleting non existent user
    user_id = 10
    response = client.delete(f'/api/users/delete/{user_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'Cannot delete user' == data['status']


