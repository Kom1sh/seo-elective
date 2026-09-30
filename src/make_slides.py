#!/usr/bin/env python3
"""Генерирует src/slides.html из данных (data.json) и текстов ниже.
Предложение электива «Веб-продвижение: SEO и GEO» для Школы Икс. Правится этот файл, затем: python3 src/make_slides.py && python3 src/build.py && python3 src/qa.py
"""
import json, pathlib, math, html
HERE = pathlib.Path(__file__).resolve().parent
D = json.load(open(HERE / "data.json", encoding="utf-8"))
BR = json.load(open(HERE / "brands.json"))
INK = "#1C1C1E"
# белые и чёрные фирменные цвета на белой плитке заменяем чернилами
for k, v in list(BR.items()):
    if v.upper() in ("#000000", "#FFFFFF", "#181717", "#191919"): BR[k] = INK
NAME = {"google": "Google", "googlesearchconsole": "Search Console", "googleanalytics": "Google Analytics", "googlegemini": "Gemini",
        "googlechrome": "Chrome", "googlemaps": "Google Maps", "googleads": "Google Ads", "anthropic": "Anthropic", "claude": "Claude",
        "perplexity": "Perplexity", "duckduckgo": "DuckDuckGo", "brave": "Brave", "semrush": "Semrush", "lighthouse": "Lighthouse",
        "cloudflare": "Cloudflare", "wordpress": "WordPress", "tildapublishing": "Tilda", "nextdotjs": "Next.js", "telegram": "Telegram",
        "vk": "VK", "reddit": "Reddit", "wikipedia": "Wikipedia", "youtube": "YouTube", "github": "GitHub", "mistralai": "Mistral",
        "deepseek": "DeepSeek", "habr": "Хабр", "maildotru": "Mail.ru", "figma": "Figma", "notion": "Notion", "githubcopilot": "Copilot",
        "googletagmanager": "Tag Manager", "matomo": "Matomo", "hotjar": "Hotjar"}

