
import json
from datetime import datetime

import requests
from celery.result import AsyncResult


def wait_for_task_execution(client):
    keys = None

    while not keys:
        _, keys = client.scan()

    for key in keys:
        result = AsyncResult(key[17:])
        result.wait()
        assert result.status == 'SUCCESS'


def test_create_user_with_missing_parameters_returns_bad_request(base_url, users):

    headers = {
        'Content-Type': 'application/json',
    }

    payload = {
        'name': 'Bruno Sousa',
    }

    response = requests.post(base_url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 400


def test_create_user_with_success_persists_data_on_celery_task(base_url, users, redis_client):

    headers = {
        'Content-Type': 'application/json',
    }

    payload = {
        'name': 'Bruno Sousa',
        'email': 'bruno.sousa@example.com',
    }

    # Create User
    response = requests.post(base_url, data=json.dumps(payload), headers=headers)
    request_finished_at = datetime.utcnow()

    assert response.status_code == 202
    new_user_data = response.json()
    assert new_user_data['name'] == 'Bruno Sousa'
    assert new_user_data['email'] == 'bruno.sousa@example.com'

    # Retrieve user before asyncronous persistence
    response = requests.get(base_url + new_user_data['uuid'] + '/')
    assert response.status_code == 404

    # Wait for asyncronous task execution
    wait_for_task_execution(redis_client)

    # Retrieve user
    response = requests.get(base_url + new_user_data['uuid'] + '/')
    assert response.status_code == 200

    # Assert created_at
    created_at = datetime.strptime(response.json()['created_at'], '%Y-%m-%d %H:%M:%S')
    assert (created_at - request_finished_at).seconds >= 5
