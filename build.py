"""Build the Trivima print showcase site, QR codes and a printable QR sheet.

Usage:  python build.py
Outputs (in this folder):
  index.html, <slug>.html      -> pages served by GitHub Pages
  qr/<slug>.svg, qr/<slug>.png -> QR codes pointing at each page
  qr-sheet.html                -> A4 sheet, each QR exactly 3.5 cm x 3.5 cm
"""
import html
import os

import base64
import io
import math
import random

import qrcode
from PIL import Image, ImageDraw
from qrcode.constants import ERROR_CORRECT_H

BASE_URL = "https://saatvik-nbil.github.io/trivima-prints/"
QR_MM = 35.0  # printed size: black symbol (square codes) or circle diameter (circular codes)
ROOT = os.path.dirname(os.path.abspath(__file__))
CIRCULAR = {"gummy-np", "spiral", "gyroid"}  # these get the circular badge style

LOGO = Image.open(os.path.join(ROOT, "assets", "nbil-icon.png")).convert("RGBA")
_buf = io.BytesIO()
LOGO.resize((400, 400), Image.LANCZOS).save(_buf, "PNG", optimize=True)
LOGO_B64 = base64.b64encode(_buf.getvalue()).decode()

PRINTS = [
    {
        "slug": "gummy-dlp",
        "title": "Gummy Bear (Medicated Gummy)",
        "platform": "Trivima Aura",
        "process": "DLP",
        "body": [
            "This gummy bear was printed on the Trivima Aura DLP platform from a photocurable, gelatin-based edible resin. It shows a route to personalized oral dosage forms, where the drug load, size and release profile can be tuned for each patient.",
            "The same approach applies to food printing, such as custom-shaped confectionery, vitamin-fortified gummies, and functional foods with controlled nutrient content.",
            "Trivima Aura's layer-by-layer curing gives fine surface detail and accurate shapes, which makes on-demand, personalized edible products possible in both pharmaceutical and food applications.",
        ],
    },
    {
        "slug": "ear",
        "title": "Human Ear",
        "platform": "Trivima Aura",
        "process": "DLP",
        "body": [
            "This anatomically accurate human ear was printed on Trivima Aura to show the platform's ability to reproduce complex freeform anatomy. Its curved helix, antihelix and concha folds are captured at high resolution with no support artifacts on the visible surfaces.",
            "Prints like this support auricular tissue engineering, where patient-specific scaffolds can be seeded with chondrocytes to rebuild cartilage. They also work as surgical planning models and as training aids.",
        ],
    },
    {
        "slug": "grid",
        "title": "Precise Grid Structure",
        "platform": "Trivima Aura",
        "process": "DLP",
        "body": [
            "This high-fidelity grid lattice was printed on Trivima Aura to benchmark its XY resolution, layer accuracy and pore uniformity. Its evenly spaced struts and open pores show tight dimensional control across the whole build area.",
            "These interconnected porous architectures are the basis of tissue engineering scaffolds, because they allow nutrient diffusion, cell infiltration and vascularization. The print also serves as a calibration standard for Trivima Aura's exposure and printing parameters.",
        ],
    },
    {
        "slug": "cornea",
        "title": "Cornea",
        "platform": "Trivima Aura",
        "process": "DLP",
        "body": [
            "This thin, dome-shaped corneal construct was printed on Trivima Aura to reproduce the natural curvature and transparency of the human cornea. Printing a smooth, optically clear curved surface with a uniform thin wall shows the platform's fine Z-resolution and surface finish.",
            "The work targets corneal tissue engineering and implant development, which could help address the global shortage of donor corneas. Constructs like this can also act as in-vitro models for ophthalmic drug testing.",
        ],
    },
    {
        "slug": "nbil-chip",
        "title": "“NBIL” Microfluidic Chip",
        "platform": "Trivima Aura",
        "process": "DLP",
        "body": [
            "This microfluidic chip was printed on Trivima Aura and has an embedded channel shaped like the letters “NBIL”, representing Next Big Innovation Labs. It shows that the platform can produce enclosed, perfusable microchannels in complex custom geometries in a single print.",
            "The sharp corners and continuous flow paths of the lettering show how precisely the internal channels are defined. This capability supports rapid prototyping of lab-on-a-chip and organ-on-a-chip devices without traditional cleanroom lithography.",
        ],
    },
    {
        "slug": "branch-chip",
        "title": "Interconnected Branching Microchip",
        "platform": "Trivima Aura",
        "process": "DLP",
        "body": [
            "This microfluidic chip was printed on Trivima Aura and has a network of interconnected branching channels, with four inlet ports and four outlet ports. Because every branch is linked, fluids from different inlets can mix, redistribute and flow along several paths across the chip, much like the interconnected capillary beds in living tissue.",
            "Designs like this are useful for multi-reagent mixing, concentration-gradient generation, perfusion of organ-on-a-chip models, and studies of flow dynamics and shear stress. The print shows that Trivima Aura can produce complex, enclosed, leak-free channel networks with multiple ports in a single print.",
        ],
    },
    {
        "slug": "gyroid",
        "title": "Spherical Gyroid",
        "platform": "Trivima Pro",
        "process": "Extrusion · FRESH",
        "body": [
            "This spherical gyroid scaffold was extrusion-printed on Trivima Pro using the FRESH (Freeform Reversible Embedding of Suspended Hydrogels) technique, then released from the support bath and suspended in buffer. Its spherical shape mimics organoids and spheroids, the 3D cell clusters widely used to model tissue function, disease and drug response.",
            "Unlike self-assembled spheroids, this print has a defined, interconnected gyroid pore network that lets nutrients and oxygen reach its core, which could help prevent the necrotic centers common in large spheroids.",
            "Printing it shows that Trivima Pro can make reproducible, size-controlled, architecturally defined 3D tissue models for drug screening, disease modeling and regenerative research.",
        ],
    },
    {
        "slug": "gummy-np",
        "title": "Gummy Bear",
        "platform": "Trivima NP",
        "process": "Extrusion",
        "body": [
            "This gummy bear was extrusion-printed on Trivima NP from a soft, gel-based material and then suspended in buffer. Its 3D shape and layer definition stay intact after immersion, which shows the print's structural stability in a hydrated environment.",
            "In food technology, this supports printing gel-based foods with custom textures and shapes, such as texture-modified meals for people with swallowing difficulties (dysphagia), personalized nutrition and novel confectionery.",
            "The same approach also applies to soft, drug-loaded dosage forms and hydrogel constructs for biomedical use.",
        ],
    },
    {
        "slug": "spiral",
        "title": "Spiral / Spring",
        "platform": "Trivima Pro",
        "process": "Extrusion · FRESH",
        "body": [
            "This continuous spiral (spring) was extrusion-printed on Trivima Pro directly inside a FRESH support bath. The bath holds each coil in place as it is deposited, so the helix needs no extra support structures.",
            "The print shows that Trivima Pro can produce suspended, unsupported filament paths with consistent pitch and diameter. Helical geometries like this are relevant to tubular tissues, vascular grafts and flexible soft-robotic or actuator components.",
        ],
    },
    {
        "slug": "tooth",
        "title": "Wisdom Tooth Crown",
        "platform": "Trivima NP",
        "process": "Extrusion",
        "body": [
            "This anatomically shaped crown of a wisdom tooth (third molar) was extrusion-printed on Trivima NP, built up layer by layer to reproduce the tooth's cusps, grooves and occlusal surface. Capturing these fine, irregular surface features shows the platform's precision on small, patient-specific anatomical geometries.",
            "Printed dental structures like this can be used for custom crowns and restorations, dental tissue engineering scaffolds, and preoperative planning models for third-molar procedures. Prints like this also serve as training models for dental education and as test pieces for evaluating new dental biomaterials.",
        ],
    },
    {
        "slug": "btcp-grid",
        "title": "β-TCP Stacked Grid",
        "platform": "Trivima Pro",
        "process": "Melt Extrusion",
        "body": [
            "This stacked grid scaffold was printed on Trivima Pro in its melt extrusion configuration, from a β-tricalcium phosphate (β-TCP) based material in 22 layers, with filaments laid in alternating directions.",
            "β-TCP is a biocompatible, osteoconductive and bioresorbable ceramic that closely matches the mineral phase of natural bone, which makes it a leading material for bone graft substitutes. The regular, interconnected macropores support bone cell attachment, vascular ingrowth and new bone formation as the material gradually resorbs.",
            "The print shows that Trivima Pro can process high-temperature, ceramic-loaded materials into precise, patient-specific scaffolds for bone tissue engineering, including orthopedic, dental and craniofacial applications.",
        ],
    },
]

