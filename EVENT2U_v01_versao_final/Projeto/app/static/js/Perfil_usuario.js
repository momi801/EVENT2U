
const userInfoContainer = document.querySelector('.user-avatar.logged-in');
const dropdownMenuLogout = document.querySelector('.dropdown-menu-logout'); 
const logoutLink = document.getElementById('dropDownLogout');
const perfilLink = document.getElementById('dropdownPerfil');


// ===============================================
// Controle de Abertura e Fechamento (Toggle)
// ===============================================

if (userInfoContainer && dropdownMenuLogout) {
    
    userInfoContainer.addEventListener('click', function(e) {
        if (e.target.closest('.dropdown-trigger')) {
            e.stopPropagation();
            dropdownMenuLogout.classList.toggle('show');
        }
    });

    dropdownMenuLogout.addEventListener('click', function(e) {
        e.stopPropagation();
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



// Link de Perfil
if (perfilLink) {
    perfilLink.addEventListener('click', function() {
        if (dropdownMenuLogout) {
            dropdownMenuLogout.classList.remove('show');
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {        
    
    const btnAlterar = document.getElementById("altera");
    const btnSalvar = document.getElementById("salvar");
    const btnCancelar = document.getElementById("cancela");
    const form = document.getElementById("profileForm");
    const inputs = form.querySelectorAll("input:not([type='file']):not(#email):not(#cpf");

    let valoresOriginais = {}; 

    // =============================
    //   Funções de estado
    // =============================
    
    function desabilitarCampos() {
        inputs.forEach(input => input.disabled = true);        

        btnAlterar.style.display = "inline-block";
        btnSalvar.style.display = "none";
        btnCancelar.style.display = "none";
    }

    function habilitarCampos() {
        inputs.forEach(input => input.disabled = false);

        btnAlterar.style.display = "none";
        btnSalvar.style.display = "inline-block";
        btnCancelar.style.display = "inline-block";
    }

    function salvarValoresOriginais() {
        valoresOriginais = {};
        inputs.forEach(input => valoresOriginais[input.id] = input.value);
    }

    function restaurarValores() {
        inputs.forEach(input => {
            input.value = valoresOriginais[input.id];
        });
    }

    // =============================
    //   Botões
    // =============================

    btnAlterar.addEventListener("click", function () {
        salvarValoresOriginais();
        habilitarCampos();
    });

    btnCancelar.addEventListener("click", function () {
        restaurarValores();
        desabilitarCampos();
    });

    // Envio REAL para o backend
    form.addEventListener("submit", function (e) {
        
        const emailInput = document.getElementById('email');
        const cpfInput = document.getElementById('cpf');

        if (emailInput) {
            emailInput.disabled = false;
        }
        if (cpfInput) {
            cpfInput.disabled = false;
        }
    });

    // Inicial
    desabilitarCampos();
});