
from datetime import datetime

from sample.app import db


class User(db.Model):

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    uuid = db.Column(db.String(32), index=True, unique=True)
    name = db.Column(db.String(32))
    email = db.Column(db.String(32))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __eq__(self, other):
        """Workaround to compare objects in transient state."""
        comparable_fields = ['uuid', 'name', 'email']
        return all([getattr(self, field) == getattr(other, field)
                    for field in comparable_fields])
