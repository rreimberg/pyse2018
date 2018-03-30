
from functools import wraps

from flask import request
from werkzeug.exceptions import UnsupportedMediaType


def requires_json(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.mimetype not in ('application/json',):
            raise UnsupportedMediaType(
                "You must send a raw body in JSON format with the Content-Type"
                " header properly set to application/json.")

        return f(*args, **kwargs)

    return decorated
