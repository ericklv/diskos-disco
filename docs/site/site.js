'use strict';
/* Each theme owns its own preview. No autoplay, tracking or external libraries. */
document.querySelectorAll('.theme').forEach(theme => {
  const main = theme.querySelector('.main-shot');
  const image = main.querySelector('img');
  const caption = theme.querySelector('.screen-caption');
  theme.querySelectorAll('[data-screen]').forEach(button => {
    button.addEventListener('click', () => {
      const previous = {src: image.getAttribute('src'), alt: image.alt, caption: caption.textContent};
      image.src = button.dataset.screen;
      image.alt = button.querySelector('img').alt;
      caption.textContent = button.dataset.caption;
      main.href = button.dataset.screen;
      main.setAttribute('aria-label', `Enlarge ${theme.querySelector('h2').textContent} ${caption.textContent}`);
      button.dataset.screen = previous.src;
      button.dataset.caption = previous.caption;
      button.querySelector('img').src = previous.src;
      button.querySelector('img').alt = previous.alt;
      button.querySelector('span').textContent = previous.caption;
      button.setAttribute('aria-label', `Preview ${theme.querySelector('h2').textContent} ${previous.caption}`);
    });
  });
});
const dialog = document.querySelector('.screen-dialog');
if (dialog && typeof dialog.showModal === 'function') {
  document.querySelectorAll('.main-shot').forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      dialog.querySelector('img').src = link.href;
      dialog.querySelector('img').alt = link.querySelector('img').alt;
      dialog.querySelector('p').textContent = `${link.closest('.theme').querySelector('h2').textContent} · ${link.closest('.theme').querySelector('.screen-caption').textContent}`;
      dialog.showModal();
    });
  });
  dialog.querySelector('button').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
}

/* Native sticky chapters: document scrolling stays under the reader's control.
 * A tall panel scrolls completely into view before pinning. Mobile, short screens
 * and reduced motion use normal flow. No wheel/touch interception or scroll hijack. */
const chapters = [...document.querySelectorAll('main > section')].map(panel => {
  const chapter = document.createElement('div');
  chapter.className = 'chapter';
  panel.before(chapter); chapter.append(panel); panel.classList.add('chapter-panel');
  return {chapter, panel};
});
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let layoutFrame = 0;
function measureChapters() {
  layoutFrame = 0;
  const pin = window.innerWidth > 900 && window.innerHeight > 680 && !reducedMotion.matches;
  chapters.forEach(({chapter, panel}) => {
    const height = Math.ceil(panel.getBoundingClientRect().height);
    chapter.style.setProperty('--chapter-height', pin ? `${height + Math.round(window.innerHeight * .2)}px` : 'auto');
    panel.style.setProperty('--pin-top', `${Math.min(0, window.innerHeight - height)}px`);
  });
}
function requestLayout() { if (!layoutFrame) layoutFrame = requestAnimationFrame(measureChapters); }
window.addEventListener('resize', requestLayout, {passive: true});
window.addEventListener('load', requestLayout, {once: true});
reducedMotion.addEventListener('change', requestLayout);
if (typeof ResizeObserver === 'function') {
  const observer = new ResizeObserver(requestLayout);
  chapters.forEach(({panel}) => observer.observe(panel));
}
if (document.fonts) document.fonts.ready.then(requestLayout);
requestLayout();

(() => {
  const v = document.querySelector('.showcase-video'); if (!v) return;
  const btns = [...document.querySelectorAll('.chapters button')];
  const times = btns.map(b => +b.dataset.t);
  btns.forEach(b => b.addEventListener('click', () => { v.currentTime = +b.dataset.t; v.play().catch(() => {}); }));
  v.addEventListener('timeupdate', () => {
    let k = -1; times.forEach((t, i) => { if (v.currentTime >= t - 0.2 && (k < 0 || t >= times[k])) k = i; });
    btns.forEach((b, i) => b.classList.toggle('active', i === k && !v.paused || i === k && v.currentTime > 0));
  });
})();

