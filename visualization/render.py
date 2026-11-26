#!/usr/bin/env python3
"""Render the two tournaments from a shared, rotating perspective camera."""
from math import atan2, cos, hypot, pi, sin, tau
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = (664, 430)
PALETTE = ["#0b141b", "#101f29", "#243b49", "#eff5f5", "#a9bdc7", "#79e0c3", "#feb76d", "#4e7488"]
NODES = {1: (0, 1.06, -.25), 2: (-1.16, -.67, .45), 3: (1.16, -.67, .45)}
VIEW = Path(__file__).resolve().parent


def font(size, bold=False):
    names = ("Arial Bold.ttf", "DejaVuSans-Bold.ttf") if bold else ("Arial.ttf", "DejaVuSans.ttf")
    for name in names:
        for directory in (Path("/System/Library/Fonts/Supplemental"), Path("/usr/share/fonts/truetype/dejavu")):
            path = directory / name
            if path.is_file():
                return ImageFont.truetype(str(path), size)
    raise RuntimeError("Arial or DejaVu Sans is required to render the GIF")


def project(x, y, z, angle, center):
    x, z = x * cos(angle) + z * sin(angle), -x * sin(angle) + z * cos(angle)
    y, z = y * cos(.34) - z * sin(.34), y * sin(.34) + z * cos(.34)
    scale = 52 * 6 / (6 - z)
    return center + x * scale, 213 - y * scale, z


def arrow(draw, a, b, reversed_edge):
    ax, ay, _ = a
    bx, by, _ = b
    d = hypot(bx - ax, by - ay)
    if d < 14:
        return
    angle = atan2(by - ay, bx - ax)
    ux, uy = cos(angle), sin(angle)
    pad = min(22, d / 4)
    end = bx - pad * ux, by - pad * uy
    color = PALETTE[6 if reversed_edge else 7]
    draw.line((ax + pad * ux, ay + pad * uy, *end), fill=color, width=5 if reversed_edge else 4)
    draw.polygon([end, (end[0] - 15 * cos(angle + .48), end[1] - 15 * sin(angle + .48)),
                  (end[0] - 15 * cos(angle - .48), end[1] - 15 * sin(angle - .48))], fill=color)


FONTS = {"title": font(33, True), "body": font(20), "label": font(23, True),
         "node": font(21, True), "small": font(19)}


def diagram(draw, center, angle, is_cycle):
    positions = {n: project(*xyz, angle, center) for n, xyz in NODES.items()}
    flip = (3, 2) if is_cycle else (2, 3)
    arrows = [(2, 1), (1, 3), flip]
    for a, b in sorted(arrows, key=lambda e: positions[e[0]][2] + positions[e[1]][2]):
        arrow(draw, positions[a], positions[b], (a, b) == flip)
    for n, (x, y, z) in sorted(positions.items(), key=lambda item: item[1][2]):
        r = 19 + 2 * z
        draw.ellipse((x - r, y - r, x + r, y + r), fill=PALETTE[2], outline=PALETTE[5], width=2)
        draw.text((x, y), str(n), font=FONTS["node"], fill=PALETTE[3], anchor="mm")


def frame(angle):
    im = Image.new("RGB", SIZE, PALETTE[0])
    draw = ImageDraw.Draw(im)
    draw.text((26, 19), "One reversal changes the rank", font=FONTS["title"], fill=PALETTE[3])
    draw.text((26, 60), "Homoscedastic tournament  ·  exact rational example", font=FONTS["small"], fill=PALETTE[4])
    for cycle, x in ((False, 26), (True, 344)):
        draw.rounded_rectangle((x, 105, x + 294, 354), radius=18, fill=PALETTE[1], outline=PALETTE[2])
        draw.text((x + 14, 112), "H   Directed triangle" if cycle else "G   Transitive", font=FONTS["label"], fill=PALETTE[3])
        diagram(draw, x + 147, angle, cycle)
        draw.text((x + 14, 296), "Triple rank 3" if cycle else "Triple rank 2", font=FONTS["label"], fill=PALETTE[5])
        draw.text((x + 14, 325), "P = −19/64" if cycle else "P = 0", font=FONTS["body"], fill=PALETTE[3])
    draw.text((26, 365), "Triple (u, v, w) = (K11, K13, K33)", font=FONTS["body"], fill=PALETTE[3])
    draw.text((26, 395), "P = uw − v² − w²", font=FONTS["body"], fill=PALETTE[4])
    draw.text((638, 395), "s = 1, a = b = ¼, c = ½", font=FONTS["small"], fill=PALETTE[4], anchor="ra")
    return im


def main():
    palette = Image.new("P", (1, 1))
    palette.putpalette([int(color[i:i + 2], 16) for color in PALETTE for i in (1, 3, 5)] + [0, 0, 0] * (256 - len(PALETTE)))
    frames = [frame(angle).quantize(palette=palette, dither=Image.Dither.NONE)
              for angle in (tau * i / 48 - pi / 10 for i in range(48))]
    frames[0].save(VIEW / "one-edge-rank.gif", save_all=True, append_images=frames[1:],
                   optimize=True, duration=120, loop=0, disposal=1)


if __name__ == "__main__":
    main()
