from flask import Blueprint, request
from pnrdnet_api.config import AES_KEY, APP_SECRET_KEY
from pnrdnet_api.dispatcher.Dispatcher import Dispatcher
from pnrdnet_api.utils.functions import get_time, validate_fields
from pnrdnet_api.utils.responses import response_with
from pnrdnet_api.utils import responses as resp
from google.protobuf.json_format import MessageToJson


record_routes = Blueprint("record_routes", __name__)


@record_routes.route("/create", methods=["POST"])
def create_record():
    try:
        data = request.get_json()
        required_fields = [
            'private_key',
            'record_id',
            'reader_id',
            'ant_id',
            'situation',
            'places',
            'transitions',
            'incidenceMatrix',
            'token',
            'tag_id'
        ]
        validate_fields(required_fields, data)
        dispatch = Dispatcher()

        result, status = dispatch.send_create_record_transaction(
            private_key=data['private_key'],
            record_id=data['record_id'],
            reader_id=data['reader_id'],
            ant_id=data['ant_id'],
            situation=data['situation'],
            places=data['places'],
            transitions=data['transitions'],
            incidenceMatrix=data['incidenceMatrix'],
            token=data['token'],
            tag_id=data['tag_id'],
            timestamp=get_time())

        return response_with(
            resp.SUCCESS_201,
            value={
                'data': f'Create record transaction {status}',
                'statusBlockchain': status}
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@record_routes.route("/detail", methods=["POST"])
def get_record_details():
    try:
        data = request.get_json()
        required_fields = ['record_id']
        validate_fields(required_fields, data)
        dispatch = Dispatcher()

        record_data, record_address = dispatch.get_record_data(
            record_id=data.get('record_id'))
        record = record_data[0][0]
        record_decoded = {
            'tag_id': record['tag_id'],
            'record_id': record['record_id'],
            'owners': record['owners'],
            'history': list()
        }
        for history in record['history']:
            record_decoded['history'].append(
                {
                    'reader_id': history['reader_id'],
                    'ant_id': history['ant_id'],
                    'situation': history['situation'],
                    'places': history['places'],
                    'transitions': history['transitions'],
                    'incidenceMatrix': list(history['incidenceMatrix']),
                    'token': list(history['token']),
                }
            )
        return response_with(
            resp.SUCCESS_201,
            value={'address': record_address, 'data': record_decoded}
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@record_routes.route("/transfer", methods=["POST"])
def transfer_record():
    try:
        data = request.get_json()
        required_fields = ['receiving_owner_pubkey',
                           'record_id', 'private_key']
        validate_fields(required_fields, data)
        dispatch = Dispatcher()

        result, status = dispatch.send_transfer_record_transaction(
            private_key=data['private_key'],
            receiving_owner=data['receiving_owner_pubkey'],
            record_id=data['record_id'],
            timestamp=get_time())
        return response_with(
            resp.SUCCESS_201,
            value={
                'data': f'Create transfer transaction {status}',
                'statusBlockchain': status}
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@record_routes.route("/update", methods=["POST"])
def update_record():
    try:
        data = request.get_json()
        required_fields = required_fields = [
            'private_key',
            'record_id',
            'reader_id',
            'ant_id',
            'situation',
            'places',
            'transitions',
            'incidenceMatrix',
            'token',
        ]
        validate_fields(required_fields, data)
        dispatch = Dispatcher()

        result, status = dispatch.send_update_record_transaction(
            private_key=data['private_key'],
            record_id=data['record_id'],
            reader_id=data['reader_id'],
            ant_id=data['ant_id'],
            situation=data['situation'],
            places=data['places'],
            transitions=data['transitions'],
            incidenceMatrix=data['incidenceMatrix'],
            token=data['token'],
            timestamp=get_time())
        return response_with(
            resp.SUCCESS_201,
            value={
                'data': f'Create update transaction {status}',
                'statusBlockchain': status}
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)
