from flask import Blueprint, request
from config import AES_KEY, APP_SECRET_KEY
from dispatcher.Dispatcher import Dispatcher
from utils.functions import encrypt_private_key, generate_auth_token, get_time, hash_password, validate_fields
from utils.responses import response_with
from utils import responses as resp


owner_routes = Blueprint("owner_routes", __name__)


@owner_routes.route("/create", methods=["POST"])
def create_owner():
    try:
        data = request.get_json()
        required_fields = ['name']
        validate_fields(required_fields, data)
        dispatch = Dispatcher()
        public_key, private_key = dispatch.get_new_key_pair()

        dispatch.send_create_agent_transaction(
            private_key=private_key,
            name=data.get('name'),
            timestamp=get_time())

        encrypted_private_key = encrypt_private_key(
            AES_KEY, public_key, private_key)

        token = generate_auth_token(encrypted_private_key, public_key)

        return response_with(
            resp.SUCCESS_201,
            value={'public_key': token, 'secret_key': encrypted_private_key}
        )
    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)
