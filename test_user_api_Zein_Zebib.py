import pytest
from app import app
from databasy import insert_user, delete_all_users
import json

def create_fresh_db():
    delete_all_users()
    global inserted_user_1 
    global inserted_user_2
    global inserted_user_3 
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

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            create_fresh_db()
    yield client

def test_api_get_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 3
    assert all(isinstance(user, dict) for user in data)
    assert inserted_user_1 == data[0]
    assert inserted_user_2 == data[1]
    assert inserted_user_3 == data[2]

def test_api_get_user(client):
    user_id = 1
    response = client.get(f'/api/users/{user_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert inserted_user_1 == data
    # Check when getting non existent user
    user_id = 4
    response = client.get(f'/api/users/{user_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert data == {}

def test_api_add_user(client):
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
    new_user['user_id'] = 4
    assert data == new_user

def test_api_update_user(client):
    updated_user = {
        'user_id' : 1,
        'name' : 'Alice Johnson',
        'email' : 'alice.j@example.com',
        'phone' : '123-456-7890',
        'address' : '123 Grape St, Grapeville',
        'country' : 'Canada'
    }
    response = client.put('/api/users/update',
                          data=json.dumps(updated_user),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert data == updated_user
    # Check when updating non existent user
    updated_user = {
        'user_id' : 5,
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
    assert data == {}

def test_api_delete_user(client):
    user_id = 1
    response = client.delete(f'/api/users/delete/{user_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'User deleted successfully' == data['status']
    # Check when deleting non existent user
    user_id = 4
    response = client.delete(f'/api/users/delete/{user_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'Cannot delete user' == data['status']