
import configparser
import os

from kombu import Exchange, Queue


CONFIG_FILE = os.getenv('CONFIG_FILE', '/etc/pyse2018/pyse2018.ini')

config = configparser.ConfigParser()
config.read(CONFIG_FILE)


class Configuration(object):

    BROKER_URL = config.get('MQ', 'BROKER_URL')
    if 'RESULT_BACKEND' in config['MQ'].keys():
        CELERY_RESULT_BACKEND = config.get('MQ', 'RESULT_BACKEND')
        CELERY_TRACK_STARTED = True

    CELERY_QUEUES = (
        Queue(
            'save-on-database',
            Exchange('save-on-database'),
            routing_key='save-on-database'),
    )

    SQLALCHEMY_DATABASE_URI = config.get('DATABASE', 'URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