# ── штриховые иконки (свои, смысловые) ─────────────────────────────────────
UI = {
 "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/>',
 "robot": '<rect x="4.5" y="8.5" width="15" height="11" rx="2.5"/><path d="M12 8.5V4.5"/><circle cx="12" cy="3.5" r="1.2"/><circle cx="9" cy="14" r="1.3"/><circle cx="15" cy="14" r="1.3"/><path d="M2 13v3M22 13v3"/>',
 "book": '<path d="M3.5 5h6.5a2 2 0 0 1 2 2v13a2 2 0 0 0-2-2H3.5z"/><path d="M20.5 5H14a2 2 0 0 0-2 2v13a2 2 0 0 1 2-2h6.5z"/>',
 "podium": '<rect x="2.5" y="12.5" width="5.5" height="8.5" rx="1"/><rect x="9.25" y="5.5" width="5.5" height="15.5" rx="1"/><rect x="16" y="9.5" width="5.5" height="11.5" rx="1"/>',
 "link": '<path d="M10 14a4.5 4.5 0 0 0 6.4 0l2.6-2.6a4.5 4.5 0 0 0-6.4-6.4L11.2 6.4"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0L5 12.6a4.5 4.5 0 0 0 6.4 6.4l1.4-1.4"/>',
 "sitemap": '<rect x="9" y="2.5" width="6" height="4.5" rx="1"/><rect x="2.5" y="17" width="6" height="4.5" rx="1"/><rect x="15.5" y="17" width="6" height="4.5" rx="1"/><path d="M12 7v4.5M5.5 17v-5.5h13V17"/>',
 "gauge": '<path d="M4 16a8 8 0 0 1 16 0"/><path d="M12 16l4.5-5.5"/><circle cx="12" cy="16" r="1.3"/><path d="M3 20h18"/>',
 "shield": '<path d="M12 2.5 4 6v6c0 5 3.4 8.4 8 9.5 4.6-1.1 8-4.5 8-9.5V6z"/><path d="M9 12l2 2 4-4"/>',
 "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.6 2.6L16.5 9"/>',
 "no": '<circle cx="12" cy="12" r="9"/><path d="M6 6l12 12"/>',
 "phone": '<rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18.5h2"/>',
 "list": '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1.2"/><circle cx="4.5" cy="12" r="1.2"/><circle cx="4.5" cy="18" r="1.2"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 "quote": '<path d="M4 15V9a3 3 0 0 1 3-3h2v5H6v4H4z"/><path d="M14 15V9a3 3 0 0 1 3-3h2v5h-3v4h-2z"/>',
 "chat": '<path d="M4 5.5h16v10H10l-5 4v-4H4z"/>',
 "doc": '<path d="M6 2.5h8l4 4v15H6z"/><path d="M14 2.5v4h4"/><path d="M9 12h6M9 16h6"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18a14 14 0 0 1 0-18z"/>',
 "megaphone": '<path d="M3 10v4l11 4V6z"/><path d="M14 6v12"/><path d="M17.5 9.5a3 3 0 0 1 0 5"/><path d="M6 14l1.5 5"/>',
 "pin": '<path d="M12 21.5s-7-6.2-7-11.3a7 7 0 0 1 14 0c0 5.1-7 11.3-7 11.3z"/><circle cx="12" cy="10" r="2.5"/>',
 "refresh": '<path d="M20 12a8 8 0 1 1-2.3-5.7"/><path d="M20 3.5v4.5h-4.5"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 "zap": '<path d="M13 2.5 5 13.5h6l-1 8 8-11h-6z"/>',
 "eye": '<path d="M1.5 12S5.5 5 12 5s10.5 7 10.5 7-4 7-10.5 7S1.5 12 1.5 12z"/><circle cx="12" cy="12" r="3"/>',
 "pen": '<path d="M4 20l3.2-.7L20 6.5a2.1 2.1 0 0 0-3-3L4.2 16.3z"/><path d="M15.5 5.5l3 3"/>',
 "arrow": '<path d="M4 12h16"/><path d="M13 5l7 7-7 7"/>',
 "coins": '<circle cx="9" cy="9" r="6"/><path d="M15.5 8.2A6 6 0 1 1 8.2 15.5"/>',
 "share": '<circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="M8.2 10.8l7.6-4.6M8.2 13.2l7.6 4.6"/>',
 "star": '<path d="M12 3l2.8 5.8 6.2.9-4.5 4.4 1.1 6.3L12 17.4l-5.6 3 1.1-6.3L3 9.7l6.2-.9z"/>',
 "flag": '<path d="M5 21V4"/><path d="M5 4h12l-2 4 2 4H5"/>',
 "home": '<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v10h13V10"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.3"/>',
 "layers": '<path d="M12 3 2.5 8 12 13l9.5-5z"/><path d="M2.5 12.5 12 17.5l9.5-5"/><path d="M2.5 17 12 22l9.5-5"/>',
}
def ui(name, cls=""): return f'<svg class="ui {cls}" viewBox="0 0 24 24" aria-hidden="true">{UI[name]}</svg>'

WORD = {"yandex": ("Яндекс", "#FC3F1D"), "chatgpt": ("ChatGPT", INK), "bing": ("Bing", "#008373"), "ahrefs": ("Ahrefs", "#FF8800"),
        "frog": ("Screaming Frog", "#4E7E2E"), "wordstat": ("Вордстат", "#FC3F1D"), "neuro": ("Нейро", "#5B3DF0"), "metrika": ("Метрика", "#FC3F1D"),
        "webmaster": ("Вебмастер", "#FC3F1D"), "pagespeed": ("PageSpeed", "#4285F4"), "tilda": ("Tilda", INK), "copilot": ("Copilot", INK),
        "alice": ("Алиса", "#5B3DF0"), "gsc": ("Search Console", "#458CF5")}
