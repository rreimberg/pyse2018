
import configparser
import os

from kombu import Exchange, Queue


CONFIG_FILE = os.getenv('CONFIG_FILE', '/etc/pyse2018/pyse2018.ini')

config = configparser.ConfigParser()
config.read(CONFIG_FILE)


class Configuration(object):

    BROKER_URL = config.get('MQ', 'BROKER_URL')

    CELERY_QUEUES = (
        Queue(
            'save-on-database',
            Exchange('save-on-database'),
            routing_key='save-on-database'),
    )

    SQLALCHEMY_DATABASE_URI = config.get('DATABASE', 'URI')
