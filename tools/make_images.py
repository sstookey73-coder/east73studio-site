"""
Regenerate the site's favicons and Open Graph images.

You only need this if the logo, app icon, or OG design changes; the
output files are committed, so the site itself has no build step.

Needs Python with: pillow, resvg-py
    pip install pillow resvg-py
Run from the repo root:
    python tools/make_images.py
"""

import io
from pathlib import Path

import resvg_py
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "images" / "brand"
EXPRESSED = ROOT / "images" / "expressed"
TOOLS = ROOT / "tools"

PAPER = "#FAF8F4"
INK_MUTED = "#6B675F"
BLUE = "#004AAD"
EXPRESSED_BG = "#141414"
EXPRESSED_MUTED = "#A3A3A3"


def svg_png(svg_path, width=None, height=None, recolor=None):
    svg = Path(svg_path).read_text(encoding="utf-8")
    if recolor:
        for a, b in recolor.items():
            svg = svg.replace(a, b)
    data = resvg_py.svg_to_bytes(svg_string=svg, width=width, height=height)
    return Image.open(io.BytesIO(bytes(data))).convert("RGBA")


def centered(canvas, im, y=None):
    x = (canvas.width - im.width) // 2
    y = (canvas.height - im.height) // 2 if y is None else y
    canvas.alpha_composite(im, (x, y))


def favicons():
    # SVG favicon = the 73 badge as-is
    (ROOT / "favicon.svg").write_text((BRAND / "mark-73-badge.svg").read_text(encoding="utf-8"), encoding="utf-8")

    # favicon.ico (16/32/48) from the badge
    badge = svg_png(BRAND / "mark-73-badge.svg", width=256)
    badge.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

    # apple-touch-icon: full-bleed blue square (iOS rounds the corners itself)
    icon = Image.new("RGBA", (180, 180), BLUE)
    mark = svg_png(BRAND / "mark-73.svg", width=118, recolor={BLUE: "#FFFFFF", BLUE.lower(): "#FFFFFF"})
    centered(icon, mark)
    icon.convert("RGB").save(ROOT / "apple-touch-icon.png", optimize=True)


def og_default():
    im = Image.new("RGBA", (1200, 630), PAPER)
    logo = svg_png(BRAND / "east73-studio-logo.svg", width=560)
    centered(im, logo, y=(630 - logo.height) // 2 - 30)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(str(TOOLS / "Inter_400Regular.ttf"), 26)
    text = "Apps, books, and prints from Houston, Texas"
    w = d.textlength(text, font=f)
    d.text(((1200 - w) / 2, 470), text, font=f, fill=INK_MUTED)
    im.convert("RGB").save(ROOT / "images" / "og-default.png", optimize=True)


def og_expressed():
    im = Image.new("RGBA", (1200, 630), EXPRESSED_BG)
    icon = Image.open(EXPRESSED / "app-icon-512.webp").convert("RGBA").resize((168, 168), Image.LANCZOS)
    mask = Image.new("L", icon.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 167, 167), radius=38, fill=255)
    icon.putalpha(mask)
    centered(im, icon, y=110)
    d = ImageDraw.Draw(im)
    title = ImageFont.truetype(str(TOOLS / "Saira_600SemiBold.ttf"), 84)
    w = d.textlength("Expressed", font=title)
    d.text(((1200 - w) / 2, 300), "Expressed", font=title, fill="#FFFFFF")
    sub = ImageFont.truetype(str(TOOLS / "Inter_400Regular.ttf"), 30)
    line = "A home-bar companion that shows what you can make with what you have."
    w = d.textlength(line, font=sub)
    d.text(((1200 - w) / 2, 430), line, font=sub, fill=EXPRESSED_MUTED)
    im.convert("RGB").save(ROOT / "images" / "og-expressed.png", optimize=True)


if __name__ == "__main__":
    favicons()
    og_default()
    og_expressed()
    print("Wrote favicon.svg, favicon.ico, apple-touch-icon.png, images/og-default.png, images/og-expressed.png")
