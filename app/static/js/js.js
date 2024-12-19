// Tela Anotar Pedidos - Funções para gerenciar a seleção de itens, resumo do pedido e confirmação de pedidos
// Este arquivo lida com a interação do usuário na tela de anotação de pedidos.
// Ele permite que os itens sejam selecionados, suas quantidades sejam ajustadas, o resumo do pedido seja atualizado
// dinamicamente e, ao confirmar, o pedido seja enviado ao servidor com os detalhes do cliente e do pedido.

document.addEventListener('DOMContentLoaded', function() {
    const itemCheckboxes = document.querySelectorAll('.item-checkbox');  // Checkbox para selecionar os itens
    const itemQuantities = document.querySelectorAll('.item-quantity');  // Campos para definir as quantidades
    const summaryContent = document.getElementById('order-summary-content');  // Área para exibir o resumo do pedido
    const confirmButton = document.getElementById('confirm-order');  // Botão para confirmar o pedido
    let selectedItems = [];  // Lista de itens selecionados no pedido
    let totalPedido = 0.0;  // Variável para armazenar o total do pedido

    // Adiciona eventos para atualizar o resumo ao selecionar ou alterar a quantidade de itens
    itemCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateSummary);
    });

    itemQuantities.forEach(quantityInput => {
        quantityInput.addEventListener('input', updateSummary);
    });

    // Função para obter o preço de um item a partir do servidor
    function getItemPrice(itemId) {
        return fetch(`/get-item-price/${itemId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Erro ao buscar o preço:', data.error);
                    return 0;
                }
                return parseFloat(data.price);  // Retorna o preço do item em formato numérico
            })
            .catch(error => {
                console.error('Erro:', error);
                return 0;  // Retorna 0 em caso de erro
            });
    }

    // Função assíncrona para atualizar o resumo do pedido com os itens selecionados e seus preços
    async function updateSummary() {
        selectedItems = [];  // Resetar a lista de itens selecionados
        totalPedido = 0.0;  // Resetar o total antes de recalcular
        summaryContent.innerHTML = '';  // Limpar conteúdo do resumo

        for (let checkbox of itemCheckboxes) {
            if (checkbox.checked) {  // Se o item estiver marcado
                const itemId = checkbox.getAttribute('data-item-id');  // ID do item
                const quantityInput = document.querySelector(`.item-quantity[data-item-id="${itemId}"]`);
                const quantity = quantityInput.value;  // Quantidade do item

                const itemPrice = await getItemPrice(itemId);  // Obter o preço do item
                const totalPrice = (itemPrice * quantity).toFixed(2);  // Calcular o preço total para o item

                totalPedido += parseFloat(totalPrice);  // Adicionar ao total do pedido

                selectedItems.push({
                    itemId: itemId,
                    quantity: quantity
                });

                summaryContent.innerHTML += `
                    <p>Item ID: ${itemId}, Quantidade: ${quantity}, Preço Total: R$${totalPrice}</p>
                `;
            }
        }

        // Exibe o total do pedido ou uma mensagem se nenhum item for selecionado
        if (selectedItems.length === 0) {
            summaryContent.innerHTML = '<p>Nenhum item selecionado.</p>';
        } else {
            summaryContent.innerHTML += `<p><strong>Total do Pedido: R$${totalPedido.toFixed(2)}</strong></p>`;
        }
    }

    // Evento para confirmar o pedido e enviá-lo para o servidor
    confirmButton.addEventListener('click', function() {
        const customerName = document.getElementById('customer-name').value || null;
        const tableNumber = document.getElementById('table-number').value || null;
        const feedback = document.getElementById('feedback').value;
    
        fetch('/anotar-pedido', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            },
            body: JSON.stringify({
                customer_name: customerName,
                table_number: tableNumber,
                feedback: feedback,
                items: selectedItems,
                total_pedido: totalPedido  // Inclui o total do pedido na requisição
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showMessage('Pedido realizado com sucesso!', 'success');
                clearForm();  // Limpa o formulário após a confirmação
            } else {
                showMessage('Erro ao realizar o pedido: ' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Erro ao realizar o pedido:', error);
            showMessage('Erro ao realizar o pedido. Por favor, tente novamente.', 'error');
        });
    });

    // Evento para cancelar a seleção de itens e limpar o resumo
    cancelButton.addEventListener('click', function() {
        // Limpa seleções e inputs
        document.querySelectorAll('.item-checkbox').forEach(checkbox => checkbox.checked = false);
        document.querySelectorAll('.item-quantity').forEach(input => input.value = 1);
        summaryContent.innerHTML = '<p>Nenhum item selecionado.</p>';
    });

    // Função para limpar o formulário após o envio ou cancelamento
    function clearForm() {
        document.getElementById('customer-name').value = '';
        document.getElementById('table-number').value = '';
        document.getElementById('feedback').value = '';
        document.querySelectorAll('.item-checkbox').forEach(checkbox => {
            checkbox.checked = false;
        });
        document.querySelectorAll('.item-quantity').forEach(input => {
            input.value = 1;
        });
        summaryContent.innerHTML = '<p>Nenhum item selecionado.</p>';
        selectedItems = [];
    }

    // Função para exibir mensagens de sucesso ou erro ao usuário
    function showMessage(message, type) {
        const messageDiv = document.getElementById('message');
        messageDiv.textContent = message;
        messageDiv.className = type;
        messageDiv.style.display = 'block';
    
        // Oculta a mensagem após 5 segundos
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }
});
