from flask import Blueprint, request
from pnrdnet_api.config import AES_KEY, APP_SECRET_KEY
from pnrdnet_api.dispatcher.Dispatcher import Dispatcher
from pnrdnet_api.utils.functions import encrypt_private_key, generate_auth_token, get_time, hash_password, validate_fields
from pnrdnet_api.utils.responses import response_with
from pnrdnet_api.utils import responses as resp


owner_routes = Blueprint("owner_routes", __name__)


@owner_routes.route("/create", methods=["POST"])
def create_owner():
    try:
        data = request.get_json()
        required_fields = ['name']
        validate_fields(required_fields, data)
        dispatch = Dispatcher()
        public_key, private_key = dispatch.get_new_key_pair()

        result, status = dispatch.send_create_owner_transaction(
            private_key=private_key,
            name=data.get('name'),
            timestamp=get_time())

        encrypted_private_key = encrypt_private_key(
            AES_KEY, public_key, private_key)

        token = generate_auth_token(encrypted_private_key, public_key)
        return response_with(
            resp.SUCCESS_201,
            value={'public_key': public_key,
                   'private_key': private_key,
                   "statusBlockchain": status}
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@owner_routes.route("/detail", methods=["POST"])
def get_owner_details():
    try:
        data = request.get_json()
        required_fields = ['public_key']
        validate_fields(required_fields, data)
        dispatch = Dispatcher()

        owner_data, owner_address = dispatch.get_owner_data(
            public_key=data.get('public_key'))

        return response_with(
            resp.SUCCESS_201,
            value={'address': owner_address, 'data': owner_data}
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)
