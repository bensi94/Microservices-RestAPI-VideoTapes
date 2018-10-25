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


# Testing tape get
def test_get_all():
    "Gets all tapes from the database and tests the length of the response"
    print("TESTING GET URL: /tapes")

    url = 'http://rest_api_service/tapes'
    resp = requests.get(url)

    assert resp.status_code == 200
    assert len(resp.json()) == 1000

def test_get_1():
    "Gets tape with id 1 from the database"
    print("TESTING GET URL: /tapes/1")

    url = 'http://rest_api_service/tapes/1'
    resp = requests.get(url)

    test_dict = {
        'id': 1,
        'title': 'Adaptive 24/7 parallelism',
        'director': 'Melony Kearley',
        'type': 'Betamax',
        'release_date': '1999-09-23T00:00:00',
        'eidr': '10.5240/FFFF-EFDF-EEED-DEEE-EFFF-C'
    }

    assert resp.json() == test_dict
    assert resp.status_code == 200

def test_get_invalid():
    "Gets invalid tape from the database"
    print("TESTING GET URL: /tapes/2000")

    url = 'http://rest_api_service/tapes/2000'
    resp = requests.get(url)

    assert resp.text == 'Tape not found!'
    assert resp.status_code == 404

# Testing tape post
def test_post_invalid_title():
    "Posts invalid tape and returns error"
    print("TESTING POST URL: /tapes")

    url = 'http://rest_api_service/tapes'
    resp = requests.post(url)

    assert resp.status_code == 400
    assert resp.text == 'Title is required'

def test_post_invalid_date():
    "Posts tape with invalid date"
    print("TESTING POST URL: /tapes?title=Everest&director=Baltasar Kormákur&type=Betamax&release_date=2015-10-300&eidr=10.5240/7900-4D22-79BF-AC9C-AE6D-L")
    data = {
        'title': 'Everest',
        'director': 'Baltasar Kormákur',
        'type': 'Betamax',
        'release_date': '2015-10-300',
        'eidr': '10.5240/7900-4D22-79BF-AC9C-AE6D-L'
    }

    url = 'http://rest_api_service/tapes'
    resp = requests.post(url, params=data)

    assert resp.status_code == 400
    assert resp.text == 'Invalid date'

def test_post_invalid_edir():
    "Posts tape with invalid eidr"
    print("TESTING POST URL: / tapes?title=Everest & director=Baltasar Kormákur & type=Betamax & release_date=2015-10-30 & eidr=sdfsa")
    data = {
        'title': 'Everest',
        'director': 'Baltasar Kormákur',
        'type': 'Betamax',
        'release_date': '2015-10-30',
        'eidr': 'sdfsa'
    }

    url = 'http://rest_api_service/tapes'
    resp = requests.post(url, params=data)

    assert resp.status_code == 400
    assert resp.text == 'Invalid eidr'

def test_post_everest():
    "Posts valid tape"
    print("TESTING POST URL: /tapes?title=Everest&director=Baltasar Kormákur&type=Betamax&release_date=2015-10-30&eidr=10.5240/7900-4D22-79BF-AC9C-AE6D-L")
   
    data = {
        'title': 'Everest',
        'director': 'Baltasar Kormákur',
        'type': 'Betamax',
        'release_date': '2015-10-30',
        'eidr': '10.5240/7900-4D22-79BF-AC9C-AE6D-L'
    }

    url = 'http://rest_api_service/tapes'
    post_resp = requests.post(url, params=data)

    # Get is used to get check if the put went into the database
    url = 'http://rest_api_service/tapes/1001'
    get_resp = requests.get(url)

    data['id'] = 1001
    data['release_date'] = '2015-10-30T00:00:00'

    assert get_resp.status_code == 200
    assert get_resp.json() == data
    assert post_resp.status_code == 200
    assert post_resp.json() == data

def test_post_eidr_already():
    "Posts valid tape and then tries to post the same tape"
    print("TESTING POST URL TWICE: /tapes?title=Everest&director=Baltasar Kormákur&type=Betamax&release_date=2015-10-30&eidr=10.5240/7900-4D22-79BF-AC9C-AE6D-L")
   
    data = {
        'title': 'Everest',
        'director': 'Baltasar Kormákur',
        'type': 'Betamax',
        'release_date': '2015-10-30',
        'eidr': '10.5240/7900-4D22-79BF-AC9C-AE6D-L'
    }

    url = 'http://rest_api_service/tapes'
    post_resp = requests.post(url, params=data)

    url = 'http://rest_api_service/tapes'
    post_resp = requests.post(url, params=data)

    assert post_resp.status_code == 400
    assert post_resp.text == 'Edir already exists'

