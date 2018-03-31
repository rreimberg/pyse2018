
import json
from datetime import datetime
from urllib.parse import urlparse

import requests
from celery import current_app
from celery.result import AsyncResult
from redis import Redis


def _wait_for_task_execution():
    parsed = urlparse(current_app.conf['CELERY_RESULT_BACKEND'])
    kwargs = {
        'host': parsed.hostname
    }

    if parsed.port:
        kwargs['port'] = parsed.port

    if parsed.path:
        kwargs['db'] = parsed.path.strip('/')

    client = Redis(**kwargs)
    for key in client.scan_iter():
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


def test_create_user_with_success_persists_data_on_celery_task(base_url, users):

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
    _wait_for_task_execution()

    # Retrieve user
    response = requests.get(base_url + new_user_data['uuid'] + '/')
    assert response.status_code == 200

    # Assert created_at
    created_at = datetime.strptime(response.json()['created_at'], '%Y-%m-%d %H:%M:%S')
    assert (request_finished_at - created_at).seconds >= 5
