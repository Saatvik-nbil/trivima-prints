"""Build the Trivima print showcase site, QR codes and a printable QR sheet.

Usage:  python build.py
Outputs (in this folder):
  index.html, <slug>.html      -> pages served by GitHub Pages
  qr/<slug>.svg, qr/<slug>.png -> QR codes pointing at each page
  qr-sheet.html                -> A4 sheet, each QR exactly 3.5 cm x 3.5 cm
"""
import html
import os

import qrcode
import qrcode.image.svg
from qrcode.constants import ERROR_CORRECT_H

BASE_URL = "https://saatvik-nbil.github.io/trivima-prints/"
QR_MM = 35.0  # printed size of the black QR symbol
ROOT = os.path.dirname(os.path.abspath(__file__))

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


def make_qr(url):
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, border=4, box_size=20)
    qr.add_data(url)
    qr.make(fit=True)
    return qr


def build_qr():
    os.makedirs(os.path.join(ROOT, "qr"), exist_ok=True)
    cells = []
    for p in PRINTS:
        url = BASE_URL + p["slug"] + ".html"
        qr = make_qr(url)
        qr.make_image(fill_color="black", back_color="white").save(
            os.path.join(ROOT, "qr", p["slug"] + ".png"))
        qr.make_image(image_factory=qrcode.image.svg.SvgPathFillImage).save(
            os.path.join(ROOT, "qr", p["slug"] + ".svg"))
        print(f"{p['slug']:12s} version {qr.version}  {url}")
        # Size the image so the black symbol (excluding the 4-module white quiet
        # zone on each side) is exactly QR_MM wide.
        n = qr.modules_count
        img_mm = QR_MM * (n + 2 * qr.border) / n
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
<div class="ruler"><i></i><span>Check: this bar should measure exactly 3.5 cm, the same as the black square of each QR code.</span></div>
</div>
</body></html>
"""
    with open(os.path.join(ROOT, "qr-sheet.html"), "w", encoding="utf-8") as f:
        f.write(sheet)


if __name__ == "__main__":
    build_pages()
    build_qr()
