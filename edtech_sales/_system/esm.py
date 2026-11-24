"""EdTech Sales Master carousel builder.

Each carousel folder has a spec.py that calls these helpers and then build().
Slides are full-size 1080 x 1350 .es-slide elements styled by the design
system's bundle.css; tokens.json becomes CSS variables here.
"""
import json, os, re, subprocess, sys, html

SYS = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ARROW = '<svg viewBox="0 0 56 24" aria-hidden="true"><path d="M2 12H52M42 3L52 12L42 21"/></svg>'
CHECK = '<span class="es-check"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5L10 17L19 7"/></svg></span>'
X_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6L18 18M18 6L6 18"/></svg>'
TICK_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5L10 17L19 7"/></svg>'


def tokens_css():
    t = json.load(open(os.path.join(SYS, "tokens.json")))
    v = []
    for tok in t["color"]["tokens"]:
        val = re.sub(r"\{(.+?)\}", r"var(--\1)", tok["value"])
        v.append(f"--{tok['name']}:{val};")
    for fam in ["spacing", "radius", "shadow", "layout"]:
        for tok in t[fam]["tokens"]:
            v.append(f"--{tok['name']}:{tok['value']};")
    for k, s in t["type"]["families"].items():
        v.append(f"--font-{k}:{s};")
    css = ":root{" + "".join(v) + "}\n"
    for g in t["type"]["groups"]:
        for s in g["styles"]:
            ls = f"letter-spacing:{s['letterSpacing']};" if "letterSpacing" in s else ""
            css += f".{s['name']}{{font-size:{s['fontSize']};line-height:{s['lineHeight']};font-weight:{s['fontWeight']};{ls}}}\n"
    return css


