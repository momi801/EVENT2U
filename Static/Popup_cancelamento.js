document.addEventListener('DOMContentLoaded', function() {
    const cancelBtn = document.querySelector('.btn-cancel');
    const confirmBtn = document.querySelector('.btn-confirm');
    const popup = document.querySelector('.popup-overlay');

    cancelBtn.addEventListener('click', function() {
        alert('Cancelamento abortado. Seus ingressos foram mantidos.');
        popup.style.display = 'none'; // fecha o popup
    });

    confirmBtn.addEventListener('click', function() {
        alert('Cancelamento confirmado! O reembolso será processado em breve.');
        popup.style.display = 'none'; // fecha o popup
    });
});