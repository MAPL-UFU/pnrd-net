"""REST API para a comunicação entre o Banco de Dados do Categorizze e Consumidores

API desenvolvida em Flask, SQLAlchemy e JWT para autenticação

  Estrutura:
    config : Arquivos de Configuração do Banco e outros
    models: Modelos do Banco em SQLAlchemy
    routes: Rotas da API modularizada por blueprints
    utils: 
        database: Inicialização da Base
        response: Respostas-padrão para API
    main: Arquivo principal do Flask
    run: Arquivo de Execução

version: 0.1.0
author: Roger Carrijo github: @roger1618
"""

import os
import sys
import logging
import argparse
from flask import Flask
from routes.auth import auth_routes
from routes.owner import owner_routes
from config import CoreConfig
from utils.responses import response_with
import utils.responses as resp
from dotenv import load_dotenv


load_dotenv()
LOGGER = logging.getLogger(__name__)


def parse_args(args):
    parser = argparse.ArgumentParser(
        description='Starts the PNRD NET')

    parser.add_argument(
        '-B', '--bind',
        help='identify host and port for api to run on',
        default='localhost:8000')
    parser.add_argument(
        '-C', '--connect',
        help='specify URL to connect to a running validator',
        default='tcp://localhost:4004')
    parser.add_argument(
        '-t', '--timeout',
        help='set time (in seconds) to wait for a validator response',
        default=500)
    parser.add_argument(
        '--primary-key',
        help='The authorized primary key for blockchain access',
        default='sawtooth')
    parser.add_argument(
        '--public-key',
        help='The public key for blockchain access',
        default='sawtooth')
    parser.add_argument(
        '--password',
        help="The authorized password for blockchain access",
        default='sawtooth')
    parser.add_argument(
        '-v', '--verbose',
        action='count',
        default=0,
        help='enable more verbose output to stderr')

    return parser.parse_args(args)


def create_app(config):
    """
    """
    app = Flask(__name__)
    app.config.from_object(config)

    # BLUEPRINTS
    app.register_blueprint(auth_routes, url_prefix="/auth")
    app.register_blueprint(owner_routes, url_prefix="/owner")
    # START GLOBAL HTTP CONFIGURATIONS

    @app.after_request
    def add_header(response):
        return response

    @app.errorhandler(400)
    def bad_request(e):
        logging.error(e)
        return response_with((resp.BAD_REQUEST_400))

    @app.errorhandler(500)
    def server_error(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)

    @app.errorhandler(404)
    def not_found(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_404)

    logging.basicConfig(
        stream=sys.stdout,
        format="%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s",
        level=logging.DEBUG,
    )
    return app


app_config = CoreConfig

app = create_app(app_config)

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", use_reloader=False)
