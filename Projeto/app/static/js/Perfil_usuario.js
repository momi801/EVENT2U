// Mapeia o contêiner clicável (o <li> ou o .user-info)
const userInfoContainer = document.querySelector('.user-avatar.logged-in');

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
    // 💡 Abertura/Fechamento: Ao clicar no contêiner do usuário (ou no avatar)
    userInfoContainer.addEventListener('click', function(e) {
        // Verifica se o clique foi dentro do trigger, mas não em um link que vá navegar imediatamente
        if (e.target.closest('.dropdown-trigger')) {
            e.stopPropagation(); // Impede que o clique suba para o documento
            // Adiciona ou remove a classe 'show' no menu de logout
            dropdownMenuLogout.classList.toggle('show');
        }
    });

    // 💡 Prevenir fechamento ao clicar dentro do menu
    dropdownMenuLogout.addEventListener('click', function(e) {
        e.stopPropagation(); // O clique dentro do menu não deve fechar o menu
    });
}

// ===============================================
// 3. Fechar Dropdown ao Clicar Fora
// ===============================================
document.addEventListener('click', function() {
    // Fecha o menu se ele estiver aberto
    if (dropdownMenuLogout) {
        dropdownMenuLogout.classList.remove('show');
    }
    // NOTA: Se você ainda usa o menu da tela inicial (dropdownMenu) neste JS, 
    // precisará adicionar a mesma linha para ele.
});



// ===============================================
// 4. Ações de Navegação (Logout e Perfil)
// ===============================================

// 💡 Link de Logout (Ele já tem o href para auth.logout, este código é opcional)
if (logoutLink) {
    logoutLink.addEventListener('click', function(e) {
        if (confirm('Tem certeza que deseja sair da sua conta?')) {
            
        } else {
            e.preventDefault(); // Impede a navegação se o usuário cancelar
        }
    });
}

// 💡 Link de Perfil (O clique nele deve fechar o menu)
if (perfilLink) {
    perfilLink.addEventListener('click', function() {
        // Garante que o menu feche após a navegação (se a navegação não for imediata)
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
        
        // IMPORTANTE: Não chame desabilitarCampos() aqui. Deixe o form ser enviado.
        // A desativação deve ocorrer no retorno do Flask (após o redirect).
    });

    // Inicial
    desabilitarCampos();
});