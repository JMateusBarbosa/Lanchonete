document.addEventListener('DOMContentLoaded', function() {
    const completeButtons = document.querySelectorAll('.btn-complete');
    
    completeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const pedidoId = this.getAttribute('data-pedido-id');
            const statusCell = this.closest('tr').querySelector('.status-cell');
            
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
                } else {
                    showMessage('Erro ao concluir o pedido: ' + data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Erro ao concluir o pedido:', error);
                showMessage('Erro ao concluir o pedido. Por favor, tente novamente.', 'error');
            });
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
