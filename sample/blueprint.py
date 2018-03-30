
from flask import Blueprint

from sample.views import UserAPI

blueprint = Blueprint('api', __name__)

user_view = UserAPI.as_view('user_api')
blueprint.add_url_rule('/user/', view_func=user_view, methods=['POST'])
blueprint.add_url_rule('/user/<user_uuid>/', view_func=user_view, methods=['GET'])
