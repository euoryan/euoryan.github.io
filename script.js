const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');

navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('show');
});

document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('show');
        document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
        link.classList.add('active');
    });
});

document.querySelector('.nav-links a:first-child').classList.add('active');

// Adiciona evento de clique para o botão de seta
document.querySelector('.scroll-indicator').addEventListener('click', () => {
    const targetSection = document.querySelector('#projetos');
    targetSection.scrollIntoView({ behavior: 'smooth' });
});