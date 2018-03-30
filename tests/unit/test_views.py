
import json
from datetime import datetime

import pytest
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm.exc import NoResultFound

from sample.models import User


@pytest.fixture
def user():
    return User(
        uuid='valid-uuid',
        name='sample',
        email='me@example.com',
        created_at=datetime(2018, 4, 1, 13, 50)
    )


def test_get_invalid_user_returns_not_found(client, mocker):
    db_fetch_mock = mocker.patch.object(BaseQuery, 'one')
    db_fetch_mock.side_effect = NoResultFound

    response = client.get('/v1/user/fake-uuid/')
    assert response.status_code == 404


def test_get_valid_user_returns_user_content(client, mocker, user):
    db_fetch_mock = mocker.patch.object(BaseQuery, 'one')
    db_fetch_mock.return_value = user

    response = client.get('/v1/user/valid-uuid/')
    assert response.status_code == 200
    assert response.content_type == 'application/json'

    expected_response = {
        'uuid': 'valid-uuid',
        'name': 'sample',
        'email': 'me@example.com',
        'created_at': '2018-04-01 13:50:00',
    }
    assert response.json == expected_response


def test_post_user_without_json_content_type_returns_unsupported_mimetype(client):
    response = client.post('/v1/user/')
    assert response.status_code == 415


def test_post_user_without_name_returns_bad_request(client):
    response = client.post('/v1/user/',
                           data=json.dumps({'email': 'email@domain.com'}),
                           headers={'Content-Type': 'application/json'})

    assert response.status_code == 400


def test_post_user_with_success(client, mocker):

    fake_uuid = mocker.Mock()
    fake_uuid.hex = 'mocked-uuid'

    uuid_mock = mocker.patch('sample.views.uuid4')
    uuid_mock.return_value = fake_uuid

    celery_delay_mock = mocker.patch('sample.views.save_on_database.delay')

    payload = {
        'name': 'username',
        'email': 'fakeemail@user.com',
    }

    response = client.post('/v1/user/',
                           data=json.dumps(payload),
                           headers={'Content-Type': 'application/json'})

    assert response.status_code == 202
    assert response.content_type == 'application/json'

    expected_response = {
        'uuid': 'mocked-uuid',
        'name': 'username',
        'email': 'fakeemail@user.com',
    }
    assert response.json == expected_response

    assert celery_delay_mock.call_count == 1
    assert celery_delay_mock.call_args == (
        ('mocked-uuid', 'username', 'fakeemail@user.com'),
    )
