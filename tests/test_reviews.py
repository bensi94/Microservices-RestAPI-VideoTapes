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

#User

def test_post_review_invalid_user():
    "Tries to Post invalid user review to the database"
    print("TESTING POST URL: /users/1000/reviews/1?rating=10")

    data = {
        'rating': 10
    }

    url = 'http://rest_api_service/users/1000/reviews/1'
    post_resp = requests.post(url, params=data)

    assert post_resp.status_code == 404
    assert post_resp.text == 'User ID does not exist!'

def test_post_review_invalid_tape():
    "Tries to Post invalid tape to the database"
    print("TESTING POST URL: /users/1/reviews/1000?rating=10")

    data = {
        'rating': 10
    }

    url = 'http://rest_api_service/users/1/reviews/10000'
    post_resp = requests.post(url, params=data)

    assert post_resp.status_code == 404
    assert post_resp.text == 'Tape ID does not exist!'

def test_post_review_invalid_rating():
    "Tries to post invalid rating to the database"
    print("TESTING POST URL: /users/1/reviews/1")

    url = 'http://rest_api_service/users/1/reviews/1'
    post_resp = requests.post(url)

    assert post_resp.status_code == 400
    assert post_resp.text == 'Invalid review!, rating has to be an integer between 1 and 10!'

def test_post_review_invalid_rating100():
    "Tries to Post invalid rating to the database"
    print("TESTING POST URL: /users/1/reviews/1?rating=100")

    data = {
        'rating': 100
    }

    url = 'http://rest_api_service/users/1/reviews/1'
    post_resp = requests.post(url, params=data)

    assert post_resp.status_code == 400
    assert post_resp.text == 'Invalid review!, rating has to be an integer between 1 and 10!'

def test_post_valid_review():
    "Posts valid review to the database"
    print("TESTING POST URL: /users/1/reviews/1?rating=10")

    data = {
        'rating': 10
    }

    url = 'http://rest_api_service/users/1/reviews/1'
    post_resp = requests.post(url, params=data)

    expected_resp = {
        'rating': 10,
        'user_id': 1, 
        'tape_id': 1, 
        'id': 1
    }

    assert post_resp.status_code == 200
    assert post_resp.json() == expected_resp

def test_post_same_review():
    "Posts valid review to the database"
    print("TESTING POST URL: /users/1/reviews/1?rating=10")

    data = {
        'rating': 10
    }

    url = 'http://rest_api_service/users/1/reviews/1'
    post_resp = requests.post(url, params=data)

    data = {
        'rating': 1
    }

    url = 'http://rest_api_service/users/1/reviews/1'
    post_resp = requests.post(url, params=data)

    assert post_resp.status_code == 400
    assert post_resp.text == 'Review already exist for this tape'

def test_get_9():
    populate_tests()
    "Gets reviews by user number 9"
    print("Testing GET URL: /users/9/reviews")

    url = 'http://rest_api_service/users/9/reviews'
    get_resp = requests.get(url)

    assert get_resp.status_code == 200
    assert len(get_resp.json()['Reviews']) == 8

def test_get_1():
    populate_tests()
    "Gets reviews by user number 1"
    print("Testing GET URL: /users/1/reviews")

    url = 'http://rest_api_service/users/1/reviews'
    get_resp = requests.get(url)

    response = {
        'id': 1,
        'name': 'Astra Dable',
        'email': 'adable0@pinterest.com',
        'phone': '755 123 8601',
        'address': '67699 Oakridge Road',
        'Reviews': 'No review for this user'
    }

    assert get_resp.status_code == 200
    assert get_resp.json() == response


def test_get_2():
    populate_tests()
    "Gets reviews by user number 2"
    print("Testing GET URL: /users/2/reviews")

    url = 'http://rest_api_service/users/2/reviews'
    get_resp = requests.get(url)

    response = {
        'id': 2,
        'name': 'Man Doy',
        'email': 'mdoy1@yahoo.co.jp',
        'phone': '186 378 5698',
        'address': '019 Mesta Park',
        'Reviews': [
            {
                'id': 1,
                'title': 'Adaptive 24/7 parallelism',
                'director': 'Melony Kearley',
                'type': 'Betamax',
                'release_date': '1999-09-23T00:00:00',
                'eidr': '10.5240/FFFF-EFDF-EEED-DEEE-EFFF-C',
                'rating': 10
            }
        ]
    }

    assert get_resp.status_code == 200
    assert get_resp.json() == response


