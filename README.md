# euoryan.com

Site pessoal publicado em [euoryan.com](https://euoryan.com) pelo GitHub Pages.

HTML, CSS e JavaScript puros, sem build e sem dependências.

## Estrutura

```
index.html            home
contato/              contato
politica/             política de privacidade
termos/               termos de uso
restrito/             aviso de projeto com acesso restrito
github/               artigo sobre a história do GitHub
404.html              página de erro de todo o domínio euoryan.com
assets/
  css/style.css       estilos da home e das páginas internas
  js/script.js        comportamento da home e das páginas internas
  fonts/              fontes da home
  images/             favicon de e-mail (BIMI) e imagens de projetos
  pages/footer.html   rodapé compartilhado, carregado por outros projetos
favicon.ico, favicon.svg, apple-touch-icon.png
CNAME                 domínio do GitHub Pages
```

## Rodar localmente

```
python3 -m http.server 8080 --bind 127.0.0.1
```

Abrir http://127.0.0.1:8080.

## Caminhos que não podem mudar

Outros projetos dependem destes arquivos pelo endereço:

- `assets/pages/footer.html`: rodapé baixado por outros sites via raw.githubusercontent.com. Precisa funcionar em qualquer site, claro ou escuro, sem CSS de quem o recebe.
- `404.html`: página de erro de todos os projetos publicados em euoryan.com. Mantém o CSS dentro do próprio arquivo.
- `assets/images/favicon/bimi-v2.svg`: logo dos e-mails, referenciado no DNS.
- `/politica/`, `/termos/` e `/contato/`: linkados pelo rodapé compartilhado.

## Cache

Ao alterar `style.css` ou `script.js`, subir o número em `?v=` nos links das páginas.

---

a vida é curta, escreva códigos ;)
