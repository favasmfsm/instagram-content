#!/usr/bin/env node
// Renders Sales Falcon carousels in the design system (flat navy / ivory / gold, T1–T10 templates).
// Content: content/NN-slug.json with "ds": true. Output: ../NN-slug/slide-XX.png + caption.md.
// Usage: node render-ds.js            -> render every ds carousel
//        node render-ds.js 12 14      -> only slugs starting with 12 or 14
//
// ds/bundle.css and ds/icons.js are copied verbatim from the design system artifact
// ("The Sales Falcon", project/components/). Malayalam falls back to Baloo Chettan 2 / Manjari.
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFile } = require('child_process');

const BUILD = __dirname;
const OUT_ROOT = path.resolve(BUILD, '..');
const CONTENT = path.join(BUILD, 'content');
const TMP = path.join(BUILD, '.tmp');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const AVATAR = 'file://' + path.resolve(BUILD, '../../instagram_avatar.png');
const HANDLE = '@thesalesfalcon';

// icon paths from the design system bundle (window.TSF.icons)
const ICONS = (() => {
  const src = fs.readFileSync(path.join(BUILD, 'ds/icons.js'), 'utf8');
  const sandbox = { window: {} };
  new Function('window', src)(sandbox.window);
  return sandbox.window.TSF.icons;
})();
const icon = (n, style = '') =>
  `<i class="tsf-i"${style ? ` style="${style}"` : ''}><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[n] || ''}</svg></i>`;

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// **bold**, *accent* (gold on Ink, gold marker on Paper), "quotes" -> curly, \n -> <br>
const md = s => esc(s || '')
  .replace(/"([^"]*)"/g, '“$1”').replace(/'/g, '’')
  .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
  .replace(/\*([^*]+)\*/g, '<em class="tsf-acc">$1</em>')
  .replace(/\n/g, '<br>');
const plain = s => String(s || '').replace(/\*+/g, '');
const words = s => plain(s).split(/\s+/).filter(w => /[\p{L}\p{N}₹]/u.test(w)).length;

const stack = (gap, inner, extra = '') =>
  `<div style="margin:auto 0;display:flex;flex-direction:column;gap:${gap}px;${extra}">${inner}</div>`;

function chrome(i, n, ink) {
  const swipe = i < n
    ? `<span class="tsf-swipe">${i === 1 ? '<span>Swipe</span>' : ''}<span class="btn">${icon('arrow-right')}</span></span>`
    : '';
  return `<span class="tsf-num">${i}/${n}</span><span class="tsf-handle">${HANDLE}</span>${swipe}`;
}

const INK = new Set(['hook', 'cheatsheet', 'cta']);

