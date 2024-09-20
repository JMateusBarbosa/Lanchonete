document.getElementById('filter-status').addEventListener('change', updateOrders);
document.getElementById('filter-time').addEventListener('change', updateOrders);
document.getElementById('search').addEventListener('input', updateOrders);

function updateOrders() {
    const status = document.getElementById('filter-status').value;
    const time = document.getElementById('filter-time').value;
    const search = document.getElementById('search').value;

    const url = `/acompanhar_pedidos?status=${status}&time=${time}&search=${search}`;

    fetch(url)
        .then(response => response.text())
        .then(html => {
            document.querySelector('.orders-table tbody').innerHTML = html;
            assignStatusToggleEvents();  // Reatribuir eventos aos botões
        })
        .catch(error => {
            console.error('Erro ao atualizar pedidos:', error);
        });
}

function assignStatusToggleEvents() {
    document.querySelectorAll('.status-toggle').forEach(button => {
        button.addEventListener('click', function() {
            const pedidoId = this.closest('.order-row').dataset.pedidoId;
            const novoStatus = this.dataset.novoStatus;

            fetch('/atualizar_status_pedido', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `pedido_id=${pedidoId}&status=${novoStatus}`,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Status atualizado com sucesso.');
                    updateOrders();
                } else {
                    alert('Erro ao atualizar status: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Erro ao atualizar status:', error);
            });
        });
    });
}

// Chamada inicial para atribuir os eventos
assignStatusToggleEvents();

setInterval(updateOrders, 10000);
