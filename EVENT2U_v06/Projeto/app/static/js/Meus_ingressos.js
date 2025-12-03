// Mapeia o contêiner clicável (o <li> ou o .user-info)
const userInfoContainer = document.querySelector('.user-avatar.logged-in');
const dropdownMenuLogout = document.querySelector('.dropdown-menu-logout'); 
const logoutLink = document.getElementById('dropDownLogout');
const perfilLink = document.getElementById('dropdownPerfil');

if (userInfoContainer && dropdownMenuLogout) {

    userInfoContainer.addEventListener('click', function(e) {
        if (e.target.closest('.user-avatar')) {
            e.stopPropagation();
            dropdownMenuLogout.classList.toggle('show');
        }
    });

    dropdownMenuLogout.addEventListener('click', function(e) {
        e.stopPropagation();
    });
}

document.addEventListener('click', function(e) {
    if (!userInfoContainer.contains(e.target) && !dropdownMenuLogout.contains(e.target)) {
        dropdownMenuLogout.classList.remove('show');
    }
});




// ===============================================
// CANCELAMENTO DE INGRESSOS
// ===============================================
document.querySelectorAll('.btn-cancel').forEach(button => {
    button.addEventListener('click', function() {
        const ticketCard = this.closest('.ticket-card');
        const eventName = ticketCard.querySelector('.event-name').textContent;
        
        if (confirm(`Tem certeza que deseja cancelar sua inscrição para "${eventName}"?`)) {                      
            
            const statusBadge = ticketCard.querySelector('.status-badge');
            statusBadge.textContent = 'Cancelado';
            statusBadge.className = 'status-badge status-canceled';
            
            // Remove o botão de cancelar
            this.remove();
            
            alert('Inscrição cancelada com sucesso!');
        }
    });
});