function body(s) {
  switch (s.type) {
    case 'hook': // T1
      return stack(48, `${s.kicker ? `<span class="tsf-kicker">${esc(s.kicker)}</span>` : ''}
        <h1 class="tsf-hook${s.small ? ' sm' : ''}">${md(s.title)}</h1>
        ${s.sub ? `<p class="tsf-body" style="color:var(--c-mist)">${md(s.sub)}</p>` : ''}`);
    case 'hook2': // T2
      return stack(40, `<h2 class="tsf-h">${md(s.title)}</h2><p class="tsf-body">${md(s.body)}</p>`);
    case 'tip': // T3
      return stack(40, `${s.n ? `<div class="tsf-badge">${esc(s.n)}</div>` : ''}<h2 class="tsf-h">${md(s.title)}</h2>
        ${s.body ? `<p class="tsf-body">${md(s.body)}</p>` : ''}
        ${s.script ? `<p class="tsf-script">${md(s.script)}</p>` : ''}`);
    case 'dodont': // T4
      return stack(48, `<h2 class="tsf-h">${md(s.title)}</h2>
        <div style="display:flex;flex-direction:column;gap:28px">
          <div class="tsf-box dont"><span class="lab"><span class="ic">${icon('cross')}</span>Don’t say this</span><p class="line">${md(s.dont)}</p></div>
          <div class="tsf-box do"><span class="lab"><span class="ic">${icon('check')}</span>Say this</span><p class="line">${md(s.do)}</p></div>
        </div>`);
    case 'chat': // T5, WhatsApp-style mock
      return stack(44, `<h2 class="tsf-h sm">${md(s.title)}</h2>
        <div class="tsf-mock chat"><div class="bar"><span class="tsf-av alt">${esc(s.initials || '')}</span><span>${esc(s.name)}${s.sub ? `<br><span class="sub">${esc(s.sub)}</span>` : ''}</span><span class="kind">${icon(s.kind === 'voice' ? 'phone' : 'chat')}${esc(s.kindLabel || 'Chat')}</span></div>
          <div class="body">${s.messages.map(m => `<div class="tsf-bub ${m.out ? 'out' : 'in'}">${md(m.text)}${m.t ? `<span class="t">${esc(m.t)}</span>` : ''}</div>`).join('')}</div></div>
        ${s.caption ? `<p class="tsf-caption">${md(s.caption)}</p>` : ''}`);
    case 'call': // T5, call script mock
      return stack(44, `<h2 class="tsf-h sm">${md(s.title)}</h2>
        <div class="tsf-mock call"><div class="bar">${esc(s.bar || 'Call')}<span class="kind">${icon('phone')}${esc(s.kindLabel || 'Call script')}</span></div>
          <div class="body">${s.rows.map(r => `<div class="tsf-script-row ${r.rep ? 'rep' : ''}"><span class="who">${esc(r.who)}</span><span class="say">${md(r.say)}</span></div>`).join('')}</div></div>
        ${s.caption ? `<p class="tsf-caption">${md(s.caption)}</p>` : ''}`);
    case 'steps': // T9 framework: numbered steps
      return stack(48, `<h2 class="tsf-h sm">${md(s.title)}</h2>
        <ol class="tsf-steps">${s.items.map((it, k) => `<li><span class="tsf-badge">${String(k + 1).padStart(2, '0')}</span><span><b>${md(it.h)}</b>${it.p ? `<span>${md(it.p)}</span>` : ''}</span></li>`).join('')}</ol>`);
    case 'split': // T9 framework: before / after. "neutral": two options, not wrong vs right,
      // so no brick cross (brick and green only ever mean don't / do).
      return stack(48, `<h2 class="tsf-h sm">${md(s.title)}</h2>
        <div class="tsf-split">
          <div class="col before"><span class="tsf-capslabel"${s.neutral ? ' style="color:var(--c-slate)"' : ''}>${icon(s.beforeIcon || 'cross')}${esc(s.beforeLabel || 'Before')}</span>${s.before.map(p => `<p>${md(p)}</p>`).join('')}</div>
          <div class="col after"><span class="tsf-capslabel">${icon(s.afterIcon || 'check')}${esc(s.afterLabel || 'After')}</span>${s.after.map(p => `<p>${md(p)}</p>`).join('')}</div>
        </div>
        ${s.caption ? `<p class="tsf-caption">${md(s.caption)}</p>` : ''}`);
    case 'metric': // T10
      return stack(32, `${s.label ? `<span class="tsf-kicker">${esc(s.label)}</span>` : ''}
        <div class="tsf-big">${esc(s.value)}</div><h2 class="tsf-h sm">${md(s.title)}</h2>
        ${s.caption ? `<p class="tsf-caption">${md(s.caption)}</p>` : ''}`);
    case 'cheatsheet': // T6
      return stack(48, `<div style="display:flex;flex-direction:column;gap:20px">
          <span class="tsf-kicker" style="display:flex;gap:12px;align-items:center">${icon('bookmark', 'width:30px;height:30px')}Save this</span>
          <h2 class="tsf-h">${md(s.title)}</h2></div>
        <ol class="tsf-list">${s.items.map((t, k) => `<li><b>${String(k + 1).padStart(2, '0')}</b><span>${md(t)}</span></li>`).join('')}</ol>`);
    case 'cta': // T7
      return `<div style="margin-top:auto;display:flex;flex-direction:column;gap:56px">
          <h2 class="tsf-h">${md(s.title)}</h2>
          ${s.sub ? `<p class="tsf-body" style="color:var(--c-mist)">${md(s.sub)}</p>` : ''}
          <span class="tsf-cta-pill">${icon(s.icon || 'send')}${esc(s.pill)}</span></div>
        <div style="margin-top:auto;margin-bottom:40px;display:flex;flex-direction:column;gap:28px;border-top:2px solid var(--c-ink-hair);padding-top:56px">
          <div class="tsf-sig"><span class="tsf-avatar"><img src="${AVATAR}" alt=""></span><span class="who">The Sales Falcon<small>Sharper thinking. Smarter selling.</small></span></div></div>`;
    default:
      throw new Error(`unknown slide type ${s.type}`);
  }
}

