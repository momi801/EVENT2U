const categoriesBtn = document.getElementById('categoriesBtn');
const categoriesMenu = document.getElementById('categoriesMenu');
const categoryItems = document.querySelectorAll('.category-item');
const loginModal = document.getElementById('loginModal');
const openLoginBtn = document.getElementById('openLoginBtn');
const closeLoginModal = document.getElementById('closeLoginModal');
const loginForm = document.getElementById('loginForm');
const loggedOutState = document.getElementById('loggedOutState');
const loggedInState = document.getElementById('loggedInState');
const dropdownMenu = document.getElementById('dropdownMenu');
const logoutBtn = document.getElementById('logoutBtn');
const bannerTicketBtn = document.getElementById('bannerTicketBtn');
const forgotPassword = document.getElementById('forgotPassword');
const goToRegister = document.getElementById('goToRegister');

// Verificar estado de login ao carregar a página
function checkLoginStatus() {
    const isLoggedIn = localStorage.getItem('userLoggedIn') === 'true';
    if (isLoggedIn) {
        loggedOutState.style.display = 'none';
        loggedInState.style.display = 'flex';
        
        // Atualizar informações do usuário
        const userName = localStorage.getItem('userName') || 'Usuário';
        const userEmail = localStorage.getItem('userEmail') || '';
        
        document.querySelector('.user-avatar').textContent = userName.charAt(0).toUpperCase();
        document.querySelector('.user-info div:first-child').textContent = userName;
    } else {
        loggedOutState.style.display = 'flex';
        loggedInState.style.display = 'none';
    }
}

// Controle do Dropdown de Categorias
if (categoriesBtn && categoriesMenu) {
    categoriesBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        categoriesMenu.classList.toggle('show');
    });

    // Fechar dropdown ao clicar fora
    document.addEventListener('click', function() {
        categoriesMenu.classList.remove('show');
    });

    // Prevenir fechamento ao clicar dentro do menu
    categoriesMenu.addEventListener('click', function(e) {
        e.stopPropagation();
    });
}

// Filtro por categoria
categoryItems.forEach(item => {
    item.addEventListener('click', function() {
        const category = this.dataset.category;
        const categoryName = this.textContent.trim();

        categoriesMenu.classList.remove('show');

        // Atualiza texto do botão
        if (category === 'all') {
            categoriesBtn.innerHTML = '📂 Categorias';
        } else {
            const emoji = this.textContent.charAt(0);
            categoriesBtn.innerHTML = `${emoji} ${categoryName}`;
        }

        window.location.href = `/?categoria=${category}`;
    });
});


// Abrir modal de login
openLoginBtn.addEventListener('click', function() {
    loginModal.style.display = 'block';
});

// Fechar modal de login
closeLoginModal.addEventListener('click', function() {
    loginModal.style.display = 'none';
});

// Fechar modal ao clicar fora
window.addEventListener('click', function(event) {
    if (event.target === loginModal) {
        loginModal.style.display = 'none';
    }
});

// Controle do Dropdown (quando logado)
loggedInState.addEventListener('click', function(e) {
    if (e.target.closest('.dropdown-trigger') || e.target === loggedInState) {
        e.stopPropagation();
        dropdownMenu.classList.toggle('show');
    }
});

// Fechar dropdown ao clicar fora
document.addEventListener('click', function() {
    dropdownMenu.classList.remove('show');
});

// Prevenir fechamento ao clicar no dropdown
dropdownMenu.addEventListener('click', function(e) {
    e.stopPropagation();
});

// Função de Logout
logoutBtn.addEventListener('click', function() {
    if (confirm('Tem certeza que deseja sair da sua conta?')) {
        localStorage.removeItem('userLoggedIn');
        localStorage.removeItem('userEmail');
        localStorage.removeItem('userName');
        
        checkLoginStatus();
        alert('Você saiu da sua conta com sucesso!');
    }
});

// Navegação do dropdown
document.querySelectorAll('.dropdown-item:not(.logout-btn)').forEach(item => {
    item.addEventListener('click', function() {
        const action = this.textContent.trim();
        switch(action) {
            case '👤 Meu Perfil':
                if (localStorage.getItem('userLoggedIn') === 'true') {
                    window.location.href = 'perfil.html';
                } else {
                    alert('Faça login para acessar seu perfil.');
                    loginModal.style.display = 'block';
                }
                break;
            case '🎫 Meus Ingressos':
                if (localStorage.getItem('userLoggedIn') === 'true') {
                    window.location.href = 'ingressos.html';
                } else {
                    alert('Faça login para ver seus ingressos.');
                    loginModal.style.display = 'block';
                }
                break;
        }
        dropdownMenu.classList.remove('show');
    });
});

// Botão de compra no banner
bannerTicketBtn.addEventListener('click', function() {
    if (localStorage.getItem('userLoggedIn') === 'true') {
        alert('Redirecionando para compra de ingressos do Taylor Swift - The Eras Tour');
    } else {
        alert('Faça login para comprar ingressos.');
        loginModal.style.display = 'block';
    }
});

// Botões de compra nos cards
document.querySelectorAll('.btn-primary:not(.search-btn):not(.btn-full)').forEach(btn => {
    btn.addEventListener('click', function() {
        if (localStorage.getItem('userLoggedIn') === 'true') {
            const eventCard = this.closest('.event-card');
            const eventName = eventCard?.querySelector('.event-name')?.textContent || 'Evento';
            alert(`Redirecionando para compra de ingressos: ${eventName}`);
        } else {
            alert('Faça login para comprar ingressos.');
            loginModal.style.display = 'block';
        }
    });
});


// Cadastre-se agora
goToRegister.addEventListener('click', function(e) {
    e.preventDefault();
    alert('Redirecionando para página de cadastro...');
});

document.querySelector('.search-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        document.querySelector('.search-btn').click();
    }
});

// Filtros de categoria
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.filter-btn').forEach(b => {
            b.classList.remove('active');
        });
        this.classList.add('active');
        const category = this.textContent;
        alert(`Filtrando por: ${category}`);
    });
});
checkLoginStatus();