const overlay = document.getElementById("modal-ingresso"); // overlay é o modal inteiro
const modal = document.getElementById("modal-ingresso");
const eventoId = document.getElementById("comprar-botao").dataset.evento;


// ABRIR MODAL
function abrirModal() {
    modal.style.display = "flex";
}

// FECHAR MODAL
function fecharModal() {
    modal.style.display = "none";
}

// FECHAR SE CLICAR FORA
overlay.addEventListener("click", function(event) {
    if (event.target === overlay) {  
        modal.style.display = "none";
    }
});

function mostrarAlerta(mensagem) {

    const span = document.getElementById('spanAlert');
    span.textContent = mensagem;
    span.style.display = 'flex';
    
    setTimeout(() => {
        span.style.display = 'none';
    }, 3000);

}

function mostrarConfirmacao() {
    const pop = document.getElementById("popConfirmacao");
   
    pop.classList.add("show");

    // Esconde após 3 segundos
    setTimeout(() => {
        pop.classList.remove("show");
    }, 3000);
    
    setTimeout(() => {
        window.location.reload();
    }, 4000); 
}

function enviarParaBackend(meia, inteira, idEvento) {
    fetch("/user/comprar_ingresso", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            meia: meia,
            inteira: inteira,
            id_evento: idEvento // Inclui o ID do evento
        })
    })
    .then(res => res.json())
    .then(data => console.log("Resposta do servidor:", data))
    .catch(err => console.error(err));
}


document.addEventListener("DOMContentLoaded", () => {

    // Quantidades
    let quantities = {
        meia: 0,
        inteira: 0
    };    
    
    const precoMeiaElement = document.getElementById("preco-ingresso-meia");
    const precoInteiraElement = document.getElementById("preco-ingresso-inteiro");


    let precoMeia = null;
    let precoInteira = null;
    
    if (precoMeiaElement) {
        let textMeia = precoMeiaElement.innerText.trim();
        precoMeia = parseFloat(textMeia.replace("R$", "").trim().replace(",", ".")) || 0;
    }
    
    // 2. Cálculo do Preço Inteira (Lógica de Gratuidade APLICADA AQUI)
    if (precoInteiraElement) {
        let textInteira = precoInteiraElement.innerText.trim();
        
        if (textInteira.toUpperCase() === 'GRATUITO') {
            precoInteira = 0;
        } else {
            // Se não for "GRATUITO", remove "R$", espaços, e converte.
            precoInteira = parseFloat(textInteira.replace("R$", "").trim().replace(",", ".")) || 0;
        }
    }
    
    // Se houver taxas, mantenha aqui
    const prices = {
        meia: precoMeia,
        inteira: precoInteira,
    };
    
    
    const qtyMeiaElement = document.getElementById('qty-meia');
    const qtyInteiraElement = document.getElementById('qty-inteira');
    const totalValueElement = document.getElementById('total-value');

    function calculateTotal() {
        const meiaTotal = quantities.meia * (prices.meia || 0);
        const inteiraTotal = quantities.inteira * (prices.inteira || 0);

        const total = meiaTotal + inteiraTotal;

        totalValueElement.textContent = total.toFixed(2).replace('.', ',');
    }

    // Controle dos botões de quantidade
    document.querySelectorAll('.quantity-btn').forEach(button => {
        button.addEventListener('click', function() {

            // Impedir mais de 1 ingresso
        const type = this.dataset.type;   // "meia" ou "inteira"
        const isPlus = this.classList.contains('plus'); // true = '+', false = '-'

        const totalSelecionado = quantities.meia + quantities.inteira;

        if (isPlus) {
            if (totalSelecionado >= 1) {
                mostrarAlerta("Você só pode comprar 1 ingresso por evento!");
                return;
            }
            quantities[type]++;
        } 
        else if (quantities[type] > 0) {
            quantities[type]--;
        }

        document.getElementById(`qty-${type}`).textContent = quantities[type];
        calculateTotal();
        });
    });

    

    // CANCELAR
    document.getElementById('cancel-btn').addEventListener('click', function() {

        quantities.meia = 0;
        quantities.inteira = 0;
        qtyMeiaElement.textContent = 0;
        qtyInteiraElement.textContent = 0;
        calculateTotal();
    });

    // CONFIRMAR COMPRA
    document.getElementById('confirm-btn').addEventListener('click', function() {

        if (quantities.meia === 0 && quantities.inteira === 0) {
            mostrarAlerta('Selecione pelo menos um ingresso antes de confirmar.');           
            
            return;
    }

    

    // ENVIE os valores ao backend AQUI
    enviarParaBackend(quantities.meia, quantities.inteira, eventoId);

    console.log("Valores enviados ao back:", quantities.meia, quantities.inteira);

    modal.style.display = 'none';
    mostrarConfirmacao();


    quantities.meia = 0;
    quantities.inteira = 0;
    qtyMeiaElement.textContent = 0;
    qtyInteiraElement.textContent = 0;
    calculateTotal();
    
});

    calculateTotal();
});