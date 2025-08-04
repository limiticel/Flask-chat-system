// Função assíncrona que busca usuários conforme o que for digitado no input
async function searchUsers(){
    // Pega o valor atual do campo de busca.
    const query = document.getElementById("search").value;

    // Faz uma requisição GET para o endpoint Flask passando o valor da busca como parâmetro da query string
    const res = await fetch(`/search_users?q=${encodeURIComponent(query)}`)
    
    // Converte a resposta da requisição para JSON(lista de nomes de usuários).
    const users = await res.json()

    // Selectiona a lista onde os resultados serão exibidos
    const resultList = document.getElementById("results")

    // Limpa a lista de resultados antes de preencher com os novos dados.
    resultList.innerHTML = "";

    // Para cada usuário retornado.
    users.forEach(user => {
        const li = document.createElement("li");

        // Cria um span só para mostrar o nome
        const span = document.createElement("span");
        span.textContent = user; // define o texto do span como o nome do usuário. 
        li.appendChild(span);// adiciona o span ao li.

        // Cria o botão para abrir o chat
        const button = document.createElement("button");
        button.textContent = "Chat"; // texto do botão
        button.style.marginLeft = "10px"; // um espacinho entre o nome e o botão

        // Ao clicar, redireciona para a página do chat privado com esse usuário
        button.onclick = () => {
            window.location.href = `/private_chat/${encodeURIComponent(user)}`;
        };

        // Adiciona o botão ao li
        li.appendChild(button);

        // Adiciona o item completo (com nome + botão) á lista de resultados.
        resultList.appendChild(li);
    })

}

// Executa assim que a página termina de carregar.
window.onload = function() {
    document.getElementById("search").addEventListener("input", searchUsers);
}