class Carousel:
    def __init__(self, folder, handle="@edtechsalesmaster"):
        self.folder = folder
        self.handle = handle
        self.slides = []  # (kind, ground_is_dark, html_fn)

    # --- shared chrome -------------------------------------------------
    def _top(self, n, dark=False, narrow=False):
        mark = "../_system/logos/esm-mark-reverse.svg" if dark else "../_system/logos/esm-mark.svg"
        return (f'<div class="es-top{" es-top--narrow" if narrow else ""}"><img class="es-mark" src="{mark}" alt="">'
                f'<span class="label es-brand">EdTech Sales Master</span><span class="label es-count">{n:02d} / {{TOTAL}}</span></div>')

    def _prog(self, n):
        return f'<div class="es-progress" style="--p:{{P{n}}}"></div>'

    @staticmethod
    def _photo(cls, photo, brief):
        inner = f'<img src="{photo}" alt="">' if photo else f'<span class="es-photo-note">{brief}</span>'
        return f'<div class="es-photo {cls}">{inner}</div>'

    def _add(self, kind, dark, fn):
        self.slides.append((kind, dark, fn))
        return self

    # --- templates -----------------------------------------------------
    def hook(self, eyebrow, title, sub, photo=None, brief=""):
        def f(n):
            return f'''<div class="es-slide es-on-dark">
<div class="es-fill">{self._photo("es-fill", photo, brief)}</div>
<div class="es-scrim"></div>
<div class="es-logo-badge"><img src="../_system/logos/esm-mark-reverse.svg" alt="EdTech Sales Master"><div class="es-wordmark"><b>EdTech Sales</b><span>MASTER</span></div></div>
<div class="es-hook"><span class="label es-eyebrow">{eyebrow}</span><h1 class="hook-title">{title}</h1><p class="body-lg">{sub}</p></div>
<div class="es-swipe button">Swipe {ARROW}</div>{self._prog(n)}</div>'''
        return self._add("hook", True, f)

    def stat(self, eyebrow, big, title, source):
        def f(n):
            return f'''<div class="es-slide es-slide--dark">{self._top(n, dark=True)}
<div class="es-stat-wrap"><span class="label es-eyebrow">{eyebrow}</span><div class="stat">{big}</div>
<h2 class="slide-title">{title}</h2><span class="label es-source">{source}</span></div>
<div class="es-bars" aria-hidden="true"><i style="height:30%"></i><i style="height:52%"></i><i style="height:74%"></i><i class="on" style="height:100%"></i></div>{self._prog(n)}</div>'''
        return self._add("stat", True, f)

    def side(self, eyebrow, title, body, after, tags=(), photo=None, brief=""):
        def f(n):
            tg = "".join(f'<span class="es-tag">{t}</span>' for t in tags)
            return f'''<div class="es-slide">{self._top(n, narrow=True)}
<div class="es-side"><div class="es-side-text"><span class="label es-eyebrow">{eyebrow}</span><h2 class="slide-title">{title}</h2>
<p class="body">{body}</p><div class="es-rule"></div><p class="body es-muted">{after}</p><div class="es-tags">{tg}</div></div>
{self._photo("", photo, brief)}</div>{self._prog(n)}</div>'''
        return self._add("side", False, f)

    def numbered(self, title, items, photo=None, brief=""):
        def f(n):
            li = "".join(f'<li><span class="numeral">{i+1:02d}</span><div><h3>{h}</h3><p>{p}</p></div></li>' for i, (h, p) in enumerate(items))
            return f'''<div class="es-slide">{self._photo("es-band es-photo--light", photo, brief)}
<div class="es-list-wrap"><h2 class="slide-title">{title}</h2><ol class="es-list">{li}</ol></div>{self._prog(n)}</div>'''
        return self._add("numbered", False, f)

    def script(self, eyebrow, title, bubbles, why, ground="es-slide--white"):
        def f(n):
            b = "".join(f'<div class="es-bubble es-bubble--{"you" if who == "You" else "them"} chat"><span class="label">{who}</span>{line}</div>' for who, line in bubbles)
            return f'''<div class="es-slide {ground}">{self._top(n)}
<div class="es-script-head"><span class="label es-eyebrow">{eyebrow}</span><h2 class="slide-title">{title}</h2></div>
<div class="es-chat">{b}</div><div class="es-why body"><b>Why</b><span>{why}</span></div>{self._prog(n)}</div>'''
        return self._add("script", False, f)

    def compare(self, eyebrow, title, wrong_head, wrong, right_head, right):
        def f(n):
            w = "".join(f"<p>{x}</p>" for x in wrong)
            r = "".join(f"<p>{x}</p>" for x in right)
            return f'''<div class="es-slide">{self._top(n)}
<div class="es-compare-wrap"><span class="label es-eyebrow">{eyebrow}</span><h2 class="slide-title">{title}</h2>
<div class="es-compare"><div class="es-col es-col--wrong"><span class="label es-col-head">{X_ICON}{wrong_head}</span>{w}</div>
<div class="es-col es-col--right"><span class="label es-col-head">{TICK_ICON}{right_head}</span>{r}</div></div></div>{self._prog(n)}</div>'''
        return self._add("compare", False, f)

    def steps(self, eyebrow, title, steps):
        def f(n):
            li = "".join(f'<li><span class="numeral">{i+1:02d}</span><h3>{h}</h3><p>{p}</p></li>' for i, (h, p) in enumerate(steps))
            return f'''<div class="es-slide es-slide--dark">{self._top(n, dark=True)}
<div class="es-steps-wrap"><span class="label es-eyebrow">{eyebrow}</span><h2 class="slide-title">{title}</h2><ol class="es-steps">{li}</ol></div>{self._prog(n)}</div>'''
        return self._add("steps", True, f)

    def bottom(self, eyebrow, title, line, callout, photo=None, brief=""):
        def f(n):
            return f'''<div class="es-slide">{self._top(n)}
<div class="es-bottom-text"><span class="label es-eyebrow">{eyebrow}</span><h2 class="slide-title">{title}</h2>
<p class="body-lg es-muted">{line}</p><div class="es-callout body">{callout}</div></div>
{self._photo("es-bottom-photo", photo, brief)}{self._prog(n)}</div>'''
        return self._add("bottom", False, f)

    def save(self, eyebrow, title, checks, cue="Save &amp; share with your team"):
        def f(n):
            li = "".join(f'<li>{CHECK}<span class="body">{c}</span></li>' for c in checks)
            return f'''<div class="es-slide es-slide--sky">{self._top(n)}
<div class="es-save-head"><span class="label es-eyebrow">{eyebrow}</span><h2 class="slide-title">{title}</h2></div>
<div class="es-save-card"><ul class="es-checks">{li}</ul></div>
<div class="es-save-cue button"><svg viewBox="0 0 30 34" aria-hidden="true"><path d="M2 2H28V32L15 23L2 32Z"/></svg> {cue}</div>{self._prog(n)}</div>'''
        return self._add("save", False, f)

    def follow(self, title="Weekly sales playbooks for <em>edtech teams.</em>",
               sub="Scripts, frameworks and marketing ideas that close more admissions."):
        def f(n):
            return f'''<div class="es-slide"><div class="es-final">
<img class="es-final-mark" src="../_system/logos/esm-mark.svg" alt="EdTech Sales Master">
<h2 class="slide-title">{title}</h2><p class="body-lg">{sub}</p>
<span class="es-pill button">Follow for more <svg viewBox="0 0 30 30" aria-hidden="true"><path d="M15 5V25M5 15H25"/></svg></span></div>
<div class="es-final-sign"><div class="handle">{self.handle}</div><span class="label">Sales · Marketing · Growth</span></div>{self._prog(n)}</div>'''
        return self._add("follow", False, f)

    # --- checks + output -----------------------------------------------
    def check_rules(self):
        kinds = [k for k, _, _ in self.slides]
        darks = [d for _, d, _ in self.slides]
        problems = []
        if not 7 <= len(kinds) <= 10: problems.append(f"{len(kinds)} slides (want 7-10)")
        if kinds[0] != "hook": problems.append("slide 1 is not the hook")
        if kinds[-2] != "save": problems.append("second to last is not the save slide")
        if kinds[-1] != "follow": problems.append("last is not the follow slide")
        for i in range(2, len(darks)):  # the hook (slide 1) is exempt
            if darks[i] and darks[i - 1] and i - 1 > 0:
                problems.append(f"dark slides {i} and {i+1} are adjacent")
        return problems

    def build(self):
        total = len(self.slides)
        body = []
        for i, (_, _, fn) in enumerate(self.slides, 1):
            h = fn(i).replace("{TOTAL}", f"{total:02d}").replace(f"{{P{i}}}", f"{i/total:.3f}")
            body.append(f'<section class="s" id="s{i}">{h}</section>')
        bundle = open(os.path.join(SYS, "bundle.css")).read()
        page = f'''<!doctype html><html><head><meta charset="utf-8"><title>{os.path.basename(self.folder)}</title>
<style>{bundle}
{tokens_css()}
html,body{{margin:0;background:#8a93a3}}
.s{{display:block;width:1080px;height:1350px;margin:0 0 24px}}
body.one .s{{display:none;margin:0}} body.one .s.on{{display:block}}
</style></head><body>
{"".join(body)}
<script>
var m=location.search.match(/slide=(\\d+)/);
if(m){{document.body.classList.add('one');document.getElementById('s'+m[1]).classList.add('on');}}
</script></body></html>'''
        out = os.path.join(self.folder, "slides.html")
        open(out, "w").write(page)
        return out, total

    def export(self):
        out, total = self.build()
        png = os.path.join(self.folder, "png"); os.makedirs(png, exist_ok=True)
        import time
        for i in range(1, total + 1):
            cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                   "--window-size=1080,1350", "--virtual-time-budget=10000", "--allow-file-access-from-files",
                   f"--screenshot={png}/{i:02d}.png", f"file://{out}?slide={i}"]
            for attempt in range(4):  # headless Chrome occasionally exits 2 transiently
                if subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                    break
                time.sleep(2 + attempt * 2)
            else:
                raise RuntimeError(f"Chrome failed to render slide {i} after 4 tries")
        return total
