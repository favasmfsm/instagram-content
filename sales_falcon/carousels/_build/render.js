#!/usr/bin/env node
// Renders carousels from content/*.json into ../NN-slug/slide-XX.png using headless Chrome.
// Usage: node render.js            -> render all
//        node render.js 11 14      -> render only carousels whose slug starts with 11 or 14
//        node render.js --doc      -> regenerate ../ideas-11-20.md from the JSON scripts
const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');

const BUILD = __dirname;
const OUT_ROOT = path.resolve(BUILD, '..');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const TMP = path.join(BUILD, '.tmp');

const MARK = (body, beak) => `<svg viewBox="80 40 395 360" xmlns="http://www.w3.org/2000/svg"><path d="M85 116 C148 58 231 43 329 75 C375 91 407 119 420 152 C447 160 466 181 470 210 C472 230 461 246 447 255 C452 230 445 214 429 208 C408 197 381 200 352 211 C306 229 268 259 236 300 C241 252 265 214 302 184 C247 201 188 245 141 310 C153 243 192 182 253 145 C192 153 133 179 85 216 C101 175 127 141 165 116 C137 116 111 116 85 116 Z" fill="${body}"/><path d="M371 155 L409 169 L389 184 L375 176 Z" fill="${beak}"/><path d="M318 125 C359 119 397 128 425 151 C391 139 361 137 335 144 Z" fill="${beak}"/><path d="M278 328 H305 V368 H278 Z M316 310 H343 V368 H316 Z M354 290 H381 V368 H354 Z" fill="#C6A66B"/><path d="M263 384 C319 386 374 360 414 313 L404 312 L428 284 L436 320 L424 316 C383 370 327 399 263 395 Z" fill="#C6A66B"/></svg>`;
const markDark = MARK('#111C26', '#F5F2EA');   // navy bird, for light backgrounds
const markLight = MARK('#F5F2EA', '#111C26');  // ivory bird, for dark backgrounds
const TICK = `<svg viewBox="0 0 20 16"><path d="M2 8.5 L7.5 13.5 L18 2.5" fill="none" stroke="#111C26" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
const CHECK_GOLD = `<svg width="30" height="24" viewBox="0 0 20 16"><path d="M2 8.5 L7.5 13.5 L18 2.5" fill="none" stroke="#C6A66B" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
const CROSS = `<svg width="26" height="26" viewBox="0 0 20 20"><path d="M3 3 L17 17 M17 3 L3 17" stroke="#5B6670" stroke-width="3.4" stroke-linecap="round"/></svg>`;

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// **bold**, *gold*, newline -> <br>
const md = s => esc(s || '')
  .replace(/"([^"]*)"/g, '“$1”').replace(/'/g, '’')
  .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
  .replace(/\*(.+?)\*/g, '<span class="g">$1</span>')
  .replace(/\n/g, '<br>');

const DARK_TYPES = new Set(['cover', 'stakes', 'cta']);

function header(s, i, n) {
  const dark = DARK_TYPES.has(s.type) || s.bg === 'dark';
  const pad = x => String(x).padStart(2, '0');
  const markBg = !dark && s.bg !== 'ivory' && s.type !== 'split' && s.type !== 'ba';
  return `<div class="top"><div class="brand"><div class="mark" ${markBg ? 'style="background:#F5F2EA"' : ''}>${dark ? markLight : markDark}</div>THE SALES FALCON</div><div class="count">${pad(i)} / ${pad(n)}</div></div>`;
}
const progress = (i, n) => `<div class="progress" style="width:${Math.round(1080 * i / n)}px"></div>`;
const photoUrl = (c, id) => {
  const p = c.photos[id];
  if (!p && process.env.PLACEHOLDER) return 'file://' + process.env.PLACEHOLDER; // layout testing only
  if (!p) throw new Error(`${c.slug}: unknown photo ${id}`);
  return 'file://' + path.join(BUILD, 'photos', p.file);
};

