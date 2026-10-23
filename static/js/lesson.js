(() => {
  const NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];
  const WHITE = 'relative flex h-32 w-8 cursor-pointer flex-col items-center justify-end rounded-b-md border border-[var(--maroon-deep)]/20 pb-2 transition-all duration-100 sm:w-10 md:w-12 lg:w-11 bg-gradient-to-b from-white to-[var(--cream)] hover:from-[var(--gold-light)]/40 hover:to-[var(--gold)]/20';
  const BLACK = 'absolute top-0 z-10 flex h-20 w-5 cursor-pointer items-end justify-center rounded-b-md pb-1 transition-all duration-100 sm:w-6 md:w-7 bg-gradient-to-b from-[var(--maroon-deep)] to-[var(--maroon)] hover:from-[var(--maroon-light)]';
  let ctx = null, muted = false;

  function tone(m) {
    if (muted) return;
    try {
      ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
      const o = ctx.createOscillator(), g = ctx.createGain(), t = ctx.currentTime;
      o.type = 'triangle'; o.frequency.value = 440 * Math.pow(2, (m - 69) / 12);
      g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(.25, t + .01); g.gain.exponentialRampToValueAtTime(.001, t + 1.2);
      o.connect(g).connect(ctx.destination); o.start(t); o.stop(t + 1.25);
    } catch (e) {}
  }

  // Builds a keyboard from MIDI note `from` to `to` inside `root`; returns {midi: element}
  function build(root, from, to, onKey) {
    root.innerHTML = '';
    const wrap = document.createElement('div'), keys = {};
    wrap.className = 'relative mx-auto flex w-max';
    for (let m = from; m <= to; m++) {
      const n = NAMES[m % 12];
      if (n.includes('#')) continue;
      const w = document.createElement('div');
      w.className = WHITE; w.dataset.midi = m;
      w.innerHTML = `<span class="lbl text-[10px] font-semibold text-[var(--maroon-light)]/60">${n}</span>`;
      keys[m] = w;
      if (m + 1 <= to && NAMES[(m + 1) % 12].includes('#')) {
        const b = document.createElement('div');
        b.className = BLACK; b.dataset.midi = m + 1;
        b.style.cssText = 'right:-3px;margin-right:-3px;box-shadow:0 2px 4px rgba(0,0,0,.4)';
        b.innerHTML = `<span class="lbl text-[8px] font-medium text-[var(--cream)]/50">${NAMES[(m + 1) % 12]}</span>`;
        w.appendChild(b); keys[m + 1] = b;
      }
      wrap.appendChild(w);
    }
    root.appendChild(wrap);
    root.addEventListener('pointerdown', e => {
      const k = e.target.closest('[data-midi]');
      if (k) { e.preventDefault(); onKey(+k.dataset.midi, k); }
    });
    return keys;
  }
  const flash = (el, cls, ms = 220) => { if (!el) return; el.classList.add(cls); setTimeout(() => el.classList.remove(cls), ms); };

  // ---- Practice keyboard (C3–C6) ----
  const kb = document.getElementById('kb');
  if (kb) {
    const play = (keys, m) => { tone(m); flash(keys[m], 'pressed', 200); };
    const keys = build(kb, 48, 84, m => play(keys, m));
    const MAP = {a:60,w:61,s:62,e:63,d:64,f:65,t:66,g:67,y:68,h:69,u:70,j:71,k:72,o:73,l:74,p:75,';':76};
    document.addEventListener('keydown', e => {
      if (e.repeat || e.ctrlKey || e.metaKey || e.altKey || e.target.closest('input,textarea,select')) return;
      const m = MAP[e.key.toLowerCase()]; if (m) play(keys, m);
    });
    const lb = document.getElementById('kb-labels');
    lb.onclick = () => { const h = kb.classList.toggle('hide-lbl'); lb.textContent = h ? 'Show Labels' : 'Hide Labels'; };
    const mb = document.getElementById('kb-mute');
    mb.onclick = () => { muted = !muted; mb.style.opacity = muted ? .45 : 1; mb.title = muted ? 'Unmute' : 'Mute'; };
    const demo = document.getElementById('kb-demo');
    demo.onclick = () => {
      demo.disabled = true;
      [60,62,64,65,67,69,71,72].forEach((m, i) => setTimeout(() => play(keys, m), i * 380));
      setTimeout(() => demo.disabled = false, 8 * 380);
    };
  }

  // ---- Interactive hands (finger numbers) ----
  document.querySelectorAll('[data-widget=hands]').forEach(el => {
    const H = [45, 80, 92, 82, 62];
    const hand = (order, label) => {
      let s = `<svg viewBox="0 0 200 175" class="w-full max-w-[220px]" role="img" aria-label="${label}"><rect x="15" y="100" width="170" height="65" rx="22" fill="var(--secondary)" stroke="var(--border)"/>`;
      order.forEach((f, i) => { const h = H[f - 1], x = 22 + i * 34, y = 108 - h;
        s += `<g class="finger" data-f="${f}"><rect x="${x}" y="${y}" width="28" height="${h + 8}" rx="14"/><text x="${x + 14}" y="${y + 22}" text-anchor="middle">${f}</text></g>`; });
      return s + `</svg><p class="mt-1 text-center text-xs text-muted-foreground">${label}</p>`;
    };
    el.innerHTML = `<div class="flex flex-wrap items-end justify-center gap-6"><div>${hand([1,2,3,4,5], 'Right hand')}</div><div>${hand([5,4,3,2,1], 'Left hand')}</div></div><p class="mt-3 text-center text-xs text-muted-foreground">Tap a finger or press 1–5 on your keyboard</p>`;
    const light = f => el.querySelectorAll(`[data-f="${f}"]`).forEach(g => flash(g, 'on', 350));
    el.addEventListener('pointerdown', e => { const g = e.target.closest('[data-f]'); if (g) light(g.dataset.f); });
    document.addEventListener('keydown', e => { if (/^[1-5]$/.test(e.key) && !e.target.closest('input,textarea,select')) light(e.key); });
  });

  // ---- Find the White Notes game ----
  document.querySelectorAll('[data-widget=notegame]').forEach(el => {
    el.innerHTML = `<div class="mb-3 flex items-center justify-between text-sm"><span>Find the note: <strong class="ng-t font-serif text-2xl text-[var(--maroon)]"></strong></span><span class="text-muted-foreground">Score: <span class="ng-s">0</span></span></div><div class="ng-k hide-lbl overflow-x-auto pb-2"></div><p class="ng-f mt-2 h-5 text-center text-sm text-muted-foreground"></p>`;
    const tEl = el.querySelector('.ng-t'), sEl = el.querySelector('.ng-s'), fEl = el.querySelector('.ng-f');
    let target, score = 0;
    const pick = () => { target = 'ABCDEFG'[Math.floor(Math.random() * 7)]; tEl.textContent = target; };
    const keys = build(el.querySelector('.ng-k'), 60, 83, (m, k) => {
      const n = NAMES[m % 12]; if (n.includes('#')) return;
      tone(m);
      if (n === target) { flash(k, 'ok', 400); sEl.textContent = ++score; fEl.textContent = 'Correct!'; pick(); }
      else { flash(k, 'bad', 400); fEl.textContent = 'Not quite — use the black-key groups as landmarks.'; }
    });
    pick();
  });
})();
