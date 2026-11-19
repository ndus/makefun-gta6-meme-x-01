"""Compose the GTA 6 loading-screen meme from scratch with Pillow.

No image assets are loaded: the sunset, the palms, the skyline, the sun and
the make.fun ghost are all drawn with Pillow primitives, so the script runs
anywhere Pillow and a bold sans font exist. The picture it draws is the one
in meme.png: a Vice-City sunset, a loading bar that finally reached 100%
after 13 years, and the make.fun ghost holding a controller.

Usage: python3 make_meme.py [output.png]   (default: meme.png beside here)
"""

import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SS = 2  # supersampling factor; the canvas is drawn big and shrunk at the end
W = 1200
HORIZON = 745  # y of the skyline base, in final-image pixels
INK = (24, 8, 18)
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def u(v):
    """Scale a final-image measure to the supersampled canvas."""
    return int(round(v * SS))


def font(size):
    return ImageFont.truetype(FONT_PATH, u(size))


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky(canvas):
    """Paint the sunset: purple up top melting into orange at the horizon."""
    stops = [
        (0.00, (43, 12, 74)),
        (0.30, (106, 27, 105)),
        (0.52, (196, 45, 110)),
        (0.62, (255, 140, 90)),
        (0.625, (46, 20, 38)),
        (1.00, (30, 12, 26)),
    ]
    d = ImageDraw.Draw(canvas)
    for y in range(canvas.height):
        t = y / (canvas.height - 1)
        for (ta, ca), (tb, cb) in zip(stops, stops[1:]):
            if ta <= t <= tb:
                d.line([(0, y), (canvas.width, y)], fill=mix(ca, cb, (t - ta) / (tb - ta)))
                break


def star(cx, cy, r, points=4, pinch=0.30):
    """Points of a sparkle: long tips on the axes, pinched between them."""
    pts = []
    for i in range(points * 2):
        ang = math.pi * i / points - math.pi / 2
        rad = r if i % 2 == 0 else r * pinch
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


def sun_and_skyline(d):
    cx, cy, r = u(565), u(660), u(218)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(232, 49, 140), outline=INK, width=u(9))
    # Skyline blocks sit on the horizon and cut across the sun's lower half.
    blocks = [(0, 70, 60), (95, 95, 45), (160, 80, 78), (255, 130, 62), (330, 105, 40),
              (415, 88, 55), (880, 92, 48), (960, 120, 66), (1065, 84, 42), (1130, 100, 70)]
    for x, w, h in blocks:
        d.rectangle([u(x), u(HORIZON - h), u(x + w), u(HORIZON + 4)], fill=INK)
    # The ground swallows the sun's lower half: repaint below the horizon in
    # the ground tone before the road stripes go on top of it.
    d.rectangle([0, u(HORIZON), u(W), u(905)], fill=(34, 15, 30))
    d.rectangle([0, u(HORIZON), u(W), u(HORIZON + 10)], fill=INK)


def palm(d, base_x, lean, height, spread=1.0):
    """One palm: a curved trunk plus a crown of drooping fronds."""
    top_x = base_x + lean
    top_y = HORIZON - height
    prev = (u(base_x), u(HORIZON + 6))
    for i in range(1, 13):
        t = i / 12
        x = base_x + lean * t * t
        y = HORIZON + 6 - height * t
        d.line([prev, (u(x), u(y))], fill=INK, width=u(17 * (1 - t * 0.55)))
        prev = (u(x), u(y))
    for sign, lift, reach in [(-1, 120, 210), (-1, 70, 250), (-1, 10, 235),
                              (1, 115, 205), (1, 62, 252), (1, 4, 228), (0, 150, 120)]:
        ex = top_x + sign * reach * spread
        ey = top_y - lift * 0.12 + reach * 0.58
        mx = top_x + sign * reach * 0.45 * spread
        my = top_y - lift
        pts = []
        for i in range(17):
            t = i / 16
            x = (1 - t) ** 2 * top_x + 2 * (1 - t) * t * mx + t ** 2 * ex
            y = (1 - t) ** 2 * top_y + 2 * (1 - t) * t * my + t ** 2 * ey
            pts.append((u(x), u(y)))
        d.line(pts, fill=INK, width=u(13), joint="curve")


def ground_detail(d):
    """A dark road running to the horizon, drawn as converging stripes."""
    cx = u(610)
    for i in range(9):
        t = i / 9
        y = HORIZON + 26 + t * t * 165
        half = 14 + t * 120
        d.line([cx - u(half), u(y), cx + u(half), u(y)], fill=(74, 44, 66), width=u(4))


