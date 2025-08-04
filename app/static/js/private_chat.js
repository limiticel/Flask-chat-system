
// Cria uma conexão com o servidor Socket.IO
var socket = io("http://192.168.1.71:5000");


// Ouvinte: quando uma mensagem for recebida do servidor.
//chama a função addMessageToList para exibi-la na interface
socket.on("receive_message", function(data) {
    addMessageToList(data);
});

// Envia uma nova mensagem para o servidor
function sendMessage() {
    // Referência à div principal do chat
    const chatDiv = document.getElementById("chat");
    
    // Campo de entrada da mensagem
    const messagebox = document.getElementById("message");
    
    // Obtém remetente e destinatário dos atributos da div
    const sender = chatDiv.getAttribute("data-currentuser");
    const receiver = chatDiv.getAttribute("data-recipient");
    const message = messagebox.value;

    // Envia a mensagem ao servidor por meio do socket
    socket.emit("send_message", {sender, receiver, message});
    
    // Limpa o campo de texto após o envio
    messagebox.value = "";
}


// Adiciona uma mensagem à lista na interface
function addMessageToList(data) {
    if (!data.message || data.message.trim() === "") {
        // Não adiciona mensagens vazias ou só com espaços
        return;
    }


    // Identifica o usuário atual para saber se a mensagem é dele.
    const currentuser = document.getElementById("chat").getAttribute("data-currentuser");

    // Cria um novo item da lista de mensagens
    const li = document.createElement("li");
    li.classList.add("message");

    // Aplica estilo dependendo do remetente.
    if (data.sender === currentuser) {
        li.classList.add("my-message"); // Mensagem do próprio usuario
    } else {
        li.classList.add("other-message"); // Mensagem do outro usuário.
    }

   
    // Define o conteúdo da mensagem.
    li.textContent = ` ${data.message}`;

    // Adicionar botão de deletar somente para mensagens próprias
    if (data.sender === currentuser && data.id) {
        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "🗑️";
        deleteBtn.onclick = () => deleteMessage(data.id); // Função que deleta
        li.appendChild(deleteBtn);
    }

    // Adiciona a mensagem à lista visivel.
    document.getElementById("messages").appendChild(li);

    scrollToBottom()
}


// Envia a requisição para deletar uma mensagem do banco de dados.
function deleteMessage(messageId) {
    fetch(`/delete_message/${messageId}`, {method: "DELETE"})
    .then(res => {
        if (res.ok) {
            reloadMessages(); // Recarrega as mensagens após deletar. 
        } else {
            alert('Erro ao excluir a mensagem');
        }
    });
}

// Recarrega todas as mensagens da conversa com destinatário atual.
function reloadMessages() {
    const recipient = document.getElementById("chat").getAttribute("data-recipient");

    fetch(`/load_messages/${recipient}`)
    .then(response => response.json())
    .then(data => {
        const messagesUl = document.getElementById("messages");
        messagesUl.innerHTML = ""; // limpa as mensagens atuais.
        data.forEach(addMessageToList); // exibe as novas mensagens.

        scrollToBottom()
    });
}


// Executa após o carregamento da página.
window.onload = function() {
    // Ao carregar, busca as mensagens da conversa atual.
    const recipient = document.getElementById("chat").getAttribute("data-recipient");

    fetch(`/load_messages/${recipient}`)
        .then(response => response.json())
        .then(data => {
            data.forEach(addMessageToList);// adiciona na interface 
        });


    // Referências ao botão e campo de mensagem
    const sendBtn = document.getElementById("sendMessage");
    const messageInput = document.getElementById("message");

    // Evento de clique no botão
    sendBtn.addEventListener("click", sendMessage);

    // Evento de tecla Enter no campo de mensagem
    messageInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // evita quebra de linha
            sendMessage();
        }
    });
}

function scrollToBottom() {
    const messagesUl = document.getElementById("messages");
    messagesUl.scrollTop = messagesUl.scrollHeight;
}
