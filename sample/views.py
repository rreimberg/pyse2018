
from uuid import uuid4

from flask import abort, jsonify, request
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound

from sample.decorators import requires_json
from sample.models import User
from sample.tasks import save_on_database


class UserAPI(MethodView):

    def get(self, user_uuid):

        try:
            user = User.query.filter_by(uuid=user_uuid).one()
        except NoResultFound:
            abort(404)

        response = {
            'uuid': user.uuid,
            'name': user.name,
            'email': user.email,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        return jsonify(response)

    @requires_json
    def post(self):

        try:
            name = request.json['name']
            email = request.json['email']
        except KeyError:
            abort(400)

        user_uuid = uuid4().hex

        save_on_database.apply_async((user_uuid, name, email), countdown=5)

        response = {
            'uuid': user_uuid,
            'name': name,
            'email': email
        }

        return jsonify(response), 202
