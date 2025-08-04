from flask_mysqldb import MySQL
from .log_settings import loggingSettings

log_set = loggingSettings()

class DBHandler:
    """
    Classe resnponsável por gerenciar a conexão com o banco de dados MySQL.
    e realizar operações como criação de tabela, inserção e consulta.
    """
    def __init__(self, app):
        """
        Inicializa o manipulador de banco de dados com base na aplicação Flask.

        Args:
            app (Flask): A instância da aplicação Flask.
        """
        self.mysql = MySQL(app)

        # Cria a tabela de usuários automaticamente, caso não exista.
        with app.app_context():
            self._create_table_if_not_exists()

    def get_connection(self):
        """
        Retorna a conexão ativa com o banco de dados MySQL.

        Returns:
            connection: Objeto de conexão com o banco.
        """ 
        log_set.info("Conectando ao banco de dados ...")
        
        return self.mysql.connection
    
    def get_unique_data(self, table_name,args):
        """
        Busca um registro único na tabela com base no nome do usuário.

        Args:
            table_name (str): Nome da tabela onde será feita a busca.
            args (dict): Dicionário com o campo 'field_name' representando o nome do usuário.

        Returns:
            dict: Registro encontrado ou None se não houver. 
        """

       
        try:
           
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name} WHERE user_name = %s", (args['field_name'],))
            data = cursor.fetchone()
            cursor.close()
        
        except Exception as error:
            print("erro", error)
            log_set.error(f"Erro: {error}")

        return data
    
    def _create_table_if_not_exists(self):
        """
        Cria a tablea 'users' no banco de dados caso ela ainda não exista.
        Essa tabela contém campos de ID, nome de usuário e senha.
        """
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS users ( 
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_name VARCHAR(50) UNIQUE NOT NULL,
                    user_password VARCHAR(255) NOT NULL
                )
                '''
            )

            
            connection.commit()
            cursor.close()
        except Exception as error:
            log_set.error(f'{error}')

    def create_user(self, user_name, user_password):
        """
        Insere um novo usuário na tabela 'users'.

        Args:
            user_name (str): Nome de usuário.
            user_password (str): Senha (Já criptografada, se aplicável).
        """
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO users (user_name, user_password) VALUES (%s, %s)",
                (user_name, user_password)
            )
            connection.commit()
            cursor.close()
            
        except Exception as error:
            log_set.error(f'{error}')