/* Actual firmware captures, kept in the selected accent across the whole tour. */
(() => {
  const hero = document.querySelector('.zune-hero'); if (!hero) return;
  const steps = [
    ['menu','Main menu','Start with the music.','A bold, flowing menu keeps your collection close. Return Home and Now Playing is ready, with room for the track and artist underneath.','On the player: swipe up to return Home.'],
    ['music','Now Playing','Room for the song.','Artwork slips off the edge to give the title and artist more space. Duration and audio details stay together; your main icon can have separate tap, double-tap and hold shortcuts.','On the player: set shortcuts in Display → Music screen → Zune.'],
    ['coverflow','Library · Coverflow','Take your covers for a spin.','Browse a curved carousel of albums. Coverflow, Wall and List are shared library choices, each dressed in the current theme.','On the player: choose Coverflow in the Album View setting.'],
    ['wall','Library · Wall','A record shop in miniature.','Let the artwork lead. A compact wall puts more albums in view, with a little colour from your collection against Zune’s quiet black canvas.','On the player: choose Wall in the Album View setting.'],
    ['quick','Quick Settings','The little things, close by.','Six configurable actions put the controls you use within reach. The track banner keeps moving while visible, with clear, centred pause and resume feedback.','On the player: customise your Quick Settings items.'],
    ['stats','Listening stats','See where the music takes you.','Your listening history, wearing the same theme. Explore your week, month and year, with clearer small text and a calmer balance between headings and detail.','Sample history is shown here; your Disc builds its own story.'],
    ['immersive','Immersive 3.0','More music. Less in the way.','Immersive 3.0 brings the spinning album and a shared transport overlay to Zune too. Tap to reveal track details, previous, play/pause and next; a spinning-disc transition carries you in and out.','Shown with the transport overlay open. Tap the artwork on your Disc to reveal it.']
  ];
  const palette = {magenta:'#ec008c',cyan:'#00b7d8',orange:'#ff751f',lime:'#9bd238'};
  let step = 0, accent = 'magenta';
  const image = hero.querySelector('#zune-screen'), link = hero.querySelector('.zune-enlarge');
  function render() {
    const [file,name,title,copy,hint] = steps[step];
    const src = `site/zune/${accent}-${file}.webp`;
    image.src = src; image.alt = `Zune ${name}, ${accent} accent, sample music and artwork`;
    link.href = src; link.setAttribute('aria-label',`Enlarge Zune ${name}`);
    hero.style.setProperty('--zune-accent',palette[accent]);
    hero.querySelector('#zune-color-name').textContent = accent[0].toUpperCase()+accent.slice(1);
    hero.querySelector('#zune-counter').textContent = `${String(step+1).padStart(2,'0')} / 07 · ${name}`;
    hero.querySelector('#zune-step-title').textContent = title;
    hero.querySelector('#zune-step-copy').textContent = copy;
    hero.querySelector('#zune-step-hint').textContent = hint;
    hero.querySelectorAll('[data-step]').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.step===step)));
    hero.querySelectorAll('[data-accent]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.accent===accent)));
  }
  hero.querySelectorAll('[data-step]').forEach(b=>b.addEventListener('click',()=>{step=+b.dataset.step;render();}));
  hero.querySelectorAll('[data-accent]').forEach(b=>b.addEventListener('click',()=>{accent=b.dataset.accent;render();}));
  function advance(delta){step=(step+delta+steps.length)%steps.length;render();}
  hero.querySelector('#zune-prev').addEventListener('click',()=>advance(-1));
  hero.querySelector('#zune-next').addEventListener('click',()=>advance(1));
  hero.querySelector('.zune-steps').addEventListener('keydown',e=>{
    if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();advance(e.key==='ArrowRight'?1:-1);hero.querySelector(`[data-step="${step}"]`).focus();}
  });
  link.addEventListener('click',e=>{
    if(!dialog || typeof dialog.showModal!=='function')return;
    e.preventDefault();dialog.querySelector('img').src=link.href;dialog.querySelector('img').alt=image.alt;
    dialog.querySelector('p').textContent=`Zune · ${steps[step][1]} · ${accent}`;dialog.showModal();
  });
})();
