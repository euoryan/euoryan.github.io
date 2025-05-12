document.addEventListener('DOMContentLoaded', function() {
    const footerUrl = 'https://raw.githubusercontent.com/euoryan/euoryan.github.io/refs/heads/main/assets/pages/footer.html';

    function loadFooter() {
        fetch(footerUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar o footer');
                }
                return response.text();
            })
            .then(html => {
                const footerContainer = document.createElement('div');
                footerContainer.innerHTML = html.trim();

                const newFooter = footerContainer.querySelector('footer');

                if (newFooter) {
                    const existingFooter = document.querySelector('footer');
                    if (existingFooter) {
                        existingFooter.parentNode.replaceChild(newFooter, existingFooter);
                    } else {
                        document.body.appendChild(newFooter);
                    }
                } else {
                    throw new Error('Nenhum footer encontrado');
                }
            })
            .catch(error => {
                console.error('Erro ao carregar o footer:', error);
                
                const fallbackFooter = document.createElement('footer');
                fallbackFooter.className = 'footer';
                fallbackFooter.innerHTML = `
                    <div class="footer-container">
                        <div class="footer-rights">
                            <span>© 2024 por Ryan</span>
                        </div>
                    </div>
                `;
                
                const existingFooter = document.querySelector('footer');
                if (existingFooter) {
                    existingFooter.parentNode.replaceChild(fallbackFooter, existingFooter);
                } else {
                    document.body.appendChild(fallbackFooter);
                }
            });
    }

    loadFooter();
});