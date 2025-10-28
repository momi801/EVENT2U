let quantities = {
    meia: 0,
    inteira: 0
};

const prices = {
    meia: 25.50,
    meiaTax: 0.50,
    inteira: 50.00,
    inteiraTax: 1.00
};

const qtyMeiaElement = document.getElementById('qty-meia');
const qtyInteiraElement = document.getElementById('qty-inteira');
const totalValueElement = document.getElementById('total-value');

function calculateTotal() {
    const meiaTotal = quantities.meia * (prices.meia + prices.meiaTax);
    const inteiraTotal = quantities.inteira * (prices.inteira + prices.inteiraTax);
    const total = meiaTotal + inteiraTotal;
    
    totalValueElement.textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
}

document.querySelectorAll('.quantity-btn').forEach(button => {
    button.addEventListener('click', function() {
        const type = this.getAttribute('data-type');
        const isPlus = this.classList.contains('plus');
        
        if (isPlus) {
            quantities[type]++;
        } else if (quantities[type] > 0) {
            quantities[type]--;
        }
        
        document.getElementById(`qty-${type}`).textContent = quantities[type];
        calculateTotal();
    });
});

document.getElementById('cancel-btn').addEventListener('click', function() {
    alert('Compra cancelada');
});

document.getElementById('confirm-btn').addEventListener('click', function() {
    if (quantities.meia === 0 && quantities.inteira === 0) {
        alert('Selecione pelo menos um ingresso');
        return;
    }
    
    alert('Compra confirmada! Total: ' + totalValueElement.textContent);
});

calculateTotal();