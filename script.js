const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
const sections = document.querySelectorAll('section, #contato');
const navItems = document.querySelectorAll('.nav-links a');

navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('show');
});

// Função para verificar qual seção está visível
function getCurrentSection() {
    let current = '';
    const scrollPosition = window.scrollY + window.innerHeight / 2; // Ponto médio da janela

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100; // Ajuste do offset para melhor detecção
        const sectionBottom = sectionTop + section.offsetHeight;

        if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
            current = section.getAttribute('id') || 'home';
        }
    });

    // Se estiver no topo da página, ative o link Home
    if (window.scrollY < 100) {
        current = 'home';
    }
    
    return current;
}

// Atualiza o link ativo baseado na seção atual
function updateActiveLink() {
    const current = getCurrentSection();
    
    navItems.forEach(link => {
        link.classList.remove('active');
        const href = link.getAttribute('href').replace('#', '');
        if (href === current || (href === '' && current === 'home')) {
            link.classList.add('active');
        }
    });
}

// Adiciona evento de scroll com throttle para melhor performance
let scrollTimeout;
window.addEventListener('scroll', () => {
    if (!scrollTimeout) {
        scrollTimeout = setTimeout(() => {
            updateActiveLink();
            scrollTimeout = null;
        }, 100);
    }
});

// Eventos de clique nos links da navegação
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        navLinks.classList.remove('show');
        
        if (link.getAttribute('href') === '#') {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        } else {
            const targetId = link.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 70; // Ajuste para compensar a navbar
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        }
    });
});

// Adiciona evento de clique para o botão de seta
document.querySelector('.scroll-indicator').addEventListener('click', () => {
    const targetSection = document.querySelector('#projetos');
    const offsetTop = targetSection.offsetTop - 70; // Ajuste para compensar a navbar
    window.scrollTo({
        top: offsetTop,
        behavior: 'smooth'
    });
});

// Inicializa o link ativo
updateActiveLink();

// Atualiza também quando a página é carregada
window.addEventListener('load', updateActiveLink);

// Atualiza quando a janela é redimensionada
window.addEventListener('resize', updateActiveLink);