CSS = """
:root{--bg:#f6f7f9;--card:#fff;--text:#14181f;--muted:#5b6472;--accent:#0b6bcb;--chip:#e8f0fb;--line:#e3e6eb}
@media (prefers-color-scheme:dark){:root{--bg:#0f1216;--card:#171b21;--text:#e8ebef;--muted:#9aa3ae;--accent:#5aa9ff;--chip:#1c2a3c;--line:#262c34}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:17px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;-webkit-text-size-adjust:100%}
.wrap{max-width:680px;margin:0 auto;padding:20px 16px 40px}
.brand{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:14px}
.brand b{color:var(--text)}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px 20px}
h1{font-size:26px;line-height:1.25;margin:0 0 12px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px}
.chip{background:var(--chip);color:var(--accent);font-size:13px;font-weight:600;padding:4px 10px;border-radius:999px}
p{margin:0 0 14px}
p:last-child{margin-bottom:0}
a{color:var(--accent);text-decoration:none}
.foot{margin-top:18px;font-size:14px;color:var(--muted);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
ul.list{list-style:none;margin:0;padding:0}
ul.list li{border-top:1px solid var(--line)}
ul.list li:first-child{border-top:0}
ul.list a{display:flex;justify-content:space-between;gap:12px;padding:14px 2px;color:var(--text)}
ul.list span{color:var(--muted);font-size:14px;white-space:nowrap}
"""


