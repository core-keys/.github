#!/usr/bin/env python3
"""
core-keys brand assets. Generated — do not hand-edit the PNGs.

    python3 brand/render.py

The mark is the device's own boot animation frozen at its final state: two
interlinked rings, "agent" over "person", with the crossings alternating so the
pair reads as one linked chain rather than two stacked circles, and a lit core
where they overlap. Geometry and palette are lifted from draw_rings() and the
UIC_* defines in core-keys/mule-esp32s3 (main/ui_screens.c, main/ui_screens.h)
and must stay in step with them: r 40, thickness 13, separation 30, core discs
at 0.62 and 0.34 of the ring thickness.

Everything is drawn supersampled and box-filtered down, the same trick
tools/gen_font.py uses on the device, so edges land soft without a real AA
rasteriser. Needs pillow.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
INTER = os.path.join(HERE, "fonts", "InterVariable.ttf")
OUT = HERE

SS = 4  # supersampling factor

# ---- palette (main/ui_screens.h) --------------------------------------------
BG      = (0x08, 0x0B, 0x18)
RING_A  = (0x9B, 0xB0, 0xEE)   # agent ring, drawn on top
RING_P  = (0x6D, 0x5E, 0xF0)   # person ring, drawn behind
CORE_B  = (0x6D, 0x5E, 0xF0)   # glow
CORE_G  = (0x8B, 0x7D, 0xFF)   # core disc
SPARK   = (0xE9, 0xE6, 0xFF)   # core highlight
INK     = (0xEA, 0xED, 0xFB)
SUB     = (0xAE, 0xB6, 0xD6)
MUTED   = (0x7A, 0x85, 0xAC)
LINE    = (0x21, 0x2B, 0x4E)

# ---- mark geometry, in units of the ring radius (device: r=40) --------------
TH_R  = 13.0 / 40.0   # stroke thickness
SEP_R = 30.0 / 40.0   # half the distance between the two ring centres
ARC   = 0.42          # half-width, radians, of the person-ring arc redrawn in front


def _ring(d, cx, cy, r, th, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=int(round(th)))


def draw_mark(img, cx, cy, r, lit=True):
    """The linked-ring mark, centred on (cx, cy). Mirrors draw_rings()."""
    th, sep = r * TH_R, r * SEP_R
    cyt, cyb = cy - sep, cy + sep

    # the glow sits under everything, on its own layer so it can be blurred
    if lit:
        glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gr = r * 0.78
        gd.ellipse([cx - gr, cy - gr, cx + gr, cy + gr], fill=CORE_B + (135,))
        glow = glow.filter(ImageFilter.GaussianBlur(r * 0.30))
        img.alpha_composite(glow)

    d = ImageDraw.Draw(img)
    _ring(d, cx, cyb, r, th, RING_P + (255,))          # person, behind
    _ring(d, cx, cyt, r, th, RING_A + (255,))          # agent, over it

    # redraw a short arc of the person ring at the LEFT crossing so it passes in
    # front there. That alternation is the whole trick: it reads as a chain.
    if sep < r:
        import math
        dx = math.sqrt(r * r - sep * sep)
        ang = math.atan2(-sep, -dx)
        a0, a1 = math.degrees(ang - ARC), math.degrees(ang + ARC)
        d.arc([cx - r, cyb - r, cx + r, cyb + r], a0, a1,
              fill=RING_P + (255,), width=int(round(th)))

    if lit:
        d.ellipse([cx - th * 0.62, cy - th * 0.62, cx + th * 0.62, cy + th * 0.62],
                  fill=CORE_G + (255,))
        d.ellipse([cx - th * 0.34, cy - th * 0.34, cx + th * 0.34, cy + th * 0.34],
                  fill=SPARK + (255,))


def mark_box(r):
    """(width, height) the mark occupies for ring radius r."""
    th, sep = r * TH_R, r * SEP_R
    return 2 * (r + th / 2), 2 * (sep + r + th / 2)


def face(px, instance="SemiBold"):
    f = ImageFont.truetype(INTER, px)
    f.set_variation_by_name(instance)
    return f


def text_tracked(d, xy, s, font, fill, tracking=0):
    """Inter has no tracking control in PIL; step the pen manually."""
    x, y = xy
    for ch in s:
        d.text((x, y), ch, font=font, fill=fill, anchor="ls")
        x += d.textlength(ch, font=font) + tracking
    return x


def tracked_width(d, s, font, tracking=0):
    return sum(d.textlength(c, font=font) for c in s) + tracking * (len(s) - 1)


def canvas(w, h, bg=BG):
    return Image.new("RGBA", (w * SS, h * SS), bg + (255,))


def finish(img, w, h, name):
    out = img.resize((w, h), Image.LANCZOS).convert("RGB")
    path = os.path.join(OUT, name)
    out.save(path)
    print("wrote %-28s %dx%d" % (name, w, h))
    return out


def vignette(img, cx, cy, radius, strength=48):
    """A soft lift behind the mark so the panel isn't a flat slab."""
    v = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(v).ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=(0x1B, 0x24, 0x50, strength))
    img.alpha_composite(v.filter(ImageFilter.GaussianBlur(radius * 0.55)))


