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