function slideBody(c, s, i, n) {
  switch (s.type) {
    case 'cover':
      return `<div class="slide cover">
        <div class="bg" style="background-image:url('${photoUrl(c, s.photo)}');${s.pos ? `background-position:${s.pos}` : ''}"></div><div class="shade"></div>
        <div class="logo"><div class="mark">${markLight}</div><div class="rule"></div><div class="word"><small>THE</small><span>SALES FALCON</span></div></div>
        <div class="text"><div class="eyebrow">${md(s.eyebrow)}</div><h1>${md(s.title)}</h1><div class="sub">${md(s.sub)}</div></div>
        <div class="swipe">Swipe ചെയ്യൂ <i></i></div>${progress(i, n)}</div>`;
    case 'stakes':
      return `<div class="slide stakes">${header(s, i, n)}
        <div class="wrap">${s.eyebrow ? `<div class="eyebrow">${md(s.eyebrow)}</div>` : ''}<div class="big ${s.size || ''}">${md(s.title)}</div><div class="bar"></div><div class="line">${md(s.line)}</div></div>
        <div class="swipe">${md(s.next || 'അടുത്ത slide-ൽ fix')} <i></i></div>${progress(i, n)}</div>`;
    case 'split':
      return `<div class="slide ivory split">${header(s, i, n)}
        <div class="photo" style="background-image:url('${photoUrl(c, s.photo)}');${s.pos ? `background-position:${s.pos}` : ''}"></div>
        <div class="content"><div class="eyebrow">${md(s.eyebrow)}</div><h2>${md(s.title)}</h2><div class="body">${md(s.body)}</div>
        ${s.note ? `<div class="divider"></div><div class="note">${md(s.note)}</div>` : ''}</div>
        ${s.tags ? `<div class="tags">${s.tags.map(t => `<span>${esc(t)}</span>`).join('')}</div>` : ''}${progress(i, n)}</div>`;
    case 'chat':
      return `<div class="slide white">${header(s, i, n)}
        <div class="content"><div class="eyebrow">${md(s.eyebrow)}</div><h2>${md(s.title)}</h2>
        <div class="bubbles">${s.messages.map(m => `<div class="bubble ${m.who === 'you' ? 'you' : 'them'}"><small>${esc(m.label || (m.who === 'you' ? 'You' : 'Customer'))}</small>${md(m.text)}</div>`).join('')}</div></div>
        ${s.why ? `<div class="why"><b>WHY</b><span>${md(s.why)}</span></div>` : ''}${progress(i, n)}</div>`;
    case 'list': {
      const numbered = s.numbered;
      return `<div class="slide ${s.bg || 'sand'}">${header(s, i, n)}
        <div class="content"><div class="eyebrow">${md(s.eyebrow)}</div><h2>${md(s.title)}</h2>
        <div class="card">${s.items.map((t, k) => `<div class="check">${numbered ? `<div class="num">${String(k + 1).padStart(2, '0')}</div>` : `<div class="tick">${TICK}</div>`}<div>${md(t)}</div></div>`).join('')}</div></div>
        ${s.save !== false ? `<div class="save"><i></i>${md(s.save || 'Save ചെയ്ത് team-ന് share ചെയ്യൂ')}</div>` : ''}${progress(i, n)}</div>`;
    }
    case 'cards': {
      const layout = s.layout || (s.items.length === 4 ? '' : 'three');
      return `<div class="slide ${s.bg || 'dark'}">${header(s, i, n)}
        <div class="content"><div class="eyebrow">${md(s.eyebrow)}</div><h2>${md(s.title)}</h2>
        <div class="grid ${layout}">${s.items.map((t, k) => `<div class="tile"><div class="n">${String(k + 1).padStart(2, '0')}</div><div><h3>${md(t.h)}</h3><p>${md(t.p)}</p></div></div>`).join('')}</div></div>
        ${s.why ? `<div class="why"><b>${esc(s.whyLabel || 'WHY')}</b><span>${md(s.why)}</span></div>` : ''}${progress(i, n)}</div>`;
    }
    case 'ba':
      return `<div class="slide ivory">${header(s, i, n)}
        <div class="content"><div class="eyebrow">${md(s.eyebrow)}</div><h2>${md(s.title)}</h2>
        <div class="ba"><div class="before"><div class="lab">${CROSS}${esc(s.beforeLabel || 'BEFORE')}</div>${s.before.map(md).join('<hr>')}</div>
        <div class="after"><div class="lab">${CHECK_GOLD}${esc(s.afterLabel || 'AFTER')}</div>${s.after.map(md).join('<hr>')}</div></div></div>
        ${s.why ? `<div class="why"><b>WHY</b><span>${md(s.why)}</span></div>` : ''}${progress(i, n)}</div>`;
    case 'cta':
      return `<div class="slide cta">${header(s, i, n)}
        <div class="wrap"><div class="eyebrow">${md(s.eyebrow || 'Free playbook')}</div><h2>${md(s.title)}</h2><div class="sub">${md(s.sub)}</div>
        <div class="key"><small>DM ചെയ്യൂ</small><span>${esc(s.keyword || 'playbook')}</span></div>
        ${s.ask ? `<div class="ask">${md(s.ask)}</div>` : ''}</div>${progress(i, n)}</div>`;
    case 'follow':
      return `<div class="slide ivory follow">
        <div class="wrap"><div class="bird">${markDark}</div><h2>ഓരോ post-ലും ഒരു<br><span class="g">sales tip.</span></h2>
        <div class="sub">Malayalam-ൽ, simple ആയി. Follow ചെയ്ത്<br>വെച്ചോളൂ.</div>
        <div class="btn">Follow ചെയ്യൂ <b>+</b></div></div>
        <div class="handle"><h4>@thesalesfalcon</h4><p>SHARPER THINKING. SMARTER SELLING.</p></div>${progress(i, n)}</div>`;
    default:
      throw new Error(`${c.slug}: unknown slide type ${s.type}`);
  }
}

