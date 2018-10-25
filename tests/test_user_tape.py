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

# Testing get all tapes that user has on loan
def test_get_tapes_96():
    "Gets all tapes that a certain user has on loan and tests the length of the response"
    print("TESTING GET URL: /users/96/tapes")

    url = 'http://rest_api_service/users/96/tapes'
    resp = requests.get(url)

    assert resp.status_code == 200
    assert len(resp.json()) == 2

def test_get_tapes_8():
    "Gets all tapes that a certain user has on loan and tests the length of the response"
    print("TESTING GET URL: /users/8/tapes")

    url = 'http://rest_api_service/users/8/tapes'
    resp = requests.get(url)

    assert resp.text == 'User has no tapes on loan'
    assert resp.status_code == 404

def test_get_tapes_2():
    "Gets all tapes that a certain user has on loan and tests the length of the response"
    print("TESTING GET URL: /users/2/tapes")

    url = 'http://rest_api_service/users/2/tapes'
    resp = requests.get(url)

    assert resp.status_code == 200
    assert len(resp.json()) == 1

def test_get_invalid_user_tapes():
    "Gets invalid user tapes from the database"
    print("TESTING GET URL: /users/1000/tapes")

    url = 'http://rest_api_service/users/1000/tapes'
    resp = requests.get(url)

    assert resp.text == 'There is no user with this ID.'
    assert resp.status_code == 400

def test_return_valid_tape():
    "Tests returning a valid tape"
    print("TESTING Delete URL: /users/10/tapes/7")

    url = 'http://rest_api_service/users/10/tapes/7'
    delete_response = requests.delete(url)

    assert delete_response.status_code == 200
    assert delete_response.text == 'Tape has been returned'

def test_return_invalid_tape():
    "Tests returning an invalid tape"
    print("TESTING Delete URL: /users/10/tapes/1001")

    url = 'http://rest_api_service/users/10/tapes/1001'
    delete_response = requests.delete(url)

    
    assert delete_response.status_code == 400
    assert delete_response.text == 'The user with this ID does not have tape on loan with this ID.'

def test_update_valid_borrow():
    "Tests updating a registration"
    print("TESTING PUT URL: /users/96/tapes/35?borrow_date=2000-10-10&return_date=2010-10-10")

    data = {
        'borrow_date': '2000-10-10',
        'return_date': '2010-10-10',
    }

    url = 'http://rest_api_service/users/96/tapes/35'
    put_resp = requests.put(url, params=data)
    
    assert put_resp.status_code == 200
    assert put_resp.text == 'Registration has been updated.'

def test_update_invalid_borrow():
    "Tests updating an invalid registration"
    print("TESTING PUT URL: /users/24/tapes/10?borrow_date=asdf&return_date=2010-10-10")

    data = {
        'borrow_date': 'asdf',
        'return_date': '2010-10-10',
    }

    url = 'http://rest_api_service/users/24/tapes/10'
    put_resp = requests.put(url, params=data)
    
    assert put_resp.status_code == 400
    assert put_resp.text == 'Invalid date format for borrow_date'

def test_post_valid_tape_to_user():
    "Tests posting a tape to user's list of tapes on loan"
    print("TESTING POST URL: /users/5/tapes/17")

    url = 'http://rest_api_service/users/5/tapes/17'

    post_resp = requests.post(url)

    assert post_resp.status_code == 200

def test_post_invalid_tape_to_user():
    "Tests posting an invalid tape to user's list of tapes on loan"
    print("TESTING POST URL: /users/51/tapes/19")

    url = 'http://rest_api_service/users/51/tapes/19'

    post_resp = requests.post(url)

    assert post_resp.status_code == 400
    assert post_resp.text == 'This user already has this tape or loan or has rented it before.'