def test_get_2_single():
    populate_tests()
    "Gets reviews by user number 2 on tape number 1"
    print("Testing GET URL: /users/2/reviews/1")

    url = 'http://rest_api_service/users/2/reviews/1'
    get_resp = requests.get(url)

    response = {
        'id': 2,
        'name': 'Man Doy',
        'email': 'mdoy1@yahoo.co.jp',
        'phone': '186 378 5698',
        'address': '019 Mesta Park',
        'Review': {
                'id': 1,
                'title': 'Adaptive 24/7 parallelism',
                'director': 'Melony Kearley',
                'type': 'Betamax',
                'release_date': '1999-09-23T00:00:00',
                'eidr': '10.5240/FFFF-EFDF-EEED-DEEE-EFFF-C',
                'rating': 10
            }
    }

    assert get_resp.status_code == 200
    assert get_resp.json() == response

def test_put_invalid():
    populate_tests()
    "Puts new rating on reveiw by user number 2 tape number 1"
    print("Testing PUT URL: /users/2/reviews/1?rating=100")

    data = {
        'rating': 100
    }

    url = 'http://rest_api_service/users/2/reviews/1'
    put_resp = requests.put(url, params=data)

    assert put_resp.status_code == 400
    assert put_resp.text == 'Invalid review!, rating has to be an integer between 1 and 10!'

    
def test_put_valid():
    populate_tests()
    "Puts new rating on reveiw by user number 2 tape number 1"
    print("Testing PUT URL: /users/2/reviews/1?rating=5")

    data = {
        'rating': 5
    }

    url = 'http://rest_api_service/users/2/reviews/1'
    put_resp = requests.put(url, params=data)

    response = {
        'rating': '5',
        'user_id': 2,
        'tape_id': 1,
        'id': 1
    }

    assert put_resp.status_code == 200
    assert put_resp.json() == response


def test_delete():
    populate_tests()
    "Deletes review by user 2 on tape 1"
    print("Testing DELETE URL: /users/2/reviews/1")

    url = 'http://rest_api_service/users/2/reviews/1'
    delete_resp = requests.delete(url)

    get_resp = requests.get(url)

    response = {
        'id': 2,
        'name': 'Man Doy',
        'email': 'mdoy1@yahoo.co.jp',
        'phone': '186 378 5698',
        'address': '019 Mesta Park',
        'Review': 'No review for this tape for this user'
    }

    assert delete_resp.status_code == 200
    assert delete_resp.text == 'Review with user ID:2 and tape ID:1 deleted'
    assert get_resp.json() == response



# Tape
def test_get_tape_reviews():
    populate_tests()
    "Gets reviews on tape number 1"
    print("Testing GET URL: /tapes/1/reviews")

    url = 'http://rest_api_service/tapes/1/reviews'
    get_resp = requests.get(url)

    assert get_resp.status_code == 200
    assert len(get_resp.json()) == 8

def test_get_all_reviews():
    populate_tests()
    "Gets reviews on tapes"
    print("Testing GET URL: /tapes/reviews")

    url = 'http://rest_api_service/tapes/reviews'
    get_resp = requests.get(url)

    assert get_resp.status_code == 200
    assert len(get_resp.json()) == 36

def test_get_tape_no():
    populate_tests()
    "Gets new rating on reveiw by tape number 2 tape user 1"
    print("Testing GET URL: /tapes/2/reviews/1")

 
    url = 'http://rest_api_service/tapes/2/reviews/1'
    get_resp = requests.get(url)

    response = {
        'id': 1,
        'name': 'Astra Dable',
        'email': 'adable0@pinterest.com',
        'phone': '755 123 8601',
        'address': '67699 Oakridge Road',
        'Review': 'No review for this tape for this user'
    }   

    assert get_resp.status_code == 200
    assert get_resp.json() == response


## Utils
# Adds few reviews to the database
def populate_tests():
    data = {
        'rating': 10
    }
    for i in range(1, 10):
        for j in range(1, i):
            url = 'http://rest_api_service/users/' + str(i) + '/reviews/' + str(j)
            requests.post(url, params=data)

 
