document.getElementById('cnpj').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    
    if (value.length <= 14) {
        if (value.length > 12) {
            value = value.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
        } else if (value.length > 8) {
            value = value.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})/, '$1.$2.$3/$4');
        } else if (value.length > 5) {
            value = value.replace(/^(\d{2})(\d{3})(\d{3})/, '$1.$2.$3');
        } else if (value.length > 2) {
            value = value.replace(/^(\d{2})(\d{3})/, '$1.$2');
        }
        
        e.target.value = value;
    }
});

document.getElementById('phone').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    
    if (value.length <= 11) {
        if (value.length > 10) {
            value = value.replace(/^(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
        } else if (value.length > 6) {
            value = value.replace(/^(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
        } else if (value.length > 2) {
            value = value.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
        } else if (value.length > 0) {
            value = value.replace(/^(\d{0,2})/, '($1');
        }
        
        e.target.value = value;
    }
});

// ------------------ Verificação das Senhas ------------------
function validarSenhas() {
    const senha = document.getElementById("password").value;
    const confirmar = document.getElementById("confirm-password").value;
    const msgIgualdade = document.getElementById("senha-msg");
    const campoConfirm = document.getElementById("confirm-password");

    if (!senha || !confirmar) {
        msgIgualdade.textContent = "";
        campoConfirm.style.borderColor = "";
        return;
    }

    if (senha !== confirmar) {
        campoConfirm.style.borderColor = "red";
        msgIgualdade.textContent = "As senhas não coincidem.";
        msgIgualdade.style.color = "red";
    } else {
        campoConfirm.style.borderColor = "green";
        msgIgualdade.textContent = "";
    }
}

document.getElementById("password").addEventListener("input", validarSenhas);
document.getElementById("confirm-password").addEventListener("input", validarSenhas);
