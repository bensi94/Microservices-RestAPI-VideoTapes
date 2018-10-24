import pytest
import requests
import json
from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG


## Alwasy happens before and after each test
@pytest.fixture(autouse=True)
def run_around_tests():
    with ClusterRpcProxy(CONFIG) as rpc:
        rpc.database_service.delete_and_populate()
   #yield
 
# Testing user get
def test_get_all():
    "Gets all users from the database and tests the length of the response"
    print("TESTING GET URL: /users")

    url = 'http://rest_api_service/users'
    resp = requests.get(url)

    assert resp.status_code == 200
    assert len(resp.json()) == 100

def test_get_1():
    "Gets user with id 1 from the database"
    print("TESTING GET URL: /users/1")

    url = 'http://rest_api_service/users/1'
    resp = requests.get(url)

    test_dict = {
        'id': 1, 
        'name': 'Astra Dable', 
        'email': 'adable0@pinterest.com',
        'phone': '755 123 8601', 
        'address': '67699 Oakridge Road' 
        }
    
    assert resp.json() == test_dict
    assert resp.status_code == 200

def test_get_56():
    "Gets user with id 56 from the database"
    print("TESTING GET URL: /users/56")

    url = 'http://rest_api_service/users/56'
    resp = requests.get(url)

    test_dict = {
        'id': 56, 
        'name': 'Barbara Fleckney', 
        'email': 'bfleckney1j@live.com', 
        'phone': '400 588 8725', 
        'address': '997 7th Point'
        }
    
    assert resp.json() == test_dict
    assert resp.status_code == 200

def test_get_invalid():
    "Gets invalid user from the database"
    print("TESTING GET URL: /users/1000")

    url = 'http://rest_api_service/users/1000'
    resp = requests.get(url)

    assert resp.text == 'User not found!'
    assert resp.status_code == 404

# Testing user post
def test_post_invalid_name():
    "Posts invalid user and returns error"
    print("TESTING POST URL: /users")

    url = 'http://rest_api_service/users'
    resp = requests.post(url)

    assert resp.status_code == 400
    assert resp.text == 'Name is required'

def test_post_invalid_email():
    "Posts invalid email and returns error"
    print("TESTING POST URL: /users?name=Bensi&email=blala&phone=5812345&address=Menntavegur 1")

    data = {
        'name': 'Bensi',
        'email': 'blala',
        'phone': '5812345',
        'address': 'Menntavegur 1'
    }
    url = 'http://rest_api_service/users'
    resp = requests.post(url, params=data)


    assert resp.status_code == 400
    assert resp.text == 'Invalid email format.'

def test_post_invalid_phone():
    "Posts invalid phone and returns error"
    print("TESTING POST URL: /users?name=Bensi&email=bensi@bensi.is&phone=blala&address=Menntavegur 1")

    data = {
        'name': 'Bensi',
        'email': 'bensi@bensi.is',
        'phone': 'blala',
        'address': 'Menntavegur 1'
    }
    url = 'http://rest_api_service/users'
    resp = requests.post(url, params=data)

    assert resp.status_code == 400
    assert resp.text == 'Invalid phone number format'
 
def test_post_bensi():
    "Posts valid users and checks response and database after"
    print("TESTING POST URL: /users?name=Bensi&email=bensi@bensi.is&phone=5812345&address=Menntavegur 1")

    data = {
        'name': 'Bensi',
        'email': 'bensi@bensi.is',
        'phone': '5812345',
        'address': 'Menntavegur 1'
    }
    url = 'http://rest_api_service/users'
    pots_resp = requests.post(url, params=data)

    data['id'] = 101

    # Get is used to get check if the post went into the database
    url = 'http://rest_api_service/users'
    get_resp = requests.get(url)

    assert get_resp.status_code == 200
    assert len(get_resp.json()) == 101
    assert pots_resp.status_code == 200
    assert pots_resp.json() == data

# Testing user put
def test_put_invalid():
    "Tests put  invalid user and returns error"
    print("TESTING PUT URL: /users/1000?name=Bensi&email=bensi@bensi.is&phone=5812345&address=Menntavegur 1")

    data = {
        'name': 'Bensi',
        'email': 'bensi@bensi.is',
        'phone': '5812345',
        'address': 'Menntavegur 1'
    }
    url = 'http://rest_api_service/users/1000'
    pots_resp = requests.put(url, params=data)

    assert pots_resp.status_code == 400
    assert pots_resp.text == 'User ID does not exist'

def test_put_invalid_email():
    "Put invalid email and returns error"
    print("TESTING PUT URL: /users/1?name=Bensi&email=blala&phone=5812345&address=Menntavegur 1")

    data = {
        'name': 'Bensi',
        'email': 'blala',
        'phone': '5812345',
        'address': 'Menntavegur 1'
    }
    url = 'http://rest_api_service/users/1'
    resp = requests.put(url, params=data)

    assert resp.status_code == 400
    assert resp.text == 'Invalid email format.'

def test_put_invalid_phone():
    "Put invalid phone and returns error"
    print("TESTING PUT URL: /users/1?name=Bensi&email=bensi@bensi.is&phone=blala&address=Menntavegur 1")

    data = {
        'name': 'Bensi',
        'email': 'bensi@bensi.is',
        'phone': 'blala',
        'address': 'Menntavegur 1'
    }
    url = 'http://rest_api_service/users/1'
    resp = requests.put(url, params=data)

    assert resp.status_code == 400
    assert resp.text == 'Invalid phone number format'

def test_put_bensi():
    "Tests put  on valid user id"
    print("TESTING PUT URL: /users/1?name=Bensi&email=bensi@bensi.is&phone=5812345&address=Menntavegur 1")

    data = {
        'name': 'Bensi',
        'email': 'bensi@bensi.is',
        'phone': '5812345',
        'address': 'Menntavegur 1'
    }

    url = 'http://rest_api_service/users/1'
    pots_resp = requests.put(url, params=data)

    # Get is used to get check if the put went into the database
    url = 'http://rest_api_service/users/1'
    get_resp = requests.get(url)

    data['id'] = 1

    assert get_resp.status_code == 200
    assert get_resp.json() == data
    assert pots_resp.status_code == 200
    assert pots_resp.json() == data

# Testing user delete
def test_delete_invalid():
    "Tests delete  on invalid user id"
    print("TESTING Delete URL: /users/1000")

    url = 'http://rest_api_service/users/1000'
    delete_response = requests.delete(url)

    assert delete_response.status_code == 400
    assert delete_response.text == 'User ID does not exist'

def test_delete_valid():
    "Tests delete  on valid user id"
    print("TESTING Delete URL: /users/1")

    url = 'http://rest_api_service/users/1'
    delete_response = requests.delete(url)

    # Get is used to get check if the put went into the database
    url = 'http://rest_api_service/users/1'
    get_resp = requests.get(url)


    assert delete_response.status_code == 200
    assert delete_response.text == 'User with ID:1 deleted'
    assert get_resp.status_code == 404
    assert get_resp.text == 'User not found!'

def test_delete_all_users():
    "Tests deleteing all user from the database"
    print("TESTING Delete ALL USERS")

    for i in range (1, 101):
        url = 'http://rest_api_service/users/' + str(i)
        requests.delete(url)
    
    url = 'http://rest_api_service/users'
    resp = requests.get(url)

    assert resp.status_code == 200
    assert len(resp.json()) == 0
