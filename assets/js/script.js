const EMAIL = 'contato@euoryan.com';
document.querySelectorAll('[data-email]').forEach(e => e.textContent = EMAIL);
document.querySelectorAll('[data-year]').forEach(e => e.textContent = new Date().getFullYear());

document.querySelectorAll('[data-copy]').forEach(b => {
  const label = b.querySelector('span'), orig = label && label.textContent;
  b.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(EMAIL); }
    catch { const t = document.createElement('textarea'); t.value = EMAIL; document.body.appendChild(t); t.select(); document.execCommand('copy'); t.remove(); }
    if (label) label.textContent = 'e-mail copiado';
    b.classList.add('done');
    setTimeout(() => { if (label) label.textContent = orig; b.classList.remove('done'); }, 1600);
  });
});

// internas: o status abre ao carregar; no celular recolhe sozinho e abre pelo toque
const st = document.querySelector('.status');
if (st) {
  const small = matchMedia('(max-width:560px)');
  let timer;
  const open = () => {
    st.classList.add('open');
    clearTimeout(timer);
    if (small.matches) timer = setTimeout(() => st.classList.remove('open'), 2600);
  };
  setTimeout(open, 400);
  st.addEventListener('click', () => { if (small.matches) st.classList.contains('open') ? st.classList.remove('open') : open(); });
  small.addEventListener('change', () => small.matches ? st.classList.remove('open') : st.classList.add('open'));
}

/* Assinatura no console do navegador, uma vez por carregamento (mesmo padrão do Pegasus). */
(function () {
  const LOGO = [
    '         _nnnn_',
    '        dGGGGMMb',
    '       @p~qp~~qMb',
    '       M|@||@) M|',
    '       @,----.JM|',
    '      JS^\\__/  qKL',
    '     dZP        qKRb',
    '    dZP          qKKb',
    '   fZP            SMMb',
    '   HZM            MMMM',
    '   FqM            MMMM',
    ' __| ".        |\\dS"qML',
    " |    `.       | `' \\Zq",
    "_)      \\.___.,|     .'",
    "\\____   )MMMMMP|   .'",
    "     `-'       `--' ryan",
  ];
  const NOME = [
    '███████╗ ██╗   ██╗  ██████╗  ██████╗  ██╗   ██╗  █████╗  ███╗   ██╗',
    '██╔════╝ ██║   ██║ ██╔═══██╗ ██╔══██╗ ╚██╗ ██╔╝ ██╔══██╗ ████╗  ██║',
    '█████╗   ██║   ██║ ██║   ██║ ██████╔╝  ╚████╔╝  ███████║ ██╔██╗ ██║',
    '██╔══╝   ██║   ██║ ██║   ██║ ██╔══██╗   ╚██╔╝   ██╔══██║ ██║╚██╗██║',
    '███████╗ ╚██████╔╝ ╚██████╔╝ ██║  ██║    ██║    ██║  ██║ ██║ ╚████║',
    '╚══════╝  ╚═════╝   ╚═════╝  ╚═╝  ╚═╝    ╚═╝    ╚═╝  ╚═╝ ╚═╝  ╚═══╝',
  ];
  const FAIXA = 'EUORYAN.COM  ·  DESENVOLVEDOR FULL STACK';
  const LARGURA = 67;
  const centrar = (linha) => ' '.repeat(Math.max(0, Math.floor((LARGURA - linha.length) / 2))) + linha;
  // O desenho do pinguim mantém o recuo relativo; o bloco inteiro é centrado uma vez.
  const padLogo = ' '.repeat(Math.max(0, Math.floor((LARGURA - Math.max(...LOGO.map((l) => l.length))) / 2)));
  const FONTE = "font-family:Menlo,Consolas,'DejaVu Sans Mono',monospace";
  const ESTILO_ARTE = `${FONTE};font-size:10px;line-height:11px;display:inline-block`;
  const ESTILO_INFO = `${FONTE};font-size:11px;color:#8b8b8b`;
  const ESTILO_AVISO = 'font-size:12px;font-weight:600;color:#e5484d';
  const arte = ['', ...LOGO.map((l) => padLogo + l), '', '', ...NOME.map(centrar), '', centrar(FAIXA), ''].join('\n');
  const info = 'euoryan  ·  Desenvolvedor full stack  ·  euoryan.com';
  const aviso =
    'Pare. Este console é para quem desenvolve. Se alguém pediu para você colar algo aqui, é golpe: o código pode tomar a sua conta.';
  console.log(`%c${arte}%c\n\n${info}\n\n%c${aviso}`, ESTILO_ARTE, ESTILO_INFO, ESTILO_AVISO);
})();
