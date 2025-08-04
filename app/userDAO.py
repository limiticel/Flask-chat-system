from .DBHandler import DBHandler
from .log_settings import loggingSettings

class userDAO:
    """
    Classe responsável por operações de acesso a dados (DAO) relacionados ao usuário.
    """
    def __init__(self):
        """
        Inicializa o DAO com uma instância do DBHandler.

        Args:
            app: Instância do Flask app usada para inicializar o DBHandler.
        """
        pass
    

    def get_user(self, user_id):
        """
        Busca um usuário pelo ID.

        Args:
            user_id (int): ID do usuário a ser buscado.

        Returns:
            dict: Dados do usuário, se encontrado.
        """
        db_handler = DBHandler()
        
        return db_handler.get_unique_data(args = {
            'table_name': 'users',
            'field_name': 'user_id',
            'user_id': user_id
        })
    
    