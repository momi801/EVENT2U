// ------------------ Formatação CPF ------------------
document.getElementById('cpf').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');

    // impede mais de 11 dígitos
    if (value.length > 11) value = value.slice(0, 11);

    if (value.length > 9) {
        value = value.replace(/^(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
    } else if (value.length > 6) {
        value = value.replace(/^(\d{3})(\d{3})(\d{3})/, '$1.$2.$3');
    } else if (value.length > 3) {
        value = value.replace(/^(\d{3})(\d{3})/, '$1.$2');
    }

    e.target.value = value;
});

// ------------------ Formatação Telefone ------------------
document.getElementById('phone').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');

    // limita a 11 números
    if (value.length > 11) value = value.slice(0, 11);

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

// ------------------ Validação da Data (não pode ser futura) ------------------
function validarDataNascimento() {
    const campoData = document.getElementById("birth-date");

    const hoje = new Date();
    hoje.setHours(0,0,0,0);

    const dataSel = new Date(campoData.value);
    dataSel.setHours(0,0,0,0);

    if (!campoData.value) {
        campoData.style.borderColor = "";
        return;
    }

    if (dataSel > hoje) {
        campoData.style.borderColor = "red";
    } else {
        campoData.style.borderColor = "green";
    }
}

document.getElementById("birth-date").addEventListener("input", validarDataNascimento);
