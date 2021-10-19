from flask import Blueprint, request
from utils.functions import generate_auth_token, validate_fields
from utils.responses import response_with
from utils import responses as resp


auth_routes = Blueprint("auth_routes", __name__)


@auth_routes.route("/create", methods=["POST"])
def authenticate():
    try:
        data = request.get_json()
        required_fields = ['public_key', 'secret_key']
        validate_fields(required_fields, data)
        token = generate_auth_token(
            data.get['secret_key'], data.get('public_key'))
        return response_with(
            resp.SUCCESS_201,
            value={'authorization': token})
    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)