# Testing tape put
def test_put_invalid_title():
    "Put invalid tape and returns error"
    print("TESTING PUT URL: /tapes/1")

    url = 'http://rest_api_service/tapes/1'
    resp = requests.put(url)

    assert resp.status_code == 400
    assert resp.text == 'Title is required'

def test_put_invalid_date():
    "Posts tape with invalid date"
    print("TESTING PUT URL: /tapes/1?title=Everest&director=Baltasar Kormákur&type=Betamax&release_date=2015-10-30&eidr=10.5240/7900-4D22-79BF-AC9C-AE6D-L")
    data = {
        'title': 'Everest',
        'director': 'Baltasar Kormákur',
        'type': 'Betamax',
        'release_date': '2015-10-300',
        'eidr': '10.5240/7900-4D22-79BF-AC9C-AE6D-L'
    }

    url = 'http://rest_api_service/tapes/1'
    resp = requests.put(url, params=data)

    assert resp.status_code == 400
    assert resp.text == 'Invalid date'

def test_put_invalid_edir():
    "PUT tape with invalid eidr"
    print("TESTING POST URL: /tapes/1?title=Everest & director=Baltasar Kormákur & type=Betamax & release_date=2015-10-30 & eidr=sdfsa")
    data = {
        'title': 'Everest',
        'director': 'Baltasar Kormákur',
        'type': 'Betamax',
        'release_date': '2015-10-30',
        'eidr': 'sdfsa'
    }

    url = 'http://rest_api_service/tapes/1'
    resp = requests.put(url, params=data)

    assert resp.status_code == 400
    assert resp.text == 'Invalid eidr'

def test_put_everest():
    "Put valid tape"
    print("TESTING PUT URL: /tapes/1?title=Everest&director=Baltasar Kormákur&type=Betamax&release_date=2015-10-30&eidr=10.5240/7900-4D22-79BF-AC9C-AE6D-L")

    data = {
        'title': 'Everest',
        'director': 'Baltasar Kormákur',
        'type': 'Betamax',
        'release_date': '2015-10-30',
        'eidr': '10.5240/7900-4D22-79BF-AC9C-AE6D-L'
    }

    url = 'http://rest_api_service/tapes/1'
    post_resp = requests.put(url, params=data)

    # Get is used to get check if the put went into the database
    url = 'http://rest_api_service/tapes/1'
    get_resp = requests.get(url)

    data['id'] = 1
    data['release_date'] = '2015-10-30T00:00:00'

    assert get_resp.status_code == 200
    assert get_resp.json() == data
    assert post_resp.status_code == 200
    assert post_resp.json() == data

def test_put_eidr_already():
    "Posputs valid tape and then tries to post the same tape"
    print("TESTING POST URL TWICE: /tapes/1?title=Everest&director=Baltasar Kormákur&type=Betamax&release_date=2015-10-30&eidr=10.5240/7900-4D22-79BF-AC9C-AE6D-L")

    data = {
        'title': 'Everest',
        'director': 'Baltasar Kormákur',
        'type': 'Betamax',
        'release_date': '2015-10-30',
        'eidr': '10.5240/7900-4D22-79BF-AC9C-AE6D-L'
    }

    url = 'http://rest_api_service/tapes/1'
    post_resp = requests.put(url, params=data)

    url = 'http://rest_api_service/tapes/100'
    post_resp = requests.put(url, params=data)

    assert post_resp.status_code == 400
    assert post_resp.text == 'Edir already exists'

def test_delete_invalid():
    "Tests delete  on invalid tapes id"
    print("TESTING Delete URL: /tapes/2000")

    url = 'http://rest_api_service/tapes/2000'
    delete_response = requests.delete(url)

    assert delete_response.status_code == 400
    assert delete_response.text == 'Tape ID does not exist'

def test_delete_valid():
    "Tests delete  on valid tapes id"
    print("TESTING Delete URL: /tapes/1")

    url = 'http://rest_api_service/tapes/1'
    delete_response = requests.delete(url)

    # Get is used to get check if the put went into the database
    url = 'http://rest_api_service/tapes/1'
    get_resp = requests.get(url)

    assert delete_response.status_code == 200
    assert delete_response.text == 'Tape with ID:1 deleted'
    assert get_resp.status_code == 404
    assert get_resp.text == 'Tape not found!'

def test_delete_all_users():
    "Tests deleteing all tapes from the database"
    print("TESTING Delete ALL TAPES")

    for i in range(1, 1001):
        url = 'http://rest_api_service/tapes/' + str(i)
        requests.delete(url)

    url = 'http://rest_api_service/tapes'
    resp = requests.get(url)

    assert resp.status_code == 200
    assert len(resp.json()) == 0