def ico(slug):
    return f'<svg class="ic" style="color:{BR.get(slug, INK)}"><use href="#i-{slug}"/></svg>'
def tile(slug, label=None, size="", extra=""):
    if slug in WORD:
        t, c = WORD[slug]; inner = f'<div class="tile word {size}" style="color:{c};{extra}">{t}</div>'
    else:
        inner = f'<div class="tile {size}" style="{extra}">{ico(slug)}</div>'
    if label is None or (slug in WORD and label == WORD[slug][0]): return inner
    return f'<div class="tl{" w" if slug in WORD else ""}">{inner}<span>{label}</span></div>'

def top(pill): return f'<div class="top"><span class="pill">{pill}</span><span class="cnt"></span></div>'
def slide(inner, title, cls=""): return f'<section class="s {cls}" data-t="{html.escape(title)}">{inner}</section>'
def sticky(kind, h, p, extra=""): return f'<div class="sticky {kind}">{extra}<h4>{h}</h4><p>{p}</p></div>'
def stat(n, l, cls=""): return f'<div class="stat {cls}"><div class="n">{n}</div><div class="l">{l}</div></div>'
def browser(url, img, w=None):
    """Окно браузера. Высота выводится из пропорций снимка, поэтому страница видна целиком."""
    st = f' style="max-width:{w}px"' if w else ""
    return f'<div class="browser"{st}><div class="bar"><i></i><i></i><i></i><span class="url">{url}</span></div><div class="shot"><img src="assets/{img}" alt=""></div></div>'
def arrow(): return '<div class="arr"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>'
def step(n, h, p, kind="", icon=None, i=0):
    ic = ui(icon, "sm") if icon else ""
    return f'<div class="step {kind} r" style="--i:{i}"><div class="hd"><span class="num">{n}</span>{ic}</div><h4>{h}</h4><p>{p}</p></div>'
def fmt(n): return f"{int(round(n)):,}".replace(",", " ")

# ── графики: SVG фиксированного размера ─────────────────────────────────────
def nice(v):
    """Округляет потолок оси до «красивого» числа: 1621 → 2000, 537 → 600, 38 → 40."""
    if v <= 0: return 1
    import math as _m
    mag = 10 ** _m.floor(_m.log10(v)); f = v / mag
    for step in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if f <= step: return step * mag
    return 10 * mag

