document.addEventListener('DOMContentLoaded', function() {

    // ====================== REMOVER INGRESSO ======================
    const removeTicketBtn = document.querySelector('.remove-ticket');
    if (removeTicketBtn) {
        removeTicketBtn.addEventListener('click', function() {
            if (document.querySelectorAll('.ticket-type').length > 1) {
                this.closest('.ticket-type').remove();
            } else {
                alert('É necessário ter pelo menos um tipo de ingresso.');
            }
        });
    }

    // ====================== LOCAL DO EVENTO DINÂMICO ======================
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

    // ====================== ENVIO DO FORMULÁRIO ======================
    document.getElementById('eventForm').addEventListener('submit', function(e) {
        

    });
});

document.addEventListener("DOMContentLoaded", function () {
    const qtdTotal = document.getElementById("qtd-total");
    const qtdInteiro = document.getElementById("qtd-inteiro");
    const qtdMeia = document.getElementById("qtd-meia");

    const precoInteiro = document.getElementById("preco-inteiro");
    const precoMeia = document.getElementById("preco-meia");

    const toggleGratuito = document.getElementById("toggle-gratuito");
    const blocoMeia = document.querySelector(".meia-bloco");

    // ================================
    // Atualizar quantidades baseado no total
    // Inteiro = 60% | Meia = 40%
    // ================================
    function atualizarQuantidades() {
        const total = parseInt(qtdTotal.value) || 0;

        const qtd40 = Math.floor(total * 0.4);
        const qtd60 = total - qtd40;

        qtdMeia.value = qtd40;
        qtdInteiro.value = qtd60;
    }

    qtdTotal.addEventListener("input", atualizarQuantidades);


    // ================================
    // Preço da meia = 50% do inteiro
    // ================================
    precoInteiro.addEventListener("input", function () {
        if (!toggleGratuito.checked) {
            const valor = parseFloat(precoInteiro.value) || 0;
            precoMeia.value = (valor / 2).toFixed(2);
        }
    });


    // ================================
    // Toggle de ingresso gratuito
    // ================================
    toggleGratuito.addEventListener("change", function () {
        if (toggleGratuito.checked) {
            // Evento gratuito → esconder meia-entrada
            blocoMeia.style.display = "none";

            // Preços zerados
            precoInteiro.value = "0.00";
            precoMeia.value = "0.00";

            // Toda quantidade vira inteira
            const total = parseInt(qtdTotal.value) || 0;
            qtdInteiro.value = total;
            qtdMeia.value = 0;

            // Desabilitar campos de preço
            precoInteiro.disabled = true;
            precoMeia.disabled = true;

        } else {
            // Reativar modo pago → mostrar meia-entrada
            blocoMeia.style.display = "block";

            precoInteiro.disabled = false;
            precoMeia.disabled = true; // sempre calculado automaticamente

            atualizarQuantidades();
            precoMeia.value = (parseFloat(precoInteiro.value) / 2 || 0).toFixed(2);
        }
    });


    // Inicializar ao carregar
    atualizarQuantidades();
});



// ========================================================================
// =========================== UPLOAD DE IMAGEM ============================
// ========================================================================

const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('eventImage');
const preview = document.getElementById('preview');
const previewImg = document.getElementById('previewImg');
const changeBtn = document.getElementById('changeImage');

// Clicar na área azul abre o seletor
dropzone.addEventListener('click', () => fileInput.click());

// Quando o usuário seleciona a imagem
fileInput.addEventListener('change', function () {
    const file = this.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function () {
        previewImg.src = reader.result;
        preview.style.display = "block";
        dropzone.style.display = "none";
    };
    reader.readAsDataURL(file);
});

// Trocar a foto
changeBtn.addEventListener('click', () => fileInput.click());


//VALIDA OS CAMPOS DO FORMULARIO DO EVENTO

document.getElementById('eventForm').addEventListener('submit', function(e) {

    const inicio = document.getElementById("eventStartDate").value;
    const fim = document.getElementById("eventEndDate").value;

    // Se algum estiver vazio, não validar ainda
    if (!inicio || !fim) return;

    const dtInicio = new Date(inicio);
    const dtFim = new Date(fim);

    // Validação: início deve ser antes do fim
    if (dtInicio >= dtFim) {
        e.preventDefault();

        mostrarErro("A data de início deve ser anterior à data de término.");
        return;
    }
});