# ---- assets ----------------------------------------------------------------

def banner(component=None, tagline="SPLIT-KEY AUTHENTICATOR",
           w=800, h=200, scale=2, name="banner.png"):
    # designed in logical units at w x h, emitted at 2x so it stays crisp on
    # retina when the README pins it to width=800
    img = canvas(w, h)
    s = SS
    # size the mark so it clears the panel edges: it stands 3.825 r tall
    r = ((h - 44) * s) / 3.825
    mw, _ = mark_box(r)
    gap = 40 * s

    d = ImageDraw.Draw(img)
    word = face(64 * s)
    small = face(17 * s, "Medium")
    line = tagline if not component else "%s  ·  %s" % (tagline, component.upper())
    tw = max(tracked_width(d, "core-keys", word, 2 * s),
             tracked_width(d, line, small, 3.2 * s))

    # centre the whole lockup, mark + gap + text
    total = mw + gap + tw
    left = (w * s - total) / 2
    cx = left + mw / 2
    cy = (h * s) // 2

    vignette(img, cx, cy, r * 2.4)
    draw_mark(img, cx, cy, r)

    tx = left + mw + gap
    base = cy + 1 * s
    text_tracked(d, (tx, base), "core-keys", word, INK + (255,), tracking=2 * s)
    text_tracked(d, (tx + 2 * s, base + 32 * s), line, small,
                 (CORE_G if component else SUB) + (255,), tracking=3.2 * s)

    return finish(img, w * scale, h * scale, name)


def avatar(w=460, name="avatar.png"):
    img = canvas(w, w)
    s = SS
    cx = cy = (w * s) // 2
    r = 88 * s
    vignette(img, cx, cy, r * 2.6, strength=58)
    draw_mark(img, cx, cy, r)
    return finish(img, w, w, name)


def mark_only(w=512, name="mark.png"):
    """Transparent-background mark, for slides and docs."""
    s = SS
    img = Image.new("RGBA", (w * s, w * s), (0, 0, 0, 0))
    cx = cy = (w * s) // 2
    draw_mark(img, cx, cy, 150 * s)
    out = img.resize((w, w), Image.LANCZOS)
    out.save(os.path.join(OUT, name))
    print("wrote %-28s %dx%d (transparent)" % (name, w, w))


