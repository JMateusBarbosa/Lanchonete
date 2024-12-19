// Acompanhar Pedidos - Funções para filtrar, buscar, paginar e concluir pedidos
// Este arquivo gerencia a interação com a tabela de pedidos na interface do usuário.
// Ele permite filtrar pedidos por status, buscar por palavra-chave, realizar a paginação de resultados,
// e concluir pedidos diretamente na tabela, atualizando o status e removendo os pedidos concluídos quando necessário.
// Além disso, exibe mensagens de sucesso ou erro conforme as ações são realizadas.

document.addEventListener('DOMContentLoaded', function() {
    
    // Definindo variáveis para os elementos da página
    const filterStatus = document.getElementById('filter-status');  // Filtro de status dos pedidos
    const searchInput = document.getElementById('search');  // Campo de pesquisa de pedidos
    const prevPageBtn = document.getElementById('prev-page');  // Botão para a página anterior
    const nextPageBtn = document.getElementById('next-page');  // Botão para a próxima página
    const currentPageLabel = document.getElementById('current-page');  // Label de página atual
    let currentPage = 1;  // Página atual
    const itemsPerPage = 10;  // Número de itens por página

    // Delegação de eventos para o botão de "Concluir Pedido"
    document.querySelector('.orders-table tbody').addEventListener('click', function(event) {
        // Verifica se o clique foi no botão 'Concluir Pedido'
        if (event.target.classList.contains('btn-complete')) {
            const pedidoId = event.target.getAttribute('data-pedido-id');  // Obtém o ID do pedido
            const statusCell = event.target.closest('tr').querySelector('.status-cell');  // Célula de status do pedido

            // Envia uma requisição POST para concluir o pedido
            fetch(`/concluir-pedido/${pedidoId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')  // Token CSRF para segurança
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    statusCell.textContent = 'Concluído';  // Atualiza o status na tabela
                    showMessage('Pedido concluído com sucesso!', 'success');  // Exibe a mensagem de sucesso

                    // Remove a linha da tabela se o filtro aplicado for "Pendente"
                    if (filterStatus.value === 'pending') {
                        const row = statusCell.closest('tr');
                        row.remove();
                    }
                } else {
                    showMessage('Erro ao concluir o pedido: ' + data.message, 'error');  // Exibe mensagem de erro
                }
            })
            .catch(error => {
                console.error('Erro ao concluir o pedido:', error);
                showMessage('Erro ao concluir o pedido. Por favor, tente novamente.', 'error');  // Exibe mensagem de erro em caso de falha na requisição
            });
        }
    });
    
    // Evento para buscar pedidos ao digitar na barra de pesquisa
    searchInput.addEventListener('input', function() {
        const searchQuery = searchInput.value;  // Obtém o valor digitado na pesquisa
        const url = new URL(window.location.href);
        url.searchParams.set('search', searchQuery);  // Atualiza o parâmetro de busca na URL

        // Requisição para buscar os pedidos com a query de pesquisa
        fetch(url.toString(), {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'  // Indica que é uma requisição AJAX
            }
        })
        .then(response => response.text())
        .then(data => {
            // Atualiza as linhas da tabela com os resultados da pesquisa
            document.querySelector('.orders-table tbody').innerHTML = data;
        })
        .catch(error => {
            console.error('Erro ao buscar os pedidos:', error);  // Exibe erro no console
        });
    });

    // Evento para filtrar pedidos por status
    filterStatus.addEventListener('change', function() {
        const status = filterStatus.value;  // Obtém o valor do filtro de status
        const url = new URL(window.location.href);
        url.searchParams.set('status', status);  // Atualiza o parâmetro de status na URL
    
        // Requisição para filtrar os pedidos com o status selecionado
        fetch(url.toString(), {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'  // Indica que é uma requisição AJAX
            }
        })
        .then(response => response.text())
        .then(data => {
            // Atualiza as linhas da tabela com os pedidos filtrados
            document.querySelector('.orders-table tbody').innerHTML = data;
        })
        .catch(error => {
            console.error('Erro ao filtrar os pedidos:', error);  // Exibe erro no console
        });
    });

    // Função para carregar uma página específica de pedidos
    function loadPage(page) {
        const searchQuery = searchInput.value;  // Obtém a pesquisa atual
        const status = filterStatus.value;  // Obtém o status atual
        const url = new URL(window.location.href);
        url.searchParams.set('page', page);  // Atualiza o parâmetro de página na URL
        url.searchParams.set('items_per_page', itemsPerPage);  // Define o número de itens por página
        if (searchQuery) {
            url.searchParams.set('search', searchQuery);  // Adiciona a query de pesquisa, se houver
        }
        if (status !== 'all') {
            url.searchParams.set('status', status);  // Adiciona o status se não for "todos"
        }

        // Requisição para carregar os pedidos da página específica
        fetch(url.toString(), {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'  // Indica que é uma requisição AJAX
            }
        })
        .then(response => response.text())
        .then(data => {
            document.querySelector('.orders-table tbody').innerHTML = data;  // Atualiza a tabela com os pedidos da página

            // Atualiza o controle de página
            currentPage = page;
            currentPageLabel.textContent = `Página ${currentPage}`;

            // Desabilita/ativa os botões de navegação de acordo com a página atual
            prevPageBtn.disabled = (currentPage === 1);
            nextPageBtn.disabled = data.trim() === "";  // Desativa o próximo botão se não houver mais pedidos
        })
        .catch(error => {
            console.error('Erro ao carregar pedidos:', error);  // Exibe erro no console
        });
    }

    // Eventos para navegação entre páginas
    prevPageBtn.addEventListener('click', function() {
        if (currentPage > 1) {
            loadPage(currentPage - 1);  // Carrega a página anterior
        }
    });

    nextPageBtn.addEventListener('click', function() {
        loadPage(currentPage + 1);  // Carrega a próxima página
    });

    // Função para exibir mensagens de sucesso ou erro
    function showMessage(message, type) {
        const messageDiv = document.getElementById('notifications');  // Obtém o elemento de notificação
        messageDiv.textContent = message;  // Define a mensagem
        messageDiv.className = `notification ${type}`;  // Define a classe de estilo para a mensagem
        messageDiv.style.display = 'block';  // Exibe a mensagem

        // Oculta a mensagem após 5 segundos
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }

    // Carregar a primeira página ao carregar a página
    loadPage(currentPage);
});
