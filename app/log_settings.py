import logging


class loggingSettings:
    """
    Classe responsável por configurar e utilizar o sistema de logging da aplicação.

    O log é armazenado no arquivo `app.log`, com nível de log padrão como INFO.
    Formato do log: [data hora] NÍVEL módulo: mensagem
    """
    def __init__(self):
        """
        Inicializa as configurações básicas de logging, como nome do arquivo, 
        nível mínimo de severidade e formato de mensagem.
        """
        logging.basicConfig(
            filename = 'app.log',
            level = logging.INFO,
            format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def info(self, arg):
        """
        Registra uma mensagem de nível INFO no log.
        
        Parâmetros:
            - args (str): A mensagem que será registrada.
        """
        return logging.info(f'{arg}')
    
    def error(self, arg):
        """
        Registra uma mensagem de nível ERROR no log.

        Parâmetros:
            - arg (str): A mensagem que será registrada.
        """
        return logging.error(f'{arg}')
