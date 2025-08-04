from flask import Flask, jsonify,render_template, request, session, redirect
from .DBHandler import DBHandler
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import DateHelper
from .log_settings import loggingSettings

from flask_socketio import emit
import datetime
helper = DateHelper()


log_set = loggingSettings()

def set_routes(app, socketio):
    """
    Define e registra todas as rotas da aplciação Flask, além de configurar os eventos de WebSocket (SocketIO).

    Args:
        app(Flask): A instância da aplicação Flask.
        sokcetio (SocketIO): A instânica do SocketIO associada ao app Flask.
    """
    # Inicializa o manipulador de banco de dados com a configuração do app. 
    db_handler = DBHandler(app)


    @app.route("/", methods=["GET", "POST"])
    def login():
        """
        Rota principal de login da aplicação.

        Se o método for GET:
            - Renderiza a página de login.

        Se o método for POST:
            - Coleta os dados enviados pelo formulário (usuário e senha).
            - Busca o usuário no banco de dados.
            - Se o usuário e a senha estiver correta, armazena os dados na sessão e redireciona para o dashboard.
        
        Returns:
            str: Renderiza o template de login (em caso de GET ou falha no login).
        """
        if request.method == "POST":
            data = helper.get_all_names_form()
            user = db_handler.get_unique_data("users",args={"field_name": data["username"]})
           

            if user and check_password_hash(user['user_password'], data["password"]):
                session['user_id'] = user['user_id']
                session["user_id"] = user["user_id"]
                session["user_name"] = user["user_name"]
                return redirect("/dashboard")
            
                
            
        return render_template("login.html")
    
    @app.route("/register", methods=["GET","POST"])
    def register():
        """
        Rota de registro de novos usuários.

        Se o método for GET:
            - Renderiza a página de cadastro.
        
        Se o método for POST:
            - Coleta os dados do formulário;
            - Verifica se a senha e a confirmação batem.
            - Se não baterem, exibe erro na tela.
            - Se estiverem corretas, cria um novo usuário no banco com a senha criptografada.

        Returns:
            str: Renderiza o template de cadastro, com ou sem mensagem de erro. 
        """

        if request.method == "POST":
            data = helper.get_all_names_form()
          
            if data["password"] != data["verification"]:
                return render_template("register.html", error="Passwords do not match")
            else:
                db_handler.create_user(data['username'], generate_password_hash(data['password']))

        return render_template("register.html")
    
    @app.route("/dashboard", methods=["GET","POST"])
    def dashboard():
        """
        Rota de página principal (dashoboard) do usuário após login.

        Verifica se o usuário está autenticado através da sessão.
        Se não estiver autenticado, redireciona para a página de login.
        Caso contrário, renderiza o dashboard.

        Returns:
            str: Redireciona para "/" se o usuário não estiver logado,
                 ou renderiza a página "dashboard.html"
        """
        if 'user_id' not in session:
            return redirect("/")
        return render_template("dashboard.html")
    

    @app.route("/load_messages/<recipient>")
    def load_messages(recipient):
        """
        Rota que carrega todas as mensagens trocadas entre o usuário logado e o destinatário.

        Recupera o nome do usuário atual da sessão e busca no banco de dados todas as mensagens.
        onde o remetente e o destinatário são uma combinação entre dois usuários.
        As mensagens são retornadas em ordem crescente ao tempo.

        Args:
            recipient (str): Nome do destinatário com quem o usuário está conversando.

        Returns:
            Response: Uma responsa JSON contendo a lista de mensagens no formato:
                [
                    {
                    "id":int,
                    "sender":str,
                    "receiver": str,
                    "message": str,
                    "timestamp": str(formatado)
                    },
                    ...
                ]
        """
        connection = db_handler.get_connection()
        sender = session.get("user_name")
        
        cursor = connection.cursor()

        # Consulta todas as mensagens trocadas entre o sender e o recipient. 
        cursor.execute("SELECT id,sender, receiver, message, timestamp FROM messages WHERE (sender = %s AND receiver = %s) OR (sender = %s AND receiver = %s) ORDER BY timestamp ASC", (sender, recipient, recipient, sender))
        messages = cursor.fetchall()
        print(messages)
        cursor.close()

        messages_list = []
        for message in messages:
            messages_list.append({
                "id": message["id"],
                "sender": message['sender'],
                "receiver": message["receiver"],
                "message": message["message"],
                "timestamp": message['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            })
       

        return jsonify(messages_list)

    @app.route("/private_chat/<recipient>", methods=["GET","POST"])
    def private_chat(recipient):
        """
        Rota responsável por exibir a interface de chat privado entre o usuário atual e outro usuário (recipient).

        Valida se o destinatário (recipient) existe no banco de dados.  Caso exista, renderiza a 
        página de chat com os dados necessários para identificar os participantes.

        Args:
            recipient (str): Nome do usuário destinatário do chat.

        Returns:
            - HTML da página de chat privado(`private_chat.html`) com dados do dstinatário.
            - JSON de erro 404 se o usuário destinatário não existir.
        """

        # Verifica se o destinatário existe no banco de dados.
        rec = db_handler.get_unique_data("users", args={"field_name": recipient})
        if not rec:
            return jsonify({"error": "User not found"}), 404
        
        # Renderiza a página de chat como nome e o ID do destinatário.
        return render_template("private_chat.html", recipient=recipient, recipient_id=rec["user_id"])
       
    @socketio.on("send_message")
    def handle_message(data):
        """
        Manipula o evento de envio de mensagem via Socket.IO.

        Valida e salva a mensagem recebida no banco de dados, e emite o evento.
        'receive_message' para todos os clientes conectados, para que possam
        atualizar sua interfaces em tempo real.

        Args:
            data (dict): Dicionário contendo os campos 'sender', 'receiver' e 'message'.
        
        Retorna:
            None
        """

        # Remove espaçoes em branco no começo e fim da mensagem
        message = data.get("message", "").strip()
        
        # Não processa mensagens vazias.
        if not message:
            return 
        
      
        connection = db_handler.get_connection()
        sender = data["sender"]
        receiver = data["receiver"]

        # Usamos a mensagem já limpa.
        message = data["message"]

        # Marca o timestamp atual no formato string.
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insere a mensagem no banco
        cursor = connection.cursor()
        cursor.execute("INSERT INTO messages (sender, receiver, message, timestamp) VALUES (%s, %s, %s, %s)", (sender, receiver, message, timestamp))
        connection.commit()
        cursor.close()

        # Envia a mensagem para todos os clientes conectados (broadcast)
        emit("receive_message",data, broadcast=True)
    
    @app.route("/search_users", methods=["GET"])
    def search_users():
        """
        Endpoint para busca de usuários pelo nome.

        Recebe um parâmetro de consulta 'q' via query string e retorna uma lista
        com os nomes de usuários que contenham o termo pesquisado.

        Retorna:
            - JSON list contendo usernames correspondentes à pesquisa,
              ou lista vazia se nenhum termo for fornecido.
            - JSON com erro e status 500 em caso de exceção.
        """
        try:
            # Obtém a query string 'q', já removendo espaçoes em branco.
            query = request.args.get("q","").strip()
            
            print(query) # Log para debug
            
            # Se query vazia, retorna lisa vazia.
            if not query:
                return jsonify([])
            
            # Obtém conexão com o banco
            connection = db_handler.get_connection()
            cursor = connection.cursor()

            # Pesquisa usernames que contenham o texto da query.
            cursor.execute("SELECT user_name FROM users WHERE user_name LIKE %s", (f"%{query}%",))
            rows = cursor.fetchall()

            # Monta lista só com os nomes retornados.
            results = [row["user_name"] for row in rows]
           
            cursor.close()
            
            # Retorna lista JSON com nomes encontrados.
            return jsonify(results)

        except Exception as e:
            log_set.error(f"{e}")

            #Retorna erro 500 com mensagem genérica
            return jsonify({"error": "An error occurred while searching for users"}), 500
        
    @app.route("/delete_message/<int:message_id>", methods=["DELETE"])
    def delete_message(message_id):
        """
        Endpoint para deletar uma mensagem pelo seu ID.

        Args:
            message_id (int): ID da mensagem a ser deletada.

        Retorna:
            JSON com {"sucess": True} em caso de sucesso,
            ou JSON com {"error":"..."} e status 500 em caso de falha.
        """
     
        try:
            connection = db_handler.get_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM messages WHERE id = %s", (message_id, ))
            connection.commit()
            cursor.close()

            log_set.info("Mensagem deletada com sucesso!")

            return jsonify({"sucess": True})

        except Exception as e:
            log_set.error(f'{e}')
            return jsonify({"error": "Failed to delete message"}, 500)