// Performance Manager
const PerformanceManager = {
    // Cache de elementos DOM
    elements: new Map(),
    // Configurações
    config: {
      throttleDelay: 16, // ~60fps
      scrollMargin: 100,
      animationDuration: 300
    },
    
    init() {
      // Cache inicial de elementos importantes
      this.cacheElements();
      // Inicializa otimizações
      this.setupIntersectionObserver();
      this.setupScrollOptimization();
      this.setupEventListeners();
      this.setupLazyLoading();
    },
  
    cacheElements() {
      // Cache elementos frequentemente acessados
      this.elements.set('nav', document.querySelector('nav'));
      this.elements.set('sections', Array.from(document.querySelectorAll('section')));
      this.elements.set('projectCards', Array.from(document.querySelectorAll('.project-card')));
    },
  
    setupIntersectionObserver() {
      // Observer para animações de entrada
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              requestAnimationFrame(() => {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
              });
              observer.unobserve(entry.target);
            }
          });
        },
        {
          threshold: 0.1,
          rootMargin: '50px'
        }
      );
  
      // Aplica o observer nos elementos que precisam de animação
      this.elements.get('projectCards').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.3s ease-out, transform 0.3s ease-out';
        observer.observe(card);
      });
    },
  
    setupScrollOptimization() {
      // Usa requestAnimationFrame para otimizar scroll
      let ticking = false;
      let lastScrollY = window.scrollY;
  
      window.addEventListener('scroll', () => {
        if (!ticking) {
          requestAnimationFrame(() => {
            this.handleScroll(lastScrollY);
            ticking = false;
          });
          ticking = true;
        }
        lastScrollY = window.scrollY;
      }, { passive: true });
    },
  
    handleScroll(lastScrollY) {
      // Aplica classe na nav baseado na direção do scroll
      const nav = this.elements.get('nav');
      const currentScroll = window.scrollY;
      
      if (currentScroll > lastScrollY) {
        nav.style.transform = 'translateY(-100%)';
      } else {
        nav.style.transform = 'translateY(0)';
      }
    },
  
    setupEventListeners() {
      // Delegation de eventos para melhor performance
      document.body.addEventListener('click', (e) => {
        const target = e.target.closest('a[href^="#"]');
        if (target) {
          e.preventDefault();
          this.smoothScroll(target.getAttribute('href').slice(1));
        }
      });
  
      // Otimiza resize com debounce
      let resizeTimeout;
      window.addEventListener('resize', () => {
        if (resizeTimeout) clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
          this.handleResize();
        }, 150);
      }, { passive: true });
    },
  
    setupLazyLoading() {
      // Lazy loading de imagens
      const imageObserver = new IntersectionObserver(
        (entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              const img = entry.target;
              if (img.dataset.src) {
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
              }
            }
          });
        },
        {
          rootMargin: '50px 0px',
          threshold: 0.1
        }
      );
  
      document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
      });
    },
  
    smoothScroll(targetId) {
      const target = document.getElementById(targetId);
      if (!target) return;
  
      const targetPosition = target.getBoundingClientRect().top + window.pageYOffset;
      const startPosition = window.pageYOffset;
      const distance = targetPosition - startPosition;
      const duration = this.config.animationDuration;
      let start = null;
  
      const animation = (currentTime) => {
        if (start === null) start = currentTime;
        const timeElapsed = currentTime - start;
        const progress = Math.min(timeElapsed / duration, 1);
  
        window.scrollTo(0, startPosition + distance * this.easeOutCubic(progress));
  
        if (timeElapsed < duration) {
          requestAnimationFrame(animation);
        }
      };
  
      requestAnimationFrame(animation);
    },
  
    easeOutCubic(t) {
      return 1 - Math.pow(1 - t, 3);
    },
  
    handleResize() {
      // Recalcula posições se necessário
      this.cacheElements();
    }
  };
  
  // Inicialização
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => PerformanceManager.init());
  } else {
    PerformanceManager.init();
  }