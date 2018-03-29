
from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy as OriginalSQLAlchemy


class SQLAlchemy(OriginalSQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        super(SQLAlchemy, self).apply_driver_hacks(app, info, options)
        if info.drivername.startswith('mysql') and info.drivername != 'mysql+gaerdbms':
            # enforce isolation level to READ COMMITTED
            if "isolation_level" not in options:
                options["isolation_level"] = "READ COMMITTED"


db = SQLAlchemy()
celery = Celery()


def create_app(override_settings={}):

    app = Flask(__name__)
    app.config.from_object('sample.settings.Configuration')
    app.config.update(override_settings)

    celery.conf.update(app.config)
    db.init_app(app)

    from sample.blueprint import blueprint
    app.register_blueprint(blueprint, url_prefix='/v1')

    return app
