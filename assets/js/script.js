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

// home: tooltip com as páginas sobre a logo; no toque, abre e fecha pelo clique
const mw = document.querySelector('.mark-wrap');
if (mw) {
  const mark = mw.querySelector('.mark');
  const set = on => { mw.classList.toggle('open', on); mark.setAttribute('aria-expanded', on); };
  mark.addEventListener('click', e => { e.stopPropagation(); set(!mw.classList.contains('open')); });
  document.addEventListener('click', e => { if (!mw.contains(e.target)) set(false); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') set(false); });
}

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
