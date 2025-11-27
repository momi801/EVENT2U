const userInfoContainer = document.querySelector('.user-info.logged-in');
const dropdownMenuLogout = document.querySelector('.dropdown-menu-logout'); 
const logoutLink = document.getElementById('dropDownLogout');
const perfilLink = document.getElementById('dropdownPerfil');


// ===============================================
// 2. Controle de Abertura e Fechamento (Toggle)
// ===============================================

if (userInfoContainer && dropdownMenuLogout) {
    userInfoContainer.addEventListener('click', function(e) {
        
        if (e.target.closest('.dropdown-trigger')) {
            e.stopPropagation();
            dropdownMenuLogout.classList.toggle('show');
        }
    });

    //Prevenir fechamento ao clicar dentro do menu
    dropdownMenuLogout.addEventListener('click', function(e) {
        e.stopPropagation(); 
    });
}

// ===============================================
// 3. Fechar Dropdown ao Clicar Fora
// ===============================================
document.addEventListener('click', function() {
    if (dropdownMenuLogout) {
        dropdownMenuLogout.classList.remove('show');
    }
});


// ===============================================
// 4. Ações de Navegação (Logout e Perfil)
// ===============================================

// 
if (logoutLink) {
    logoutLink.addEventListener('click', function(e) {
        if (confirm('Tem certeza que deseja sair da sua conta?')) {
        } else {
            e.preventDefault();
        }
    });
}

// Link de Perfil (O clique nele deve fechar o menu)
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
    const inputs = form.querySelectorAll("input:not(#email):not(#cpfj");

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
    form.addEventListener("submit", function () {

        const emailInput = document.getElementById('email');
        const cnpjInput = document.getElementById('cnpj');

        if (emailInput) {
            emailInput.disabled = false;
        }
        if (cpfInput) {
            cnpjInput.disabled = false;
        }
    });

    desabilitarCampos();
});