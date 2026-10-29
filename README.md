# euoryan.com

Site pessoal publicado em [euoryan.com](https://euoryan.com) pelo GitHub Pages, atrás da Cloudflare.

HTML, CSS e JavaScript puros, sem build e sem dependências. Nenhum recurso vem de outro domínio.

## Estrutura

```
index.html              home
contato/                contato
politica/               política de privacidade
termos/                 termos de uso
restrito/               aviso de projeto com acesso restrito
github/                 artigo sobre a história do GitHub
404.html                página de erro dos endereços na raiz de euoryan.com
assets/
  css/style.css         estilos de todas as páginas, exceto a 404
  js/script.js          comportamento de todas as páginas, exceto a 404
  fonts/                Neue Montreal (home), Space Grotesk (internas) e Inter (404)
  images/favicon/       logos dos e-mails (BIMI)
  images/og.png         imagem de prévia dos links
  images/projetos/      imagens guardadas para uso futuro
  images/clientes/      imagens guardadas para uso futuro
  pages/footer.html     rodapé compartilhado, carregado por outros projetos
favicon.ico, favicon.svg, apple-touch-icon.png
robots.txt              libera buscadores e bloqueia robôs de IA
sitemap.xml             páginas públicas para os buscadores
.well-known/
  security.txt          contato para relatar falhas de segurança
  tdmrep.json           reserva de direitos contra mineração de texto e dados
.nojekyll               publica os arquivos sem processamento do Jekyll
CNAME                   domínio do GitHub Pages
```

## Rodar localmente

```
python3 -m http.server 8081 --bind 127.0.0.1
```

Abrir http://127.0.0.1:8081. Usar `127.0.0.1` em vez de `localhost`, que pode resolver para IPv6 e não abrir.

## Caminhos que não podem mudar

Outros projetos dependem destes arquivos pelo endereço:

- `assets/pages/footer.html`: rodapé baixado por outros sites via raw.githubusercontent.com. Precisa funcionar em qualquer site, claro ou escuro, sem CSS de quem o recebe.
- `404.html`: página de erro dos endereços na raiz de euoryan.com. Repositórios publicados em euoryan.com/<repo> precisam de uma cópia própria. Mantém o CSS dentro do arquivo e só caminhos absolutos.
- `assets/images/favicon/bimi-v2.svg`: logo dos e-mails, referenciado no DNS.
- `/politica/`, `/termos/` e `/contato/`: linkados pelo rodapé compartilhado.
- `/restrito/` e `/github/`: linkados por outros projetos.

## Segurança

Cada página declara uma Content-Security-Policy que só aceita scripts, estilos, fontes e imagens do próprio domínio. Ao adicionar um recurso externo, a página bloqueia o carregamento até a política ser ajustada.

A 404 libera o próprio CSS pelo hash `sha256` do bloco `<style>`. Qualquer mudança nesse bloco exige recalcular o hash:

```
python3 -c "import re,hashlib,base64;s=re.search(r'<style>(.*?)</style>',open('404.html').read(),re.S).group(1);print(base64.b64encode(hashlib.sha256(s.encode()).digest()).decode())"
```

O `security.txt` vence no campo `Expires` e precisa ser renovado antes dessa data.

## Cache

Ao alterar `style.css` ou `script.js`, subir o número em `?v=` nos links de todas as páginas, exceto a 404.

---

a vida é curta, escreva códigos ;)
