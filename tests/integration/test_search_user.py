
import requests


def test_search_unexistent_user_returns_not_found(base_url, users):

    response = requests.get(base_url + '123456/')
    assert response.status_code == 404


def test_search_registered_user_returns_user_data(base_url, user_andre, user_rafael):

    response = requests.get(base_url + user_rafael.uuid + '/')

    assert response.status_code == 200
    assert response.json() == {
        'uuid': user_rafael.uuid,
        'name': user_rafael.name,
        'email': user_rafael.email,
        'created_at': user_rafael.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    }