def social(component, w=1280, h=640, name="social.png"):
    """GitHub social preview / og:image card."""
    img = canvas(w, h)
    s = SS
    cx, cy = (w * s) // 2, (h * s) // 2 - 46 * s
    r = 96 * s
    vignette(img, cx, cy, r * 2.8, strength=56)
    draw_mark(img, cx, cy, r)

    d = ImageDraw.Draw(img)
    word = face(84 * s)
    _, mh = mark_box(r)
    base = cy + mh / 2 + 92 * s
    ww = tracked_width(d, "core-keys", word, 2 * s)
    text_tracked(d, (cx - ww / 2, base), "core-keys", word, INK + (255,), tracking=2 * s)

    small = face(22 * s, "Medium")
    line = "SPLIT-KEY AUTHENTICATOR  ·  %s" % component.upper()
    lw = tracked_width(d, line, small, 4 * s)
    text_tracked(d, (cx - lw / 2, base + 40 * s), line, small, CORE_G + (255,), tracking=4 * s)
    return finish(img, w, h, name)


def svg(name="logo.svg", r=40.0):
    """The mark as SVG, from the same geometry the PNGs use.

    The chain alternation is a stroked arc of the person ring, drawn last over
    the agent ring at the left crossing — the SVG twin of the ui_arc() call in
    draw_rings().
    """
    import math
    th, sep = r * TH_R, r * SEP_R
    pad = th / 2
    w = 2 * (r + pad)
    h = 2 * (sep + r + pad)
    cx, cy = w / 2, h / 2
    cyt, cyb = cy - sep, cy + sep

    dx = math.sqrt(r * r - sep * sep)
    ang = math.atan2(-sep, -dx)
    a0, a1 = ang - ARC, ang + ARC
    p0 = (cx + r * math.cos(a0), cyb + r * math.sin(a0))
    p1 = (cx + r * math.cos(a1), cyb + r * math.sin(a1))

    hx = lambda c: "#%02X%02X%02X" % c
    out = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}"
     width="{w:.0f}" height="{h:.0f}" role="img" aria-label="core-keys">
  <title>core-keys</title>
  <g fill="none" stroke-width="{th:.2f}">
    <circle cx="{cx:.2f}" cy="{cyb:.2f}" r="{r:.2f}" stroke="{hx(RING_P)}"/>
    <circle cx="{cx:.2f}" cy="{cyt:.2f}" r="{r:.2f}" stroke="{hx(RING_A)}"/>
    <path d="M {p0[0]:.2f} {p0[1]:.2f} A {r:.2f} {r:.2f} 0 0 1 {p1[0]:.2f} {p1[1]:.2f}"
          stroke="{hx(RING_P)}" stroke-linecap="butt"/>
  </g>
  <circle cx="{cx:.2f}" cy="{cy:.2f}" r="{th * 0.62:.2f}" fill="{hx(CORE_G)}"/>
  <circle cx="{cx:.2f}" cy="{cy:.2f}" r="{th * 0.34:.2f}" fill="{hx(SPARK)}"/>
</svg>
"""
    with open(os.path.join(OUT, name), "w") as f:
        f.write(out)
    print("wrote %-28s %.0fx%.0f (vector)" % (name, w, h))


REPOS = {
    "protocol":         "PROTOCOL",
    "daemon":           "DAEMON",
    "mule-esp32s3":     "FIRMWARE",
    "case-tdisplay-s3": "CASE",
    "spec":             "SPEC",
}

def distribute():
    """Copy each repo's banner into its own checkout, if it sits alongside.

    Every repo keeps its own .github/banner.png so its README renders offline
    and on any host — this script stays the single place the art is made.
    """
    import shutil
    root = os.path.dirname(os.path.dirname(HERE))   # ~/core-keys-org
    for repo in REPOS:
        dest_dir = os.path.join(root, repo, ".github")
        if not os.path.isdir(os.path.join(root, repo, ".git")):
            print("skip %-20s (no checkout beside this one)" % repo)
            continue
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy(os.path.join(OUT, "banner-%s.png" % repo),
                    os.path.join(dest_dir, "banner.png"))
        print("copied banner -> %s/.github/banner.png" % repo)


if __name__ == "__main__":
    banner()                                   # org / generic
    for repo, label in REPOS.items():
        banner(label, name="banner-%s.png" % repo)
    avatar()
    mark_only()
    for repo, label in REPOS.items():
        social(label, name="social-%s.png" % repo)
    svg()
    distribute()
