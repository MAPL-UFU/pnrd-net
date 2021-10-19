from flask import Blueprint, request
from pnrdnet_addressing.addresser import NAMESPACE
from pnrdnet_api.dispatcher.Dispatcher import Dispatcher
from pnrdnet_api.utils.functions import generate_auth_token, validate_fields
from pnrdnet_api.utils.responses import response_with
from pnrdnet_api.utils import responses as resp


core_routes = Blueprint("core_routes", __name__)


@core_routes.route("/login", methods=["POST"])
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


@core_routes.route("/network", methods=["GET"])
def get_owner_details():
    try:
        print(NAMESPACE)
        dispatch = Dispatcher()

        net_data, net_address = dispatch.get_network_data()

        return response_with(
            resp.SUCCESS_201,
            value={'address': net_address, 'data': net_data}
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)