const FONTS = `@import url('https://fonts.googleapis.com/css2?family=Baloo+Chettan+2:wght@500;600;700;800&family=Manjari:wght@400;700&display=block');
:root { --font-display: Montserrat, "Baloo Chettan 2", "Helvetica Neue", Arial, sans-serif;
        --font-body: Inter, Manjari, system-ui, sans-serif; }
html, body { margin: 0; padding: 0; background: #111C26; }
/* Malayalam fonts have no italic: keep them upright instead of a fake slant */
.tsf-slide { font-synthesis-style: none; }`;

function page(s, i, n) {
  const ink = s.ink ?? INK.has(s.type);
  return `<!doctype html><html lang="en"><head><meta charset="utf-8">
<style>${FONTS}</style><link rel="stylesheet" href="file://${path.join(BUILD, 'ds/bundle.css')}"></head>
<body><div class="tsf-slide${ink ? ' ink' : ''}" id="slide">${body(s)}${chrome(i, n, ink)}</div></body></html>`;
}

// One Chrome process and one throwaway profile per slide. Parallel shots that share a
// profile can hand a page to another tab, which is how 11-price-objection's cover got
// another carousel's text ghosted into it.
function shoot(htmlFile, pngFile) {
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'tsf-chrome-'));
  return new Promise((resolve, reject) => {
    execFile(CHROME, [
      '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
      `--user-data-dir=${profile}`, '--no-first-run', '--no-default-browser-check',
      '--allow-file-access-from-files', '--virtual-time-budget=15000',
      '--window-size=1080,1350', `--screenshot=${pngFile}`, 'file://' + htmlFile,
    ], { timeout: 90000 }, err => {
      fs.rmSync(profile, { recursive: true, force: true });
      err ? reject(err) : resolve();
    });
  });
}

// Contact sheet for review: _build/.tmp/sheet-<slug>.png (not committed).
function sheet(slug, dir, n) {
  const cols = 4, w = 432, h = 540, gap = 12;
  const rows = Math.ceil(n / cols);
  const W = cols * (w + gap) + gap, H = rows * (h + gap) + gap;
  const imgs = Array.from({ length: n }, (_, k) =>
    `<img src="file://${path.join(dir, `slide-${String(k + 1).padStart(2, '0')}.png`)}" style="width:${w}px;height:${h}px;display:block">`).join('');
  const html = path.join(TMP, `sheet-${slug}.html`);
  fs.writeFileSync(html, `<!doctype html><html><body style="margin:0;background:#c8c8c8"><div style="display:grid;grid-template-columns:repeat(${cols},${w}px);gap:${gap}px;padding:${gap}px">${imgs}</div></body></html>`);
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'tsf-chrome-'));
  return new Promise((resolve, reject) => execFile(CHROME, ['--headless=new', '--disable-gpu', '--hide-scrollbars',
    '--force-device-scale-factor=1', `--user-data-dir=${profile}`, '--allow-file-access-from-files',
    `--window-size=${W},${H}`, `--screenshot=${path.join(TMP, `sheet-${slug}.png`)}`, 'file://' + html],
  { timeout: 60000 }, err => { fs.rmSync(profile, { recursive: true, force: true }); err ? reject(err) : resolve(); }));
}

// Layout check: load the slide in Chrome and report any content box that crosses the
// 80px side margins or the 96px top/bottom band (the chrome itself is exempt).
const PROBE = `<script>addEventListener('load', () => document.fonts.ready.then(() => {
  const bad = [];
  document.querySelectorAll('#slide *').forEach(el => {
    if (el.closest('.tsf-num,.tsf-handle,.tsf-swipe') || !el.childNodes.length) return;
    const r = el.getBoundingClientRect();
    if (r.width && (r.left < (el.classList.contains('tsf-acc') ? 70 : 79) || r.right > (el.classList.contains('tsf-acc') ? 1010 : 1001) || r.top < 95 || r.bottom > 1255))
      bad.push(el.className || el.tagName);
  });
  const o = document.createElement('pre'); o.id = 'overflow'; o.textContent = JSON.stringify([...new Set(bad)]);
  document.body.appendChild(o);
}));</script>`;

