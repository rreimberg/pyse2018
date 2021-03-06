
from urllib.parse import urlparse

import MySQLdb
import pytest
from redis import Redis

from sample.app import db
from sample.models import User


@pytest.fixture(scope='session')
def create_db(app):

    result = urlparse(app.config['SQLALCHEMY_DATABASE_URI'])
    db_name = result.path.strip('/')

    connection_params = {
        'host': result.hostname,
        'user': result.username,
        'password': result.password,
    }

    if result.port:
        connection_params['port'] = result.port

    raw_connection = MySQLdb.connect(**connection_params)
    cursor = raw_connection.cursor()

    database_already_exists = cursor.execute(
        'SELECT schema_name FROM information_schema.schemata WHERE '
        'schema_name = "{}"'.format(db_name)
    )

    if not database_already_exists:
        cursor.execute('CREATE DATABASE {}'.format(db_name))

    db.drop_all()
    db.create_all()


@pytest.fixture(scope='session')
def redis_client(app):
    result = urlparse(app.config['CELERY_RESULT_BACKEND'])
    connection_params = {
        'host': result.hostname
    }

    if result.port:
        connection_params['port'] = result.port

    if result.path:
        connection_params['db'] = result.path.strip('/')

    client = Redis(**connection_params)
    return client


@pytest.yield_fixture(autouse=True)
def truncate_db(create_db, redis_client):
    yield

    # teardown

    # truncate mysql tables
    connection = db.engine.connect()
    transaction = connection.begin()
    connection.execute('SET FOREIGN_KEY_CHECKS = 0;')
    for table in db.get_tables_for_bind():
        connection.execute(table.delete())
    connection.execute('SET FOREIGN_KEY_CHECKS = 1;')
    transaction.commit()

    # clear celery results
    for key in redis_client.scan_iter():
        redis_client.delete(key)


@pytest.fixture(scope='session')
def base_url():
    return 'http://pyse2018-api.docker/v1/user/'


@pytest.fixture
def user_andre():
    user = User(
        uuid='1d3c7157f1244a9987f19090588d331d',
        name='André Silva',
        email='andre.silva@example.com',
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def user_rafael():
    user = User(
        uuid='443d94e90a624bb68302bb40378b789d',
        name='Rafael Reimberg',
        email='rafael.reimberg@example.com',
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def users(user_andre, user_rafael):
    return [user_andre, user_rafael]