def page(title, inner):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<style>{CSS}</style></head>
<body><main class="wrap">
<div class="brand"><b>Next Big Innovation Labs</b> &middot; Trivima</div>
{inner}
</main></body></html>
"""


def build_pages():
    for i, p in enumerate(PRINTS, 1):
        paras = "\n".join(f"<p>{html.escape(t)}</p>" for t in p["body"])
        inner = f"""<article class="card">
<h1>{html.escape(p['title'])}</h1>
<div class="chips"><span class="chip">{html.escape(p['platform'])}</span><span class="chip">{html.escape(p['process'])}</span></div>
{paras}
</article>
<div class="foot"><a href="./">&larr; All prints</a><span>Print {i} of {len(PRINTS)}</span></div>"""
        with open(os.path.join(ROOT, p["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(page(f"{p['title']} – {p['platform']}", inner))

    items = "\n".join(
        f'<li><a href="{p["slug"]}.html">{html.escape(p["title"])}<span>{html.escape(p["platform"])}</span></a></li>'
        for p in PRINTS
    )
    inner = f"""<article class="card"><h1>Trivima Print Showcase</h1>
<p style="color:var(--muted)">Prints made on Trivima Aura (DLP), Trivima Pro and Trivima NP (extrusion).</p>
<ul class="list">{items}</ul></article>"""
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page("Trivima Print Showcase", inner))


def qr_matrix(url):
    """Module matrix (no quiet zone). Level H so the centre logo is tolerated."""
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, border=0)
    qr.add_data(url)
    qr.make(fit=True)
    return qr.version, [list(r) for r in qr.get_matrix()]


def logo_size(n):
    """Odd number of modules for the white logo backing (~27% of symbol width)."""
    k = round(n * 0.27)
    return k if k % 2 else k + 1


def is_finder(r, c, n):
    return (r < 7 and c < 7) or (r < 7 and c >= n - 7) or (r >= n - 7 and c < 7)


class Canvas:
    """Draws the same shapes to SVG (vector, for printing) and PIL (PNG)."""

    def __init__(self, size, px_per_module=24):
        self.size, self.s = size, px_per_module
        self.svg = []
        self.im = Image.new("RGB", (round(size * px_per_module),) * 2, "white")
        self.d = ImageDraw.Draw(self.im)

    def rect(self, x, y, w, h, fill="#000", r=0):
        self.svg.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r:g}" fill="{fill}"/>')
        s = self.s
        box = [x * s, y * s, (x + w) * s - 1, (y + h) * s - 1]
        if r:
            self.d.rounded_rectangle(box, radius=r * s, fill=fill)
        else:
            self.d.rectangle(box, fill=fill)

    def circle(self, cx, cy, rad, fill="#000"):
        self.svg.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{rad:g}" fill="{fill}"/>')
        s = self.s
        self.d.ellipse([(cx - rad) * s, (cy - rad) * s, (cx + rad) * s, (cy + rad) * s], fill=fill)

    def ring(self, cx, cy, rad, width, fill="#000"):
        self.svg.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{rad:g}" fill="none" stroke="{fill}" stroke-width="{width:g}"/>')
        s = self.s
        self.d.ellipse([(cx - rad - width / 2) * s, (cy - rad - width / 2) * s,
                        (cx + rad + width / 2) * s, (cy + rad + width / 2) * s],
                       outline=fill, width=max(1, round(width * s)))

    def logo(self, cx, cy, size):
        x, y = cx - size / 2, cy - size / 2
        self.svg.append(f'<image x="{x:g}" y="{y:g}" width="{size:g}" height="{size:g}" href="data:image/png;base64,{LOGO_B64}"/>')
        px = round(size * self.s)
        icon = LOGO.resize((px, px), Image.LANCZOS)
        self.im.paste(icon, (round(x * self.s), round(y * self.s)), icon)

    def save(self, base):
        with open(base + ".svg", "w", encoding="utf-8") as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.size:g} {self.size:g}" '
                    f'shape-rendering="geometricPrecision"><rect width="100%" height="100%" fill="#fff"/>'
                    + "".join(self.svg) + "</svg>")
        self.im.save(base + ".png", dpi=(600, 600))


def draw_finders(cv, off, n, rounded):
    r1, r2 = (1.6, 0.9) if rounded else (0, 0)
    for fr, fc in ((0, 0), (0, n - 7), (n - 7, 0)):
        x, y = off + fc, off + fr
        cv.rect(x, y, 7, 7, "#000", r1)
        cv.rect(x + 1, y + 1, 5, 5, "#fff", r1 * 0.7)
        cv.rect(x + 2, y + 2, 3, 3, "#000", r2)


def square_qr(m, base):
    """Classic square QR: black symbol + 4-module quiet zone + logo in centre."""
    n, q = len(m), 4
    cv = Canvas(n + 2 * q)
    for r in range(n):
        for c in range(n):
            if m[r][c] and not is_finder(r, c, n):
                cv.rect(q + c, q + r, 1, 1)
    draw_finders(cv, q, n, rounded=False)
    k = logo_size(n)
    mid = q + n / 2
    cv.rect(mid - k / 2, mid - k / 2, k, k, "#fff", 1.2)
    cv.logo(mid, mid, k - 1.6)
    cv.save(base)
    return QR_MM * (n + 2 * q) / n  # image width so the black symbol is QR_MM


def circular_qr(m, base, seed):
    """Circular badge: dot-style QR inside a circle filled with decorative dots.
    The whole circle is QR_MM in diameter."""
    n, gap = len(m), 2
    inner = n + 2 * gap
    D = math.ceil(inner * math.sqrt(2)) + 3
    if (D - n) % 2:
        D += 1
    off = (D - n) // 2
    cv = Canvas(D)
    c0 = D / 2
    rng = random.Random(seed)
    lo, hi = off - gap, off + n + gap
    for r in range(D):
        for c in range(D):
            if lo <= r < hi and lo <= c < hi:
                continue
            if math.hypot(c + 0.5 - c0, r + 0.5 - c0) < D / 2 - 1.9 and rng.random() < 0.5:
                cv.circle(c + 0.5, r + 0.5, 0.42)
    for r in range(n):
        for c in range(n):
            if m[r][c] and not is_finder(r, c, n):
                cv.circle(off + c + 0.5, off + r + 0.5, 0.46)
    draw_finders(cv, off, n, rounded=True)
    cv.ring(c0, c0, D / 2 - 0.35, 0.7)  # outer edge = full diameter
    k = logo_size(n) + 2
    cv.circle(c0, c0, k / 2 + 0.3, "#fff")
    cv.logo(c0, c0, (k + 0.6) * 0.72)
    cv.save(base)
    return QR_MM, n * QR_MM / D  # image width, symbol width


def build_qr():
    os.makedirs(os.path.join(ROOT, "qr"), exist_ok=True)
    cells = []
    for i, p in enumerate(PRINTS):
        # Extensionless URL (GitHub Pages serves <slug>.html) keeps every code
        # at version 6, which has no alignment pattern hidden under the logo.
        url = BASE_URL + p["slug"]
        version, m = qr_matrix(url)
        base = os.path.join(ROOT, "qr", p["slug"])
        if p["slug"] in CIRCULAR:
            img_mm, sym = circular_qr(m, base, seed=i)
            shape = f"circle {img_mm:.1f} mm, symbol {sym:.1f} mm"
        else:
            img_mm = square_qr(m, base)
            shape = f"square, symbol {QR_MM:.1f} mm"
        print(f"{p['slug']:12s} v{version}  {shape:32s} {url}")
        cells.append(
            f'<div class="cell"><img src="qr/{p["slug"]}.svg" alt="" '
            f'style="width:{img_mm:.3f}mm;height:{img_mm:.3f}mm">'
            f'<div class="t">{html.escape(p["title"])}</div>'
            f'<div class="s">{html.escape(p["platform"])} &middot; {html.escape(p["process"])}</div></div>'
        )

    sheet = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Trivima QR Sheet</title>
<style>
/* Content is kept well inside the A4 printable area (about 177 x 205 mm vs. 180 x 267 mm
   printable with 15 mm margins), so "Fit to page" never needs to shrink it: QRs stay 35 mm. */
@page{{size:A4 portrait;margin:15mm}}
html,body{{margin:0;padding:0;background:#fff}}
body{{font:10pt/1.3 system-ui,"Segoe UI",sans-serif;color:#000;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.sheet{{width:178mm;margin:0 auto}}
.grid{{display:grid;grid-template-columns:repeat(4,42mm);gap:5mm 3mm}}
.cell{{text-align:center;break-inside:avoid;border:0.2mm dashed #bbb;padding:1.5mm 0;height:62mm;box-sizing:border-box;overflow:hidden}}
.cell img{{max-width:none;display:block;margin:0 auto 1mm}}
.t{{font-weight:600;font-size:8pt;line-height:1.2;padding:0 1.5mm}}
.s{{font-size:7pt;color:#444;margin-top:0.5mm}}
.ruler{{margin-top:6mm;font-size:7.5pt;color:#444;display:flex;align-items:center;gap:3mm}}
.ruler i{{display:block;width:35mm;height:2.5mm;border:0.3mm solid #000;border-top:0;box-sizing:border-box}}
</style></head><body>
<div class="sheet">
<div class="grid">{''.join(cells)}</div>
<div class="ruler"><i></i><span>Check: this bar should measure exactly 3.5 cm &mdash; the black square of each square QR, and the diameter of each circular QR.</span></div>
</div>
</body></html>
"""
    with open(os.path.join(ROOT, "qr-sheet.html"), "w", encoding="utf-8") as f:
        f.write(sheet)


if __name__ == "__main__":
    build_pages()
    build_qr()
