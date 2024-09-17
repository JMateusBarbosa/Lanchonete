
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

    function updateSummary() {
        selectedItems = [];
        summaryContent.innerHTML = '';

        itemCheckboxes.forEach(checkbox => {
            if (checkbox.checked) {
                const itemId = checkbox.getAttribute('data-item-id');
                const quantityInput = document.querySelector(`.item-quantity[data-item-id="${itemId}"]`);
                const quantity = quantityInput.value;
                
                // Update selected items array
                selectedItems.push({
                    itemId: itemId,
                    quantity: quantity
                });

                // Assume you have an item list with prices stored somewhere or fetched from the server
                const itemPrice = getItemPrice(itemId); // Replace with actual price retrieval
                const totalPrice = (itemPrice * quantity).toFixed(2);

                summaryContent.innerHTML += `
                    <p>Item ID: ${itemId}, Quantidade: ${quantity}, Preço Total: R$${totalPrice}</p>
                `;
            }
        });

        if (selectedItems.length === 0) {
            summaryContent.innerHTML = '<p>Nenhum item selecionado.</p>';
        }
    }

    function getItemPrice(itemId) {
        // Implement a function to retrieve the item price based on itemId
        // This might be an AJAX call to fetch data from the server
        return 10.00; // Placeholder value
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
                alert('Pedido realizado com sucesso!');
            } else {
                alert('Erro ao realizar o pedido.');
            }
        });
    });
    

    cancelButton.addEventListener('click', function() {
        // Clear selections and inputs
        document.querySelectorAll('.item-checkbox').forEach(checkbox => checkbox.checked = false);
        document.querySelectorAll('.item-quantity').forEach(input => input.value = 1);
        summaryContent.innerHTML = '<p>Nenhum item selecionado.</p>';
    });
    confirmButton.addEventListener('click', function() {
        const customerName = document.getElementById('customer-name').value;
        const tableNumber = document.getElementById('table-number').value;
        const feedback = document.getElementById('feedback').value;
        console.log({
            customer_name: customerName,
            table_number: tableNumber,
            feedback: feedback,
            items: selectedItems
        });
    });
    
});
