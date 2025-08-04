from app import create_app
from app.config import Config
from app.routes import set_routes
import eventlet

# Aplica monkey patch do eventlet para tornar compátivel com bibliotecas que usam operações de rede síncronas. 
eventlet.monkey_patch()

# Cria a aplicação Flask e instancia o SocketIO com as configurações definidas.
app, socketio = create_app()


if __name__ == "__main__":
    """
    Ponto de entrada da aplicação.

    Inicia o servidor Flask com suporte a WebSocket via SocketIO, usando o eventlet como servidor assíncrono.
    O servidor escuta em todas as interfaces (0.0.0.0) na porta 5000.
    """
    socketio.run(app, host="0.0.0.0", port=5000,debug=Config.DEBUG)