function overflow(htmlFile) {
  const probe = htmlFile.replace(/\.html$/, '.probe.html');
  fs.writeFileSync(probe, fs.readFileSync(htmlFile, 'utf8').replace('</body>', PROBE + '</body>'));
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'tsf-chrome-'));
  return new Promise(resolve => execFile(CHROME, ['--headless=new', '--disable-gpu', `--user-data-dir=${profile}`,
    '--allow-file-access-from-files', '--virtual-time-budget=15000', '--window-size=1080,1350', '--dump-dom', 'file://' + probe],
  { timeout: 90000, maxBuffer: 1 << 24 }, (err, out) => {
    fs.rmSync(profile, { recursive: true, force: true });
    const m = /<pre id="overflow">([^<]*)<\/pre>/.exec(out || '');
    resolve(m ? JSON.parse(m[1].replace(/&quot;/g, '"')) : ['(probe failed)']);
  }));
}

function lint(c) {
  const warn = [];
  c.slides.forEach((s, k) => {
    const texts = [s.title, s.sub, s.body, s.script, s.dont, s.do, s.caption, s.pill,
      ...(s.items || []).map(t => (typeof t === 'string' ? t : `${t.h} ${t.p || ''}`)),
      ...(s.messages || []).map(m => m.text), ...(s.rows || []).map(r => r.say),
      ...(s.before || []), ...(s.after || [])].filter(Boolean);
    const total = texts.reduce((a, t) => a + words(t), 0);
    const limit = s.type === 'cheatsheet' || s.type === 'chat' || s.type === 'call' || s.type === 'steps' ? 45 : 30;
    if (total > limit) warn.push(`slide ${k + 1} (${s.type}): ${total} words`);
    const head = words(s.title);
    if (head > (k === 0 ? 10 : 8)) warn.push(`slide ${k + 1}: headline ${head} words`);
    const acc = texts.join(' ').match(/(?<!\*)\*[^*]+\*(?!\*)/g) || [];
    const accWords = acc.reduce((a, t) => a + words(t), 0);
    if (accWords > 3) warn.push(`slide ${k + 1}: ${accWords} gold words`);
  });
  if (c.slides.length < 7 || c.slides.length > 10) warn.push(`${c.slides.length} slides`);
  if (c.slides[c.slides.length - 1].type !== 'cta') warn.push('last slide is not the CTA');
  return warn;
}

async function renderOne(c) {
  const dir = path.join(OUT_ROOT, c.slug);
  fs.mkdirSync(dir, { recursive: true });
  for (const f of fs.readdirSync(dir)) if (/^slide-\d+\.png$/.test(f)) fs.unlinkSync(path.join(dir, f));
  const n = c.slides.length;
  const jobs = c.slides.map((s, k) => async () => {
    const i = k + 1;
    const html = path.join(TMP, `ds-${c.slug}-${i}.html`);
    fs.writeFileSync(html, page(s, i, n));
    await shoot(html, path.join(dir, `slide-${String(i).padStart(2, '0')}.png`));
    const out = await overflow(html);
    if (out.length) layout.push(`slide ${i}: outside the margins: ${out.join(', ')}`);
  });
  const layout = [];
  const pool = 4; let next = 0;
  await Promise.all(Array.from({ length: pool }, async () => { while (next < jobs.length) await jobs[next++](); }));
  fs.writeFileSync(path.join(dir, 'caption.md'), `${c.caption.trim()}\n\n${c.hashtags}\n`);
  await sheet(c.slug, dir, n);
  const warn = [...lint(c), ...layout];
  console.log(`${warn.length ? '!' : '✓'} ${c.slug} (${n} slides)${warn.map(w => `\n    ${w}`).join('')}`);
}

(async () => {
  const only = process.argv.slice(2);
  // fresh scratch pages every run, so no stale page can be picked up
  fs.rmSync(TMP, { recursive: true, force: true });
  fs.mkdirSync(TMP, { recursive: true });
  const files = fs.readdirSync(CONTENT).filter(f => f.endsWith('.json')).sort();
  for (const f of files) {
    const c = JSON.parse(fs.readFileSync(path.join(CONTENT, f), 'utf8'));
    if (!c.ds) continue;
    if (only.length && !only.some(p => c.slug.startsWith(p))) continue;
    await renderOne(c);
  }
})().catch(e => { console.error(e); process.exit(1); });
