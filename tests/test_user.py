from utils import delete_all_db, init_database
import pytest
import time
import requests
import json

@pytest.fixture()
def resource():
    print("setup")
    init_database()
    yield
    delete_all_db()


def test_get_1():
    "GET request to url returns a 200"
    url = 'http://rest_api_service/users/1'
    resp = requests.get(url)

    test_dict = {
        'id': 1, 
        'name': 'Astra Dable', 
        'email': 
        'adable0@pinterest.com',
        'phone': '755 123 8601', 
        'address': '67699 Oakridge Road' 
        }
    
    assert resp.json() == test_dict
    assert resp.status_code == 200