def ghost(d, x, y, w, h):
    """The make.fun ghost: white body, sparkle eyes, controller in hand."""
    r = w // 2
    d.pieslice([u(x), u(y), u(x + w), u(y + w)], 180, 360, fill=(255, 255, 255), outline=INK, width=u(7))
    d.rectangle([u(x), u(y + r), u(x + w), u(y + h)], fill=(255, 255, 255))
    d.line([u(x), u(y + r), u(x), u(y + h)], fill=INK, width=u(7))
    d.line([u(x + w), u(y + r), u(x + w), u(y + h)], fill=INK, width=u(7))
    d.line([u(x), u(y + h), u(x + w), u(y + h)], fill=INK, width=u(7))
    for fx in (x + w * 0.30, x + w * 0.68):
        d.rectangle([u(fx), u(y + h - 16), u(fx + 13), u(y + h)], fill=INK)
    for ex in (x + w * 0.30, x + w * 0.70):
        d.polygon([(u(px), u(py)) for px, py in star(ex, y + h * 0.38, u(23), pinch=0.24)], fill=INK)
    # Controller, held up in front of the body.
    cw, ch = w * 0.62, h * 0.20
    cx0, cy0 = x + (w - cw) / 2, y + h * 0.55
    for ax, ay, bx, by in [(x + 4, y + h * 0.50, cx0 + 8, cy0 + ch * 0.55),
                           (x + w - 4, y + h * 0.50, cx0 + cw - 8, cy0 + ch * 0.55)]:
        d.line([u(ax), u(ay), u(bx), u(by)], fill=INK, width=u(30))
        d.line([u(ax), u(ay), u(bx), u(by)], fill=(255, 255, 255), width=u(17))
    d.rounded_rectangle([u(cx0), u(cy0), u(cx0 + cw), u(cy0 + ch)], u(26),
                        fill=(38, 34, 54), outline=INK, width=u(6))
    px, py = cx0 + cw * 0.16, cy0 + ch * 0.5
    d.line([u(px - 11), u(py), u(px + 11), u(py)], fill=(255, 255, 255), width=u(6))
    d.line([u(px), u(py - 11), u(px), u(py + 11)], fill=(255, 255, 255), width=u(6))
    for bx, col in [(cx0 + cw * 0.50, (16, 14, 24)), (cx0 + cw * 0.63, (16, 14, 24)),
                    (cx0 + cw * 0.82, (255, 64, 150)), (cx0 + cw * 0.90, (255, 170, 90))]:
        d.ellipse([u(bx - 8), u(py - 8), u(bx + 8), u(py + 8)], fill=col)
    # The star coin, pinned at the ghost's top right.
    kx, ky, kr = x + w * 0.99, y + h * 0.10, 37
    d.ellipse([u(kx - kr), u(ky - kr), u(kx + kr), u(ky + kr)], fill=(214, 51, 132), outline=INK, width=u(6))
    d.polygon([(u(px), u(py)) for px, py in star(kx, ky, u(18), points=5, pinch=0.48)], fill=(255, 255, 255))


def caption(d, cx, y, text, size, fill=(255, 255, 255), stroke=6):
    d.text((u(cx), u(y)), text, font=font(size), fill=fill, anchor="ma",
           stroke_width=u(stroke), stroke_fill=INK)


def loading_bar(d):
    x0, x1, y, h = 90, 1110, 905, 52
    d.rounded_rectangle([u(x0), u(y), u(x1), u(y + h)], u(h // 2), fill=(255, 255, 255), outline=INK, width=u(5))
    d.text((u(600), u(y + h / 2)), "100%", font=font(30), fill=INK, anchor="mm")


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("meme.png")
    img = Image.new("RGB", (u(W), u(W)), (30, 12, 26))
    sky(img)
    d = ImageDraw.Draw(img)
    sun_and_skyline(d)
    palm(d, base_x=30, lean=185, height=520)
    palm(d, base_x=1170, lean=-190, height=540)
    ground_detail(d)
    ghost(d, x=748, y=548, w=262, h=338)
    caption(d, 600, 38, "13 YEARS OF LOADING...", 79)
    loading_bar(d)
    caption(d, 600, 972, "GTA 6 - DAY ONE", 44)
    d.rectangle([0, u(1062), u(W), u(W)], fill=(16, 6, 12))
    caption(d, 600, 1080, "TIP: MY AGENT SPENT THE WAIT", 37, stroke=0)
    caption(d, 600, 1128, "EARNING REAL MONEY ON MAKE.FUN", 37, stroke=0)
    img.resize((W, W), Image.LANCZOS).save(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
