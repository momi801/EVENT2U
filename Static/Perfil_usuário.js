document.addEventListener('DOMContentLoaded', function() {
    const profilePicture = document.getElementById('profilePicture');
    const pictureUpload = document.getElementById('pictureUpload');
    const userTypeSelect = document.getElementById('userType');
    const userTypeBadge = document.querySelector('.user-type');
    const switchProfileBtn = document.getElementById('switchProfile');

    // Upload de foto de perfil
    pictureUpload.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                profilePicture.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });

    // Alterar tipo de usuário
    userTypeSelect.addEventListener('change', function() {
        const type = this.value;
        userTypeBadge.textContent = type === 'organizador' ? 'Organizador' : 'Usuário';
        userTypeBadge.className = 'user-type ' + type;
    });

    // Alternar entre perfil de organizador e usuário
    switchProfileBtn.addEventListener('click', function() {
        const currentType = userTypeSelect.value;
        const newType = currentType === 'organizador' ? 'usuario' : 'organizador';
        
        userTypeSelect.value = newType;
        userTypeBadge.textContent = newType === 'organizador' ? 'Organizador' : 'Usuário';
        userTypeBadge.className = 'user-type ' + newType;
        
        switchProfileBtn.textContent = newType === 'organizador'
            ? 'Mudar para Perfil de Usuário'
            : 'Mudar para Perfil de Organizador';
    });

    // Envio do formulário
    document.getElementById('profileForm').addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Perfil atualizado com sucesso!');
    });
});