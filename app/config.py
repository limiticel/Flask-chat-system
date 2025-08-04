import os
from dotenv import load_dotenv


load_dotenv()
# Class de configuração principal da aplicação Flask
class Config:
    # Chave secreta para proteger sessões e cookies (importante em produção)
    SECRET_KEY = os.environ.get("SECRET_KEY","default_secret_key")
    
    # Define onde as sessões serão armazenadas(neste caso, no sistema de arquivos)
    SESSION_TYPE = "filesystem"
    
    # Habilita o modo de depuração (útil durante o desenvolvimento).
    DEBUG = True


# Classe de configuração do banco de dados MySQL
class DatabaseConfig:
    # Endereço do host do MySQL
    MYSQL_HOST = os.environ.get("MYSQL_HOST")

    # Nome de usuário do banco de dados
    MYSQL_USER = os.environ.get("MYSQL_USER")

    # Senha do usuário do banco de dados.
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")

    # Nome do banco de dados a ser utilizado
    MYSQL_DB = os.environ.get("MYSQLDB")

    # Tipo de cursor usado para retornar os resultados como dicionários.
    MYSQL_CURSORCLASS = "DictCursor"

def app_config(app):
    """
    Aplica as configurações da aplicação e do banco de dados à instância Flask fornecida.

    Args:
        app (Flask): A instância da aplicação Flask a ser configurada.
    """
    # Carrega as configurações gerais da aplicação a partir da classe Config.
    app.config.from_object(Config)
    
    # APlica manualmente as configurações do banco de dados à aplicação Flask.
    app.config['MYSQL_HOST'] = DatabaseConfig.MYSQL_HOST
    app.config['MYSQL_USER'] = DatabaseConfig.MYSQL_USER
    app.config['MYSQL_PASSWORD'] = DatabaseConfig.MYSQL_PASSWORD
    app.config['MYSQL_DB'] = DatabaseConfig.MYSQL_DB
    app.config['MYSQL_CURSORCLASS'] = DatabaseConfig.MYSQL_CURSORCLASS

    