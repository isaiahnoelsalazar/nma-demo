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
  // ---- Staff note-reading game (bass: Middle C/B, treble: all line, space and middle notes) ----
  const STAFF = {
    bass: { glyph: '𝄢', label: 'Bass Clef', buttons: ['Middle C', 'Middle B'],
      notes: [{ ans: 'Middle B', step: 9, midi: 59 }, { ans: 'Middle C', step: 10, midi: 60 }] },
    treble: { glyph: '𝄞', label: 'Treble Clef', buttons: ['A','B','C','D','E','F','G','Middle C','Middle D'],
      notes: [{ ans: 'E', step: 0, midi: 64 }, { ans: 'F', step: 1, midi: 65 }, { ans: 'G', step: 2, midi: 67 }, { ans: 'A', step: 3, midi: 69 },
              { ans: 'B', step: 4, midi: 71 }, { ans: 'C', step: 5, midi: 72 }, { ans: 'D', step: 6, midi: 74 }, { ans: 'E', step: 7, midi: 76 },
              { ans: 'F', step: 8, midi: 77 }, { ans: 'Middle C', step: -2, midi: 60 }, { ans: 'Middle D', step: -1, midi: 62 }] }
  };
  document.querySelectorAll('[data-widget=staffgame]').forEach(el => {
    const cfg = STAFF[el.dataset.clef]; if (!cfg) return;
    const treble = el.dataset.clef === 'treble';
    el.innerHTML = `<div class="mb-2 flex items-center justify-between text-sm"><span class="font-medium text-[var(--maroon-deep)]">What is this note?</span><span class="text-muted-foreground">Score: <span class="sg-s">0</span></span></div><div class="sg-svg mx-auto max-w-xs rounded-xl bg-[var(--cream)] p-2"></div><div class="mt-3 flex flex-wrap justify-center gap-2">${cfg.buttons.map(b => `<button type="button" class="pill" data-a="${b}">${b}</button>`).join('')}</div><p class="sg-f mt-2 h-5 text-center text-sm text-muted-foreground"></p>`;
    const box = el.querySelector('.sg-svg'), sEl = el.querySelector('.sg-s'), fEl = el.querySelector('.sg-f');
    let note, score = 0;
    const draw = n => {
      const y = 108 - n.step * 6, up = n.step < 4, sx = up ? 127.5 : 112.5;
      let s = `<svg viewBox="0 0 220 170" class="w-full" role="img" aria-label="${cfg.label} stave with one note">`;
      for (let i = 0; i < 5; i++) s += `<line x1="10" x2="210" y1="${60 + i * 12}" y2="${60 + i * 12}" stroke="var(--maroon-deep)" stroke-width="1.2"/>`;
      s += `<text x="16" y="${treble ? 112 : 92}" font-size="${treble ? 64 : 54}" fill="var(--maroon-deep)">${cfg.glyph}</text>`;
      if (n.step <= -2 || n.step >= 10) s += `<line x1="104" x2="136" y1="${y}" y2="${y}" stroke="var(--maroon-deep)" stroke-width="1.2"/>`;
      s += `<ellipse cx="120" cy="${y}" rx="8" ry="5.5" transform="rotate(-20 120 ${y})" fill="var(--maroon)"/><line x1="${sx}" x2="${sx}" y1="${y}" y2="${up ? y - 36 : y + 36}" stroke="var(--maroon)" stroke-width="1.8"/>`;
      return s + `<text x="110" y="162" text-anchor="middle" font-size="11" fill="var(--muted)">${cfg.label}</text></svg>`;
    };
    const next = () => { let n; do { n = cfg.notes[Math.floor(Math.random() * cfg.notes.length)]; } while (n === note && cfg.notes.length > 1); note = n; box.innerHTML = draw(n); };
    el.addEventListener('click', e => {
      const b = e.target.closest('[data-a]'); if (!b) return;
      tone(note.midi);
      if (b.dataset.a === note.ans) { sEl.textContent = ++score; fEl.textContent = 'Correct!'; next(); }
      else fEl.textContent = 'Not quite — try again.';
    });
    next();
  });
  // ---- Lesson 1 interactive players ----
  // keys: clickable keyboard with finger-number guides; lights keys in sync with the section video if cues are set
  document.querySelectorAll('[data-player][data-kind=keys]').forEach(el => {
    const keys = build(el, 48, 84, m => { tone(m); flash(keys[m], 'pressed', 200); });
    const g = el.dataset.guide, R = el.dataset.hand !== 'L';
    const PC = { black2: [1, 3], black3: [6, 8, 10], allC: [0] };
    const FING = { black2: R ? [2, 3] : [3, 2], black3: R ? [2, 3, 4] : [4, 3, 2], allC: [1] };
    Object.keys(keys).forEach(m => {
      const i = (PC[g] || []).indexOf(m % 12); if (i < 0) return;
      keys[m].classList.add('guide'); keys[m].insertAdjacentHTML('beforeend', `<span class="fing">${FING[g][i]}</span>`);
    });
    let cues = []; try { cues = JSON.parse(el.dataset.cues || '[]'); } catch (e) {}
    const vid = el.closest('.sec-card') && el.closest('.sec-card').querySelector('video');
    if (vid && cues.length) {
      const lit = new Set();
      const loop = () => {
        const t = vid.currentTime, now = new Set();
        cues.forEach(([s0, d, ms]) => { if (t >= s0 && t < s0 + d) ms.forEach(m => now.add(m)); });
        Object.keys(keys).forEach(m => keys[m].classList.toggle('pressed', now.has(+m)));
        if (!vid.paused && !vid.ended) requestAnimationFrame(loop);
      };
      ['play', 'seeked', 'pause', 'ended'].forEach(ev => vid.addEventListener(ev, () => requestAnimationFrame(loop)));
    }
  });

  // beat: rhythm trainer (S = stomp crotchet, K = clap crotchet, M = clap minim)
  const hit = type => {
    if (muted) return;
    try {
      ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
      const t = ctx.currentTime, g = ctx.createGain(); g.connect(ctx.destination);
      if (type === 'S') {
        const o = ctx.createOscillator(); o.frequency.setValueAtTime(140, t); o.frequency.exponentialRampToValueAtTime(45, t + .15);
        g.gain.setValueAtTime(.6, t); g.gain.exponentialRampToValueAtTime(.001, t + .22); o.connect(g); o.start(t); o.stop(t + .25);
      } else {
        const buf = ctx.createBuffer(1, ctx.sampleRate * .15, ctx.sampleRate), d = buf.getChannelData(0);
        for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / d.length);
        const n = ctx.createBufferSource(), f = ctx.createBiquadFilter(); f.type = 'bandpass'; f.frequency.value = 1800;
        n.buffer = buf; g.gain.value = .7; n.connect(f).connect(g); n.start(t);
      }
    } catch (e) {}
  };
  document.querySelectorAll('[data-player][data-kind=beat]').forEach(el => {
    const pat = [...(el.dataset.pattern || '')], bpm = +el.dataset.bpm || 70, beat = 60000 / bpm, LEN = { S: 1, K: 1, M: 2 };
    el.classList.remove('overflow-x-auto');
    el.innerHTML = `<div class="flex items-center gap-3"><button type="button" class="bp-go flex items-center gap-1.5 rounded-md bg-gold-gradient px-3 py-1.5 text-xs font-semibold text-[var(--maroon-deep)]">Play rhythm</button><span class="bp-c font-serif text-2xl text-[var(--gold-light)]">&nbsp;</span></div><div class="mt-3 flex gap-1">${pat.map((p, i) => `<div data-i="${i}" class="bp-b h-8 rounded border border-[var(--gold)]/30 bg-white/10 text-center text-[11px] leading-8 text-[var(--cream)]/70" style="flex:${LEN[p]}">${p === 'M' ? '1-2' : '1'}</div>`).join('')}</div><p class="mt-2 text-[11px] text-[var(--cream)]/50">♩ = ${bpm} BPM${el.dataset.pattern.includes('S') ? ' · stomp on crotchets, clap on minims' : ' · clap along'}</p>`;
    const go = el.querySelector('.bp-go'), cnt = el.querySelector('.bp-c'), blocks = el.querySelectorAll('.bp-b');
    let timers = [];
    const stop = () => { timers.forEach(clearTimeout); timers = []; blocks.forEach(b => b.classList.remove('on')); cnt.innerHTML = '&nbsp;'; go.textContent = 'Play rhythm'; };
    go.onclick = () => {
      if (timers.length) return stop();
      go.textContent = 'Stop'; let t = 0;
      pat.forEach((p, i) => {
        timers.push(setTimeout(() => { blocks.forEach(b => b.classList.remove('on')); blocks[i].classList.add('on'); cnt.textContent = '1'; hit(p); }, t * beat));
        if (p === 'M') timers.push(setTimeout(() => { cnt.textContent = '2'; }, (t + 1) * beat));
        t += LEN[p];
      });
      timers.push(setTimeout(stop, t * beat));
    };
  });
})();
