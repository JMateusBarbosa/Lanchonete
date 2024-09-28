document.addEventListener('DOMContentLoaded', function() {
    const filterStatus = document.getElementById('filter-status');

    // Delegação de eventos para os botões 'Concluir Pedido'
    document.querySelector('.orders-table tbody').addEventListener('click', function(event) {
        if (event.target.classList.contains('btn-complete')) {
            const pedidoId = event.target.getAttribute('data-pedido-id');
            const statusCell = event.target.closest('tr').querySelector('.status-cell');

            fetch(`/concluir-pedido/${pedidoId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    statusCell.textContent = 'Concluído';  // Atualiza o status na tabela
                    showMessage('Pedido concluído com sucesso!', 'success');

                    // Remove a linha da tabela se o filtro aplicado for "Pendente"
                    if (filterStatus.value === 'pending') {
                        const row = statusCell.closest('tr');
                        row.remove();
                    }
                } else {
                    showMessage('Erro ao concluir o pedido: ' + data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Erro ao concluir o pedido:', error);
                showMessage('Erro ao concluir o pedido. Por favor, tente novamente.', 'error');
            });
        }
    });

    // Adicionar evento para o filtro de status
    filterStatus.addEventListener('change', function() {
        const status = filterStatus.value;
        const url = new URL(window.location.href);
        url.searchParams.set('status', status);  // Atualiza o parâmetro de status na URL
    
        fetch(url.toString(), {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(data => {
            // Atualiza apenas as linhas da tabela, e não o layout completo
            document.querySelector('.orders-table tbody').innerHTML = data;
        })
        .catch(error => {
            console.error('Erro ao filtrar os pedidos:', error);
        });
    });

    // Função para exibir mensagens de sucesso ou erro
    function showMessage(message, type) {
        const messageDiv = document.getElementById('notifications');
        messageDiv.textContent = message;
        messageDiv.className = `notification ${type}`;
        messageDiv.style.display = 'block';

        // Oculta a mensagem após 5 segundos
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }
});
