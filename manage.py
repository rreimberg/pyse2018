#!/usr/bin/env python

from flask_script import Manager

from sample.app import create_app, db

app = create_app()
manager = Manager(app)


@manager.command
def create_db():
    db.create_all()


if __name__ == "__main__":
    manager.run()
