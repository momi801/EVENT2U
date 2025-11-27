document.addEventListener('DOMContentLoaded', function() {
    const abrirPopupBtns = document.querySelectorAll('.abrir-popup');
    const popup = document.querySelector('.popup-overlay');

    const cancelBtn = document.querySelector('.btn-cancel-popup');
    const confirmBtn = document.querySelector('.btn-confirm-popup');

    // --- ABRIR POPUP ---
    abrirPopupBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            popup.style.display = 'flex';
        });
    });

    // --- BOTÃO MANTER INGRESSO ---
    cancelBtn.addEventListener('click', function() {
        popup.style.display = 'none';
    });

    // --- BOTÃO CONFIRMAR CANCELAMENTO ---
    confirmBtn.addEventListener('click', function() {
        
        popup.style.display = 'none';
    });

});