function page(c, s, i, n) {
  return `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://${path.join(BUILD, 'slides.css')}"></head><body>${slideBody(c, s, i, n)}</body></html>`;
}

function shoot(htmlFile, pngFile) {
  return new Promise((resolve, reject) => {
    execFile(CHROME, [
      '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
      '--allow-file-access-from-files', '--virtual-time-budget=10000',
      '--window-size=1080,1350', `--screenshot=${pngFile}`, 'file://' + htmlFile,
    ], { timeout: 60000 }, err => (err ? reject(err) : resolve()));
  });
}

function credits(c) {
  const used = [];
  c.slides.forEach((s, k) => { if (s.photo && c.photos[s.photo]) used.push([k + 1, c.photos[s.photo]]); });
  const lines = used.map(([k, p]) => `- Slide ${k}: ${p.credit} — ${p.url}${p.url.includes('?') ? '&' : '?'}utm_source=the_sales_falcon&utm_medium=referral`);
  const names = [...new Set(used.map(([, p]) => p.credit))];
  return { md: `# Photo credits (Unsplash)\n\n${lines.join('\n')}\n`, line: `Photos: ${names.join(', ')} / Unsplash` };
}

async function renderOne(c) {
  const dir = path.join(OUT_ROOT, c.slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.mkdirSync(TMP, { recursive: true });
  for (const f of fs.readdirSync(dir)) if (/^slide-\d+\.png$/.test(f)) fs.unlinkSync(path.join(dir, f));
  const n = c.slides.length;
  const jobs = c.slides.map((s, k) => async () => {
    const i = k + 1;
    const html = path.join(TMP, `${c.slug}-${i}.html`);
    fs.writeFileSync(html, page(c, s, i, n));
    await shoot(html, path.join(dir, `slide-${String(i).padStart(2, '0')}.png`));
  });
  // small pool so Chrome doesn't thrash
  const pool = 4; let next = 0;
  await Promise.all(Array.from({ length: pool }, async () => { while (next < jobs.length) await jobs[next++](); }));
  const cr = credits(c);
  fs.writeFileSync(path.join(dir, 'photo-credits.md'), cr.md);
  fs.writeFileSync(path.join(dir, 'caption.md'), `${c.caption.trim()}\n\n${c.hashtags}\n\n${cr.line}\n`);
  console.log(`✓ ${c.slug} (${n} slides)`);
}

const plain = s => String(s || '').replace(/\*\*?/g, '').replace(/\n/g, ' ');
function slideDoc(s) {
  switch (s.type) {
    case 'cover': return `**Hook 1 (photo):** ${plain(s.title)} — _${plain(s.sub)}_`;
    case 'stakes': return `**Hook 2 (stakes, no photo):** ${plain(s.title)} — _${plain(s.line)}_`;
    case 'split': return `${plain(s.title)} — ${plain(s.body)}${s.note ? ' / ' + plain(s.note) : ''}`;
    case 'chat': return `${plain(s.title)} (chat) — ${s.messages.map(m => `${m.label || (m.who === 'you' ? 'You' : 'Customer')}: ${plain(m.text)}`).join(' · ')}`;
    case 'list': return `${plain(s.title)} — ${s.items.map(plain).join(' · ')}`;
    case 'cards': return `${plain(s.title)} — ${s.items.map((t, k) => `${k + 1}. ${plain(t.h)}: ${plain(t.p)}`).join(' · ')}`;
    case 'ba': return `${plain(s.title)} (before → after) — ${s.before.map(plain).join(' / ')} → ${s.after.map(plain).join(' / ')}`;
    case 'cta': return `CTA — ${plain(s.title)} → DM "${s.keyword || 'playbook'}"`;
    case 'follow': return 'Follow slide';
  }
}
function writeDoc(all) {
  let out = '# The Sales Falcon — Carousels 11–20 (scripts)\n\nEvery carousel opens with **two hooks**: slide 1 is a photo cover that names the problem, and slide 2 is a bold text slide with no photo that raises the stakes. Rendered from `_build/content/*.json`; edit the JSON and run `node _build/render.js`.\n';
  for (const c of all) {
    out += `\n---\n\n## ${c.slug}\n\n`;
    c.slides.forEach((s, k) => { out += `${k + 1}. ${slideDoc(s)}\n`; });
  }
  fs.writeFileSync(path.join(OUT_ROOT, 'ideas-11-20.md'), out);
  console.log('✓ ideas-11-20.md');
}

(async () => {
  const args = process.argv.slice(2);
  const files = fs.readdirSync(path.join(BUILD, 'content')).filter(f => f.endsWith('.json')).sort();
  const all = files.map(f => JSON.parse(fs.readFileSync(path.join(BUILD, 'content', f), 'utf8')));
  if (args.includes('--doc')) return writeDoc(all);
  const pick = args.filter(a => !a.startsWith('--'));
  for (const c of all) if (!pick.length || pick.some(p => c.slug.startsWith(p))) await renderOne(c);
})().catch(e => { console.error(e); process.exit(1); });
