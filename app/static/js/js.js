//Tela Anotar pedidos
document.addEventListener('DOMContentLoaded', function() {
    const itemCheckboxes = document.querySelectorAll('.item-checkbox');
    const itemQuantities = document.querySelectorAll('.item-quantity');
    const summaryContent = document.getElementById('order-summary-content');
    const confirmButton = document.getElementById('confirm-order');
    const cancelButton = document.getElementById('cancel-order');
    let selectedItems = [];

    itemCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateSummary);
    });

    itemQuantities.forEach(quantityInput => {
        quantityInput.addEventListener('input', updateSummary);
    });

    function getItemPrice(itemId) {
        return fetch(`/get-item-price/${itemId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Erro ao buscar o preço:', data.error);
                    return 0;
                }
                return parseFloat(data.price); // Converte para float
            })
            .catch(error => {
                console.error('Erro:', error);
                return 0; // Retorna 0 caso haja erro
            });
    }

    function updateSummary() {
        selectedItems = [];
        summaryContent.innerHTML = '';

        itemCheckboxes.forEach(async (checkbox) => {
            if (checkbox.checked) {
                const itemId = checkbox.getAttribute('data-item-id');
                const quantityInput = document.querySelector(`.item-quantity[data-item-id="${itemId}"]`);
                const quantity = quantityInput.value;

                const itemPrice = await getItemPrice(itemId); // Aguarda o carregamento do preço
                const totalPrice = (itemPrice * quantity).toFixed(2);

                selectedItems.push({
                    itemId: itemId,
                    quantity: quantity
                });

                summaryContent.innerHTML += `
                    <p>Item ID: ${itemId}, Quantidade: ${quantity}, Preço Total: R$${totalPrice}</p>
                `;
            }
        });

        if (selectedItems.length === 0) {
            summaryContent.innerHTML = '<p>Nenhum item selecionado.</p>';
        }
    }

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
                items: selectedItems
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showMessage('Pedido realizado com sucesso!', 'success');
                clearForm(); // Limpa o formulário após o sucesso
            } else {
                showMessage('Erro ao realizar o pedido: ' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Erro ao realizar o pedido:', error);
            showMessage('Erro ao realizar o pedido. Por favor, tente novamente.', 'error');
        });
    });

    cancelButton.addEventListener('click', function() {
        // Limpa seleções e inputs
        document.querySelectorAll('.item-checkbox').forEach(checkbox => checkbox.checked = false);
        document.querySelectorAll('.item-quantity').forEach(input => input.value = 1);
        summaryContent.innerHTML = '<p>Nenhum item selecionado.</p>';
    });

    // Função para limpar o formulário
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


    // Função para exibir mensagens de sucesso ou erro
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