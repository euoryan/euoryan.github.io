// Throttle function using requestAnimationFrame
const throttle = (func) => {
    let ticking = false;
    return (...args) => {
        if (!ticking) {
            requestAnimationFrame(() => {
                func(...args);
                ticking = false;
            });
            ticking = true;
        }
    };
};

const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
const sections = document.querySelectorAll('section, #contato');
const navItems = document.querySelectorAll('.nav-links a');

navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('show');
});

function getCurrentSection() {
    const scrollPosition = window.scrollY + window.innerHeight / 3; // Ajustado para 1/3 da altura da janela
    let current = '';
    
    // Se estiver próximo do fim da página, considere como estando na seção de contato
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
        return 'contato';
    }

    sections.forEach(section => {
        const sectionTop = section.getBoundingClientRect().top + window.scrollY - 100;
        const sectionBottom = sectionTop + section.offsetHeight;

        if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
            current = section.getAttribute('id') || 'home';
        }
    });

    return window.scrollY < 100 ? 'home' : current;
}

function updateActiveLink() {
    const current = getCurrentSection();
    
    navItems.forEach(link => {
        const href = link.getAttribute('href').replace('#', '');
        link.classList.toggle('active', 
            href === current || (href === '' && current === 'home')
        );
    });
}

// Otimizado event listener para scroll
window.addEventListener('scroll', throttle(updateActiveLink));

// Otimizado smooth scroll
document.querySelectorAll('.nav-links a, .scroll-indicator').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        navLinks.classList.remove('show');
        
        const href = link.getAttribute('href');
        if (href === '#') {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
            return;
        }

        const targetSection = document.querySelector(href);
        if (targetSection) {
            const offsetTop = targetSection.offsetTop - 70;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// Usar passive true para melhor performance em touch events
window.addEventListener('load', updateActiveLink, { passive: true });
window.addEventListener('resize', throttle(updateActiveLink), { passive: true });

document.addEventListener('DOMContentLoaded', function() {
    // Função reutilizável para criar funcionalidade "Mostrar mais/menos"
    function setupToggleCards(containerSelector, cardSelector, perPage = 6) {
        const container = document.querySelector(containerSelector);
        const cards = container.querySelectorAll(cardSelector);
        
        // Se houver mais cards que o limite por página
        if (cards.length > perPage) {
            // Ocultar cards extras inicialmente
            cards.forEach((card, index) => {
                if (index >= perPage) {
                    card.style.display = 'none';
                }
            });
            
            // Criar o botão toggle
            const toggleButton = document.createElement('button');
            toggleButton.className = 'btn';
            toggleButton.textContent = 'Mostrar mais';
            toggleButton.style.cssText = `
                display: block;
                margin: 2rem auto 0;
            `;
            
            // Estado para controlar se os cards estão expandidos
            let isExpanded = false;
            
            // Adicionar funcionalidade ao botão
            toggleButton.addEventListener('click', function() {
                isExpanded = !isExpanded;
                
                cards.forEach((card, index) => {
                    if (index >= perPage) {
                        card.style.display = isExpanded ? 'block' : 'none';
                        
                        // Adicionar animação suave
                        if (isExpanded) {
                            card.style.opacity = '0';
                            card.style.transform = 'translateY(20px)';
                            setTimeout(() => {
                                card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                                card.style.opacity = '1';
                                card.style.transform = 'translateY(0)';
                            }, 50 * (index - perPage + 1)); // Efeito cascata
                        }
                    }
                });
                
                // Atualizar texto do botão
                this.textContent = isExpanded ? 'Mostrar menos' : 'Mostrar mais';
                
                // Role suavemente até o último card visível se estiver recolhendo
                if (!isExpanded) {
                    const lastVisibleCard = cards[perPage - 1];
                    lastVisibleCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }
            });
            
            // Adicionar o botão após o grid
            container.parentNode.insertBefore(toggleButton, container.nextSibling);
        }
    }
    
    // Aplicar para a seção de projetos
    setupToggleCards('.projects-grid', '.project-card', 6);
    
    // Aplicar para a seção de clientes
    setupToggleCards('.clientes-grid', '.cliente-card', 6);
    
    // Aplicar o efeito 3D aos cards de clientes
    const clienteCards = document.querySelectorAll('.cliente-card');
    
    clienteCards.forEach(card => {
        let rafId = null;
        
        const handleMouseMove = (e) => {
            if (rafId) {
                cancelAnimationFrame(rafId);
            }
            
            rafId = requestAnimationFrame(() => {
                const rect = card.getBoundingClientRect();
                const x = ((e.clientX - rect.left) / rect.width) * 100;
                const y = ((e.clientY - rect.top) / rect.height) * 100;
                
                card.style.setProperty('--mouse-x', `${x}%`);
                card.style.setProperty('--mouse-y', `${y}%`);
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = -(e.clientY - rect.top - centerY) / 10;
                const rotateY = (e.clientX - rect.left - centerX) / 10;
                
                card.style.transform = `
                    perspective(1000px) 
                    rotateX(${rotateX}deg) 
                    rotateY(${rotateY}deg) 
                    translateZ(20px)
                `;
            });
        };
        
        const handleMouseLeave = () => {
            if (rafId) {
                cancelAnimationFrame(rafId);
            }
            
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0)';
        };
        
        card.addEventListener('mousemove', handleMouseMove);
        card.addEventListener('mouseleave', handleMouseLeave);
    });
});