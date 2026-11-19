// يرسم طبقات الترجمة العربية (PNG شفافة 1080x1920) لكل حالة تظليل كلمة بكلمة
// ويكتب overlays.json بتوقيت كل طبقة. التشغيل: node render_captions.mjs
import { createRequire } from 'module';
import fs from 'fs';
const { chromium } = createRequire(import.meta.url)('playwright');
import path from 'path';

const ROOT = path.dirname(new URL(import.meta.url).pathname);
const cfg = JSON.parse(fs.readFileSync(path.join(ROOT, 'captions.json'), 'utf8'));
const OUT = path.join(ROOT, 'out', 'captions');
fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });
const font = (w) => 'file://' + path.join(ROOT, 'assets', `cairo-arabic-${w}-normal.woff2`);
const HL = '#FFD43B';

const css = `
@font-face{font-family:Cairo;font-weight:900;src:url(${font(900)})}
@font-face{font-family:Cairo;font-weight:700;src:url(${font(700)})}
html,body{margin:0;width:1080px;height:1920px;background:transparent;overflow:hidden}
body{font-family:Cairo,'Noto Color Emoji',sans-serif;direction:rtl}
.header{position:absolute;top:150px;left:50%;transform:translateX(-50%);white-space:nowrap;
  font-weight:700;font-size:38px;color:#fff;padding:10px 34px 16px;border-radius:999px;
  background:rgba(8,14,40,.55);border:2px solid rgba(255,255,255,.18);backdrop-filter:blur(6px)}
.box{position:absolute;left:96px;right:96px;bottom:330px;display:flex;flex-direction:column;
  align-items:center;gap:6px;padding:26px 30px 34px;border-radius:40px;
  background:linear-gradient(180deg,rgba(6,10,30,.30),rgba(6,10,30,.62))}
.line{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:0 24px;line-height:1.55}
.w{font-weight:900;font-size:82px;color:#fff;transition:none;
  text-shadow:0 4px 0 rgba(0,0,0,.55),0 0 22px rgba(0,0,0,.6)}
.w.future{opacity:.28}
.w.now{transform:scale(1.14);text-shadow:0 0 26px currentColor,0 4px 0 rgba(0,0,0,.6)}
.fraction .line:nth-child(2) .w{font-size:96px;line-height:1}
.fraction .line:nth-child(1){border-bottom:6px solid rgba(255,255,255,.85);padding-bottom:6px}
.rows .line{gap:0 30px}.rows .w{font-size:74px}
`;

function html(scene, active) {
  // active: index of the word currently highlighted (-1 = none yet)
  let k = 0;
  const lines = scene.lines.map((ln) => {
    const ws = ln.map(([txt, , color]) => {
      const i = k++;
      let cls = 'w', st = '';
      if (i > active) cls += ' future';
      else if (i === active) { cls += ' now'; st = `color:${color || HL}`; }
      else st = `color:${color || '#fff'}`;
      return `<span class="${cls}" style="${st}">${txt}</span>`;
    }).join('');
    return `<div class="line">${ws}</div>`;
  }).join('');
  return `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>
  <div class="header">${cfg.header}</div>
  <div class="box ${scene.layout}">${lines}</div></body></html>`;
}

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
const overlays = [];
for (const [si, scene] of cfg.scenes.entries()) {
  const words = scene.lines.flat();
  const times = words.map((w) => w[1]);
  // حالة -1 (كل الكلمات باهتة) من بداية المشهد حتى أول كلمة
  const states = [[-1, scene.start + 0.25, times[0]]];
  times.forEach((t, i) => states.push([i, t, i + 1 < times.length ? times[i + 1] : scene.end]));
  for (const [active, s, e] of states) {
    if (e - s <= 0.01) continue;
    await page.setContent(html(scene, active), { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const file = path.join(OUT, `s${si + 1}_${String(active + 1).padStart(2, '0')}.png`);
    await page.screenshot({ path: file, omitBackground: true });
    overlays.push({ file, start: +s.toFixed(3), end: +e.toFixed(3) });
  }
}
await browser.close();
fs.writeFileSync(path.join(ROOT, 'out', 'overlays.json'), JSON.stringify(overlays, null, 1));
console.log(`rendered ${overlays.length} caption states`);