def line_chart(points, w=760, h=330, color="#0FBCB0", fill="#C3FAF5", every=1, vline=None, ymax=None, mark_last=True, mark_peak=False, xfmt=None, dot_r=5):
    L, R, T, B = 74, 24, 28, 44
    vals = [v for _, v in points]; ymax = ymax or nice(max(vals) * 1.12) or 1
    n = len(points); xs = [L + (w - L - R) * i / max(1, n - 1) for i in range(n)]
    ys = [T + (h - T - B) * (1 - v / ymax) for v in vals]
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">']
    ticks = 4
    for k in range(ticks + 1):
        yy = T + (h - T - B) * k / ticks; vv = ymax * (1 - k / ticks)
        out.append(f'<line x1="{L}" x2="{w-R}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="#E0E2E8" stroke-width="1"/>')
        out.append(f'<text class="ax" x="{L-10}" y="{yy+5:.1f}" text-anchor="end">{fmt(vv)}</text>')
    area = f"M{xs[0]:.1f},{h-B} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in zip(xs, ys)) + f" L{xs[-1]:.1f},{h-B} Z"
    line = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    out.append(f'<path d="{area}" fill="{fill}"/>'); out.append(f'<path d="{line}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, (lab, v) in enumerate(points):
        if i == n - 1 or (i % every == 0 and n - 1 - i >= max(2, every // 2)):
            out.append(f'<text class="ax" x="{xs[i]:.1f}" y="{h-14}" text-anchor="middle">{xfmt(lab) if xfmt else lab}</text>')
    if vline is not None:
        i, txt = vline; out.append(f'<line x1="{xs[i]:.1f}" x2="{xs[i]:.1f}" y1="{T-8}" y2="{h-B}" stroke="{INK}" stroke-width="2" stroke-dasharray="6 6"/>')
        out.append(f'<text class="val" x="{xs[i]+10:.1f}" y="{T+8}" text-anchor="start">{txt}</text>')
    if mark_last:
        out.append(f'<circle cx="{xs[-1]:.1f}" cy="{ys[-1]:.1f}" r="{dot_r+2}" fill="#fff" stroke="{color}" stroke-width="4"/>')
        out.append(f'<text class="val" x="{xs[-1]-14:.1f}" y="{ys[-1]-16:.1f}" text-anchor="end" style="font-size:22px">{fmt(vals[-1])}</text>')
    if mark_peak and n > 1:
        out.append(f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="{dot_r}" fill="#fff" stroke="{color}" stroke-width="3"/>')
        out.append(f'<text class="val" x="{xs[0]+12:.1f}" y="{ys[0]-14:.1f}" text-anchor="start">{fmt(vals[0])}</text>')
    out.append("</svg>"); return "".join(out)

def bars(cats, series, w=760, h=330, suffix="", ymax=None):
    L, R, T, B = 60, 16, 30, 44
    allv = [v for _, _, vals in series for v in vals]; ymax = ymax or nice(max(allv) * 1.15) or 1
    n, m = len(cats), len(series); gw = (w - L - R) / n; bw = min(78, gw * 0.7 / m); gap = 8
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">']
    for k in range(5):
        yy = T + (h - T - B) * k / 4; out.append(f'<line x1="{L}" x2="{w-R}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="#E0E2E8"/>')
        out.append(f'<text class="ax" x="{L-10}" y="{yy+5:.1f}" text-anchor="end">{ymax*(1-k/4):.0f}{suffix}</text>')
    for ci, c in enumerate(cats):
        cx = L + gw * ci + gw / 2; total = m * bw + (m - 1) * gap; x0 = cx - total / 2
        for si, (name, color, vals) in enumerate(series):
            v = vals[ci]; x = x0 + si * (bw + gap); hh = (h - T - B) * v / ymax; y = h - B - hh
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(hh,2):.1f}" rx="8" fill="{color}"/>')
            lab = ("—" if v is None else f"{v:g}{suffix}")
            out.append(f'<text class="val" x="{x+bw/2:.1f}" y="{y-10:.1f}" text-anchor="middle">{lab}</text>')
        out.append(f'<text class="ax" x="{cx:.1f}" y="{h-14}" text-anchor="middle" style="font-size:17px;fill:{INK};font-weight:500">{c}</text>')
    out.append("</svg>"); return "".join(out)

def hbars(items, w=700, rowh=52, maxv=None, labw=300, color="#0FBCB0", fmtv=fmt, mono=False):
    maxv = maxv or max(v for _, v, *_ in items)
    h = rowh * len(items); out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">']
    for i, it in enumerate(items):
        lab, v = it[0], it[1]; col = it[2] if len(it) > 2 else color
        y = i * rowh; bw = (w - labw - 110) * v / maxv
        fam = "font-family:var(--fm);font-weight:500;font-size:16px" if mono else "font-size:18px;font-weight:500"
        out.append(f'<text x="{labw-14}" y="{y+rowh/2+6}" text-anchor="end" style="{fam};fill:{INK}">{html.escape(lab)}</text>')
        out.append(f'<rect x="{labw}" y="{y+rowh/2-14}" width="{max(bw,3):.1f}" height="28" rx="8" fill="{col}"/>')
        out.append(f'<text class="val" x="{labw+bw+12:.1f}" y="{y+rowh/2+6}">{fmtv(v)}</text>')
    out.append("</svg>"); return "".join(out)

def donut(parts, size=300, thick=46, center=""):
    r = (size - thick) / 2; c = math.pi * 2 * r; tot = sum(v for _, v, _ in parts); off = 0
    out = [f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" aria-hidden="true"><g transform="rotate(-90 {size/2} {size/2})">']
    for lab, v, col in parts:
        seg = c * v / tot
        out.append(f'<circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="{col}" stroke-width="{thick}" stroke-dasharray="{seg:.2f} {c-seg:.2f}" stroke-dashoffset="{-off:.2f}"/>')
        off += seg
    out.append("</g>")
    if center: out.append(f'<text x="{size/2}" y="{size/2+12}" text-anchor="middle" class="val" style="font-size:34px">{center}</text>')
    out.append("</svg>"); return "".join(out)

def graph(orphan=True, w=640, h=420):
    """Схема ссылок: узлы-страницы и связи; одна страница-сирота."""
    nodes = {"home": (110, 92, "Главная"), "a": (330, 74, "/guide"), "b": (500, 90, "/create"), "c": (200, 230, "/tacz"),
             "d": (400, 220, "/guide/verstak"), "e": (560, 250, "/download"), "f": (300, 360, "/blog"), "o": (100, 360, "/steam-deck")}
    edges = [("home", "a"), ("home", "b"), ("home", "c"), ("a", "d"), ("b", "d"), ("b", "e"), ("c", "f"), ("d", "f"), ("a", "c")]
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">']
    for a, b in edges:
        x1, y1, _ = nodes[a]; x2, y2, _ = nodes[b]; out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#C9CCD4" stroke-width="3"/>')
    for k, (x, y, lab) in nodes.items():
        iso = (k == "o")
        fill = "#FFC6C6" if iso else ("#C3FAF5" if k == "home" else "#F7F8FA"); stroke = "#600000" if iso else "#0FBCB0" if k == "home" else "#C9CCD4"
        nw = max(104, len(lab) * 8.4 + 18)
        out.append(f'<rect x="{x-nw/2:.1f}" y="{y-26}" width="{nw:.1f}" height="52" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        out.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" style="font-family:var(--fm);font-weight:500;font-size:13px;fill:{INK}">{lab}</text>')
    hx, hy, _ = nodes["home"]
    out.append(f'<circle cx="{hx-36}" cy="{hy-62}" r="16" fill="{INK}"/><circle cx="{hx-41}" cy="{hy-65}" r="2.5" fill="#fff"/><circle cx="{hx-31}" cy="{hy-65}" r="2.5" fill="#fff"/><path d="M{hx-42} {hy-56} q6 5 12 0" stroke="#fff" stroke-width="2" fill="none"/>')
    out.append(f'<text x="{hx-12}" y="{hy-57}" style="font-size:16px;font-weight:500;fill:{INK}">робот идёт по ссылкам</text>')
    ox, oy, _ = nodes["o"]
    out.append(f'<text x="{ox-52}" y="{oy+52}" text-anchor="start" style="font-size:16px;font-weight:500;fill:#600000">ни одной входящей ссылки</text>')
    out.append("</svg>"); return "".join(out)


def qcard(kind, label, q, meta, page, win=None):
    tail = f'<span class="pill" style="margin-top:auto;align-self:flex-start">{win}</span>' if win else ""
    return f'<div class="sticky {kind}"><span class="lab">{label}</span><div class="qcard"><div class="q">{q}</div><div class="meta">{meta}</div></div><p>{page}</p>{tail}</div>'

def plist(items, icon):
    return '<ul class="plist">' + "".join(
        f'<li>{ui(icon, "xs")}<div><b>{h}</b><i>{p}</i></div></li>' for h, p in items) + '</ul>'

def divider(n, title, sub, items):
    return slide(top("Раздел " + n) + f'<div class="body"><div class="row fill" style="gap:60px;align-items:flex-end"><div style="flex:1.2;display:flex;flex-direction:column;height:100%">'
      f'<div class="divn">{n}</div><div style="margin-top:auto"><div class="divt">{title}</div><div class="divs">{sub}</div></div></div>'
      f'<div class="divlist" style="flex:1;padding-bottom:12px">{"".join(f"<span>{x}</span>" for x in items)}</div></div></div>', f"Раздел {n}: {title}", "dark")



S = []
SNAP = "5 сентября 2026"

def nstep(h, p, icon, i=0):
    return f'<div class="step r" style="--i:{i}"><div class="hd">{ui(icon, "sm")}</div><h4>{h}</h4><p>{p}</p></div>'

def srcbar(name, rows):
    """Полоса источников трафика за 30 дней: поиск отдельно, остальное серым."""
    tot = sum(r[1] for r in rows); search = rows[0][1]; pct = search / tot * 100
    return (f'<div class="sb"><div class="sbh"><b>{name}</b><span>{fmt(tot)} визитов за 30 дней</span></div>'
            f'<div class="sbb"><i style="width:{pct:.1f}%"><em>{round(pct)}% из поиска</em></i><u></u></div>'
            f'<div class="sbl"><span>поиск — {fmt(search)}</span><span>остальное — {fmt(tot - search)}</span></div></div>')

# 1 обложка
PGC = [("Проблема", "Многие проекты Школы Икс делаются в стол."),
       ("Гипотеза", "Непонятно, как сделать, чтобы о проекте узнали и начали им пользоваться."),
       ("Цель", "Больше проектов, которые запущены и которыми пользуются.")]
S.append(slide(top("Школа Икс, предложение электива") +
  '<div class="body cover"><div class="row fill" style="gap:48px">'
  '<div style="flex:1;display:flex;flex-direction:column;min-width:0">'
  '<h1 style="font-size:70px">Веб‑продвижение:<br>SEO и GEO</h1>'
  '<p class="sub">Электив о том, как довести проект до людей: чтобы его находили в поиске и советовали нейросети.</p>'
  '<div class="who"><div><b>Егор Протасов<span class="mono" style="font-weight:500;font-size:19px;color:var(--blue);margin-left:14px">egorprotasov.ru</span></b>'
  '<br><span>SEO-специалист и PM. Проекты мапка.рф, techkio.ru, mediachef.app</span></div></div></div>'
  '<div style="width:560px;flex:none;display:flex;flex-direction:column;gap:14px;justify-content:center">'
  + "".join(f'<div class="pgc"><span>{k}</span><p>{v}</p></div>' for k, v in PGC)
  + '</div></div></div>', "Обложка", "cover"))

# 2 проблема
S.append(slide(top("Проблема") + '<h1>Проект доходит до защиты и на этом останавливается</h1>'
  '<div class="body"><div class="pipe" style="margin:auto 0 24px">'
  + step("1", "Идея", "Придумали, что сделать и для кого.", "", "flag", 0) + arrow()
  + step("2", "Разработка", "Сделали сайт, сервис или приложение.", "", "pen", 1) + arrow()
  + step("3", "Защита", "Показали комиссии, получили оценку.", "", "podium", 2) + arrow()
  + '<div class="step coral r" style="--i:3;background:var(--coral-l)"><div class="hd"><span class="num" style="background:var(--coral-d)">4</span>' + ui("user", "sm") + '</div>'
    '<h4>О проекте узнают люди</h4><p>Этого шага в учёбе нет. Проект кладут в стол.</p></div>'
  + '</div><div class="sticky yel tight" style="margin-bottom:auto;flex-direction:row;align-items:center;gap:20px">' + ui("target", "lg")
  + '<div><h4>Сколько проектов так остановилось — посчитаем</h4><p>Первым делом возьмём проекты прошлых лет и проверим, какие из них сегодня открываются и кому-то нужны.</p></div></div>'
  '</div>', "Проблема"))

# 3 гипотеза
HAVE = [("Придумать идею", "Кому это нужно и зачем."), ("Спроектировать", "Экраны, данные, логика."),
        ("Сделать", "Код, дизайн, контент."), ("Защитить", "Презентация и ответы комиссии.")]
MISS = [("Что люди ищут", "Какими словами они описывают свою задачу."),
        ("Где проект найдут", "Яндекс, Google, ответы нейросетей."),
        ("Как понять, что пришли", "Счётчик посещений и первые заявки."),
        ("Как о проекте рассказать", "Площадки, где его упомянут.")]
S.append(slide(top("Гипотеза") + '<h1>Проекты уходят в стол, потому что никто не учит приводить к ним людей</h1>'
  '<div class="body"><div class="g2" style="margin:auto 0;align-items:stretch">'
  f'<div class="sticky grey tight big"><span class="lab">Чему учат сейчас</span>{plist(HAVE, "check")}</div>'
  f'<div class="sticky yel tight big"><span class="lab">Чего не хватает, чтобы проект запустился</span>{plist(MISS, "search")}</div>'
  '</div></div>', "Гипотеза"))

# 4 откуда люди
S.append(slide(top("Почему поиск") + '<h1>На двух моих сайтах больше 80% посетителей пришли из поиска</h1>'
  '<div class="body"><div class="row fill" style="gap:48px;align-items:center">'
  f'<div style="flex:1.35;display:flex;flex-direction:column;gap:40px">{srcbar("techkio.ru", D["techkio_sources30"])}{srcbar("мапка.рф", D["mapka_sources30"])}</div>'
  '<div style="flex:1;display:flex;flex-direction:column;gap:16px">'
  + sticky("teal", "Рекламы нет", "В Метрике у обоих сайтов нет ни одного перехода с рекламы. Люди сами ищут, что им нужно.")
  + sticky("grey", "Сайт должен быть там, где ищут", "Если проекта нет в поиске, о нём узнают только знакомые автора.")
  + f'</div></div><p class="foot">Яндекс Метрика, источники визитов за 30 дней до {SNAP}. В «остальное» входят прямые заходы, ссылки с других сайтов и соцсети.</p></div>', "Почему поиск"))

# 5 скорость
W = D["techkio_weekly"]
pts = [(d[8:10] + "." + d[5:7], v) for d, v in W]
S.append(slide(top("Сколько это занимает") + f'<h1>techkio.ru за шесть недель дошёл до {fmt(W[-1][1])} посетителей из поиска в неделю</h1>'
  '<div class="body"><div class="row fill" style="gap:36px;align-items:center">'
  f'<div class="chart" style="flex:1.3">{line_chart(pts, w=840, h=420, color="#0FBCB0", fill="#C3FAF5")}'
  '<div class="leg"><span>визиты из поиска за неделю, начало недели</span></div></div>'
  '<div style="flex:1" class="sticky yel tight"><span class="lab">Что для этого сделано</span>'
  + plist([("Собрали запросы", "Что люди ищут про моды и сервер."),
           ("Сделали страницы под них", "Гайды, ответы на частые вопросы."),
           ("Связали страницы ссылками", "Чтобы поиск нашёл каждую."),
           ("Подключили Вебмастер и Метрику", "Видно, что работает, а что нет.")], "check")
  + f'</div></div><p class="foot">Яндекс Метрика, techkio.ru: счётчик стоит с 15 июля 2026, визиты из поисковых систем по неделям до 24 августа. Всё это — темы электива.</p></div>', "Сколько это занимает"))

# 6 программа
PROG = [("Вводное: ниша и методика", "Что поиск и нейросети дают проекту и по какой методике идём.", "цель продвижения своего проекта"),
        ("Семантика и структура", "Что ищут люди и какие страницы под это нужны. Подключаем Вебмастер, Search Console, Метрику и GA4.", "запросы, карта сайта и аналитика"),
        ("On-Page: техника", "Чтобы поиск видел и быстро открывал каждую страницу.", "все страницы проекта в поиске"),
        ("On-Page: контент", "Заголовки, тексты и ответы, которые находят поиск и нейросети.", "главные страницы под запросы"),
        ("Off-page: ссылки, PBN, крауд", "Ссылки с других сайтов, свои сети сайтов и упоминания на форумах.", "план, где о проекте напишут"),
        ("Собираем всё в кучу", "Проверяем проект по всем шагам и запускаем.", "проект в поиске и первые посетители"),
        ("Программатик SEO", "Сотни страниц из шаблона и таблицы данных, как 105 посадочных Мапки.", "план таких страниц для проекта")]
S.append(slide(top("Программа") + '<h1>Семь занятий. После каждого у проекта появляется что-то рабочее</h1>'
  '<div class="body"><div class="chk" style="margin:auto 0">'
  + "".join(f'<div class="ck"{" style=\"grid-column:1 / -1\"" if i == len(PROG) else ""}><span class="num">{i}</span><div><h5>{h}</h5><p>{d} На выходе: {r}.</p></div></div>'
            for i, (h, d, r) in enumerate(PROG, 1))
  + '</div><p class="foot">Теория на живых сайтах, практика на своём проекте или учебном. Посадочные Мапки — карта сайта мапка.рф, 14.09.2026.</p></div>', "Программа"))

# 7 как измерим
CRIT = [("Открывается", "Проект доступен по своему адресу, а не только на ноутбуке автора."),
        ("Есть в поиске", "Страницы проекта находятся в Яндексе и Google."),
        ("Пришли люди", "В Метрике видны первые посетители из поиска.")]
S.append(slide(top("Как поймём, что сработало") + '<h1>Считаем запущенные проекты до электива и после него</h1>'
  '<div class="body"><div style="display:flex;flex-direction:column;gap:24px;margin:auto 0">'
  '<div class="g3">' + "".join(f'<div class="sticky teal tight"><span class="num">{i}</span><h4>{h}</h4><p>{t}</p></div>' for i, (h, t) in enumerate(CRIT, 1)) + '</div>'
  '<div class="pipe">'
  + nstep("Первое занятие", "Проверяем по трём признакам проекты участников и проекты прошлых лет.", "list", 0) + arrow()
  + nstep("Последнее занятие", "Проверяем проекты участников по тем же признакам.", "flag", 1) + arrow()
  + nstep("Сравниваем", "Разница — сколько проектов электив довёл до людей.", "target", 2)
  + '</div></div><p class="foot">Проект считается запущенным, только если выполнены все три признака.</p></div>', "Как измерим"))

# 8 что нужно
S.append(slide(top("Что нужно") + '<h1>Для пилота нужен один семестр и место в расписании</h1>'
  '<div class="body"><div class="g2" style="margin:auto 0;align-items:stretch">'
  '<div class="sticky teal tight big"><span class="lab">Что уже есть</span>'
  + plist([("Факультатив по субботам", "Серия из пяти встреч, материалы на <span style=\"white-space:nowrap\">kom1sh.github.io/seo-course</span>."),
           ("Интерес студентов", "На идею факультатива откликнулись 14 человек в чате курса."),
           ("Живые примеры", "На занятиях разбираем настоящие сайты: мапка.рф и techkio.ru.")], "check")
  + '</div><div class="sticky yel tight big"><span class="lab">Что нужно от школы</span>'
  + plist([("Место в расписании", "Один семестр, семь занятий."),
           ("Зачёт за электив", "Чтобы участие было частью учёбы."),
           ("Список проектов прошлых лет", "Чтобы посчитать, сколько из них живы сейчас.")], "arrow")
  + '</div></div><p class="foot">Связь: Telegram @Kom1sh.</p></div>', "Что нужно"))

out = "\n".join(S)
(HERE / "slides.html").write_text(out, encoding="utf-8")
print("slides.html:", len(S), "слайдов,", len(out.encode()) // 1024, "КБ")
