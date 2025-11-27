// ===============================================
// 1. Mapeamento de Elementos (Nova Página)
// ===============================================

// Mapeia o contêiner clicável (o <li> ou o .user-info)
const userInfoContainer = document.querySelector('.user-info.logged-in');

// Mapeia o menu que deve ser exibido/ocultado
const dropdownMenuLogout = document.querySelector('.dropdown-menu-logout'); 

// Mapeia o link de logout (usando o ID que você deu)
const logoutLink = document.getElementById('dropDownLogout');

// Mapeia o link de perfil (usando o ID que você deu)
const perfilLink = document.getElementById('dropdownPerfil');


// ===============================================
// 2. Controle de Abertura e Fechamento (Toggle)
// ===============================================

if (userInfoContainer && dropdownMenuLogout) {
    // Abertura/Fechamento: Ao clicar no contêiner do usuário (ou no avatar)
    userInfoContainer.addEventListener('click', function(e) {
        
        if (e.target.closest('.dropdown-trigger')) {
            e.stopPropagation(); // Impede que o clique suba para o documento
            // Adiciona ou remove a classe 'show' no menu de logout
            dropdownMenuLogout.classList.toggle('show');
        }
    });

    // Prevenir fechamento ao clicar dentro do menu
    dropdownMenuLogout.addEventListener('click', function(e) {
        e.stopPropagation(); // O clique dentro do menu não deve fechar o menu
    });
}

// ===============================================
// Fechar Dropdown ao Clicar Fora
// ===============================================
document.addEventListener('click', function() {
    // Fecha o menu se ele estiver aberto
    if (dropdownMenuLogout) {
        dropdownMenuLogout.classList.remove('show');
    }
});


// ===============================================
// Ações de Navegação (Logout e Perfil)
// ===============================================


// Link de Perfil (O clique nele deve fechar o menu)
if (perfilLink) {
    perfilLink.addEventListener('click', function() {
        if (dropdownMenuLogout) {
            dropdownMenuLogout.classList.remove('show');
        }
    });
}


//===============================================
// CONFIRMACAO DE CANCELAMENTO DE EVENTO
//===============================================

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('confirmation-modal');
    const closeModal = modal.querySelector('.close-button');
    const confirmBtn = document.getElementById('modal-confirm-btn');
    const cancelBtn = document.getElementById('modal-cancel-btn');
    let eventoIdModal = null;

    // DROPDOWN TOGGLE
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const dropdown = button.closest('.dropdown');
            dropdown.classList.toggle('show');
        });
    });

    // FECHAR DROPDOWN SE CLICAR FORA
    document.addEventListener('click', (e) => {
        const openDropdowns = document.querySelectorAll('.dropdown.show');
        openDropdowns.forEach(dropdown => {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove('show');
            }
        });
    });

    // ABRIR MODAL AO CLICAR EM CANCELAR
    document.querySelectorAll('.cancelar-evento').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            eventoIdModal = btn.dataset.eventoId;
            modal.style.display = 'block';
        });
    });

    // FECHAR MODAL
    const fecharModal = () => modal.style.display = 'none';
    closeModal.onclick = fecharModal;
    cancelBtn.onclick = fecharModal;
    window.onclick = (e) => { if(e.target == modal) fecharModal(); };

    // CONFIRMAR CANCELAMENTO
    confirmBtn.addEventListener('click', async () => {
        if (!eventoIdModal) return;

        try {
            const res = await fetch(`/admin/atualizar_status/${eventoIdModal}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ status: 'cancelado' })
            });

            const data = await res.json();

            if (data.sucesso) {
                const eventCard = document.querySelector(`.cancelar-evento[data-evento-id='${eventoIdModal}']`).closest('.event-card');
                const statusSpan = eventCard.querySelector('.event-status');
                
                const eventActionsDiv = eventCard.querySelector('.event-actions');
                const dropdownContainer = eventActionsDiv.querySelector('.dropdown');
                
                // Atualiza o status
                statusSpan.textContent = 'cancelado';
                // Define a classe CSS correta para 'cancelado'
                statusSpan.className = 'event-status status-draft'; 

                // 3Remove o dropdown e adiciona o botão de relatório
                if(dropdownContainer) {
                    dropdownContainer.remove(); 
                }                
                
                eventActionsDiv.classList.remove('dropdown'); 

                eventActionsDiv.innerHTML += '<button class="btn btn-secondary" disabled>Ver Relatório</button>';                

                // Fecha modal
                fecharModal();
                window.location.reload();
            } 
        }
        catch (err) {
            console.error('Erro ao cancelar evento:', err);
        }
    });
});