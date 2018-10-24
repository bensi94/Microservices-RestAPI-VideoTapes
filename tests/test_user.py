import pytest
import time
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


def test_post_invalid_name():
    "Posts invalid user and returns error"
    print("TESTING POST URL: /users")

    url = 'http://rest_api_service/users'
    resp = requests.post(url)

    assert resp.status_code == 400
    assert resp.text == 'Name is required'


def test_post_invalid_email():
    "Posts invalid user and returns error"
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
    "Posts invalid user and returns error"
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
    "Posts invalid user and returns error"
    print("TESTING POST URL: /users?name=Bensi&email=bensi@bensi.is&phone=5812345&address=Menntavegur 1")

    data = {
        'name': 'Bensi',
        'email': 'bensi@bensi.is',
        'phone': '5812345',
        'address': 'Menntavegur 1'
    }
    url = 'http://rest_api_service/users'
    resp = requests.post(url, params=data)

    data['id'] = 101

    assert resp.status_code == 200
    assert resp.json() == data

    

    
