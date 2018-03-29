
from datetime import datetime

from sample.app import db


class User(db.Model):

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    uuid = db.Column(db.String(32), index=True, unique=True)
    name = db.Column(db.String(32), index=True)
    email = db.Column(db.String(32), index=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
