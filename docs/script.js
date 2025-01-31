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
    const scrollPosition = window.scrollY + window.innerHeight / 2;
    let current = '';

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
    const projectCards = document.querySelectorAll('.project-card');
    const projectsGrid = document.querySelector('.projects-grid');
    const PROJECTS_PER_PAGE = 6;
    
    // Se houver mais de 6 projetos
    if (projectCards.length > PROJECTS_PER_PAGE) {
        // Ocultar projetos extras inicialmente
        projectCards.forEach((card, index) => {
            if (index >= PROJECTS_PER_PAGE) {
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
        
        // Estado para controlar se os projetos estão expandidos
        let isExpanded = false;
        
        // Adicionar funcionalidade ao botão
        toggleButton.addEventListener('click', function() {
            isExpanded = !isExpanded;
            
            projectCards.forEach((card, index) => {
                if (index >= PROJECTS_PER_PAGE) {
                    card.style.display = isExpanded ? 'block' : 'none';
                    
                    // Adicionar animação suave
                    if (isExpanded) {
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(20px)';
                        setTimeout(() => {
                            card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                        }, 50);
                    }
                }
            });
            
            // Atualizar texto do botão
            this.textContent = isExpanded ? 'Mostrar menos' : 'Mostrar mais';
            
            // Role suavemente até o último projeto visível se estiver recolhendo
            if (!isExpanded) {
                const lastVisibleProject = projectCards[PROJECTS_PER_PAGE - 1];
                lastVisibleProject.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        });
        
        // Adicionar o botão após a grid de projetos
        projectsGrid.parentNode.insertBefore(toggleButton, projectsGrid.nextSibling);
    }
});