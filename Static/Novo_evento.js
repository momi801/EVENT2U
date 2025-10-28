document.addEventListener('DOMContentLoaded', function() {
    const imageUpload = document.getElementById('imageUpload');
    const eventImage = document.getElementById('eventImage');
    const imagePreview = document.getElementById('imagePreview');
    const changeImage = document.getElementById('changeImage');

    imageUpload.addEventListener('click', function() {
        eventImage.click();
    });

    eventImage.addEventListener('change', function(e) {
        if (e.target.files && e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.querySelector('img').src = e.target.result;
                imagePreview.style.display = 'block';
                imageUpload.style.display = 'none';
            }
            reader.readAsDataURL(e.target.files[0]);
        }
    });

    changeImage.addEventListener('click', function() {
        imagePreview.style.display = 'none';
        imageUpload.style.display = 'block';
        eventImage.value = '';
    });

    // Adicionar tipo de ingresso
    const addTicketType = document.getElementById('addTicketType');
    const ticketTypes = document.getElementById('ticketTypes');

    addTicketType.addEventListener('click', function() {
        const newTicket = document.createElement('div');
        newTicket.className = 'ticket-type';
        newTicket.innerHTML = `
            <div class="ticket-header">
                <span class="ticket-title">Novo Tipo de Ingresso</span>
                <button type="button" class="remove-ticket"><i class="fas fa-times"></i></button>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Nome do Ingresso</label>
                    <input type="text" class="form-control" value="Novo Ingresso">
                </div>
                <div class="form-group">
                    <label>Preço (R$)</label>
                    <input type="number" class="form-control" min="0" step="0.01" value="0.00">
                </div>
                <div class="form-group">
                    <label>Quantidade</label>
                    <input type="number" class="form-control" min="0" value="50">
                </div>
            </div>
            <div class="form-group">
                <label>Descrição</label>
                <input type="text" class="form-control" placeholder="Descrição opcional do ingresso">
            </div>
        `;
        ticketTypes.appendChild(newTicket);

        newTicket.querySelector('.remove-ticket').addEventListener('click', function() {
            ticketTypes.removeChild(newTicket);
        });
    });

    // Remover ingresso padrão
    document.querySelector('.remove-ticket').addEventListener('click', function() {
        if (document.querySelectorAll('.ticket-type').length > 1) {
            this.closest('.ticket-type').remove();
        } else {
            alert('É necessário ter pelo menos um tipo de ingresso.');
        }
    });

    // Mostrar/ocultar campo de localização
    const eventType = document.getElementById('eventType');
    const locationField = document.getElementById('locationField');

    eventType.addEventListener('change', function() {
        const label = locationField.querySelector('label');
        const input = locationField.querySelector('input');
        if (this.value === 'online') {
            label.textContent = 'Link do Evento Online *';
            input.placeholder = 'https://...';
        } else {
            label.textContent = 'Local do Evento *';
            input.placeholder = 'Endereço completo ou link online';
        }
    });

    // Envio do formulário
    document.getElementById('eventForm').addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Evento criado com sucesso! Redirecionando para a página do evento...');
    });
});