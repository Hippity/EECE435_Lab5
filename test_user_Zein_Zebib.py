import pytest
from databasy import insert_user, delete_user , delete_all_users , get_users , get_user_by_id , update_user

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

@pytest.fixture
def test_db():
    create_fresh_db()
    yield test_db
    delete_all_users()

def test_get_users(test_db):
    users = get_users()
    assert isinstance(users, list)
    print(users)
    assert len(users) == 2
    assert all(isinstance(user, dict) for user in users)
    assert inserted_user_1 == users[0]
    assert inserted_user_2 == users[1]

def test_get_user(test_db):
    user = get_user_by_id(2)
    assert isinstance(user, dict)
    assert inserted_user_2 == user
    # Non existing user
    user = get_user_by_id(3)
    assert isinstance(user, dict)
    assert user == {}

def test_add_user(test_db):
    new_user = {
        'name' : 'John Doe',
        'email' : 'john.d@example.com',
        'phone' : '789-456-1230',
        'address' : '123 Grape St, Grapeville',
        'country' : 'USA'
    }
    added_user = insert_user(new_user)
    assert isinstance(new_user, dict)
    new_user['user_id'] = 3
    assert added_user == new_user

def test_update_user(test_db):
    # Add new user
    new_user = {
        'name' : 'John Doe',
        'email' : 'john.d@example.com',
        'phone' : '789-456-1230',
        'address' : '123 Grape St, Grapeville',
        'country' : 'USA'
    }
    added_user = insert_user(new_user)
    assert isinstance(new_user, dict)
    new_user['user_id'] = 3
    assert added_user == new_user
    # Update user
    added_user['address'] = '123 Melon St, Melonville'
    updated_user = update_user(added_user)
    assert isinstance(new_user, dict)
    assert added_user == updated_user
    # Non existing user
    added_user['user_id'] = 4
    updated_user = update_user(added_user)
    assert isinstance(new_user, dict)
    assert updated_user == {}

def test_delete_user(test_db):
    user_id = 1
    msg = delete_user(user_id)
    assert 'User deleted successfully' == msg['status']
    user_id = 3
    msg = delete_user(user_id)
    assert 'Cannot delete user' == msg['status']
