from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import datetime
from flask import jsonify
from .config import Config

def create_app():
    '''
    Cria e configura a aplicação Flask com suport a Websocket via SocketIO.

    Retorna:
        - app (Flask): instância da aplicação Flask configurada.
        - socketio (SocketIO): instância do SocketIO para comunicação em tempo real.
    '''
    # Instancia a aplicação Flask
    app = Flask(__name__)

    # Aplica as configurações definidas na função app_config do módulo config.
    config.app_config(app)
    
    # Inicializa o SocketIO com suporte a CORS para aceitar conexões de qualquer origem.
    socketio = SocketIO(app, cors_allowed_origins='*')

    # Importa e registra as rotas da aplicação, passando o ap e o socketio
    from .routes import set_routes
    set_routes(app, socketio)

    # Retorna a aplicação e o socketio, normalmente utilizados no run.py.
    return app, socketio