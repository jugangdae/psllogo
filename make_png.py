#!/usr/bin/env python3

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import aggdraw
from PIL import Image


TOKEN = re.compile(r"[MLCZmlcz]|[-+]?(?:\d*\.\d+|\d+\.?)(?:e[-+]?\d+)?", re.I)


def color(value):
    if value == "transparent":
        return (0, 0, 0, 0)
    value = value.lstrip("#")
    if len(value) != 6:
        raise SystemExit("background must be transparent or hex color, e.g. ffffff")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4)) + (255,)


def fill_of(el):
    style = dict(
        part.split(":", 1) for part in el.get("style", "").split(";") if ":" in part
    )
    return color(el.get("fill") or style.get("fill", "000000"))


def viewbox(root):
    return [float(x) for x in re.split(r"[,\s]+", root.get("viewBox").strip())]


def resize_rgba(image, size):
    return image.convert("RGBa").resize(size, Image.Resampling.LANCZOS).convert("RGBA")


def straight_alpha(image):
    return Image.frombytes("RGBa", image.size, image.tobytes()).convert("RGBA")


def solid_color_alpha(image, fill):
    alpha = image.getchannel("A")
    flat = Image.new("RGBA", image.size, fill)
    flat.putalpha(alpha)
    return flat


def path_of(d, min_x, min_y, scale, dx, dy):
    tokens = TOKEN.findall(d)
    path = aggdraw.Path()
    i = 0
    cmd = ""
    x = y = sx = sy = 0.0

    def point(px, py):
        return dx + (px - min_x) * scale, dy + (py - min_y) * scale

    def number():
        nonlocal i
        value = float(tokens[i])
        i += 1
        return value

    while i < len(tokens):
        if tokens[i].isalpha():
            cmd = tokens[i]
            i += 1

        rel = cmd.islower()
        op = cmd.upper()

        if op == "Z":
            path.close()
            x, y = sx, sy
            continue

        while i < len(tokens) and not tokens[i].isalpha():
            if op == "M":
                nx, ny = number(), number()
                x, y = (x + nx, y + ny) if rel else (nx, ny)
                path.moveto(*point(x, y))
                sx, sy = x, y
                op = "L"
            elif op == "L":
                nx, ny = number(), number()
                x, y = (x + nx, y + ny) if rel else (nx, ny)
                path.lineto(*point(x, y))
            elif op == "C":
                x1, y1, x2, y2, nx, ny = [number() for _ in range(6)]
                if rel:
                    x1, y1, x2, y2, nx, ny = x + x1, y + y1, x + x2, y + y2, x + nx, y + ny
                path.curveto(*point(x1, y1), *point(x2, y2), *point(nx, ny))
                x, y = nx, ny
            else:
                raise SystemExit(f"unsupported path command: {cmd}")

    return path


def output_name(svg, size, background):
    background = background.lstrip("#") if background != "transparent" else background
    return f"{svg.stem}_{size}_{background}.png"


def convert(svg, size, bg, out_dir, background):
    root = ET.parse(svg).getroot()
    min_x, min_y, width, height = viewbox(root)
    scale = size / max(width, height)

    image = Image.new("RGBA", (round(width * scale), round(height * scale)), (0, 0, 0, 0))
    draw = aggdraw.Draw(image)
    fills = []

    for el in root.iter():
        if el.tag.endswith("path"):
            fill = fill_of(el)
            fills.append(fill)
            draw.path(path_of(el.get("d"), min_x, min_y, scale, 0, 0), aggdraw.Brush(fill))

    draw.flush()
    image = straight_alpha(image)

    bbox = image.getbbox()
    if not bbox:
        raise SystemExit(f"empty svg: {svg}")

    logo = image.crop(bbox)
    ratio = size / max(logo.size)
    logo = resize_rgba(logo, (round(logo.width * ratio), round(logo.height * ratio)))
    if len(set(fills)) == 1:
        logo = solid_color_alpha(logo, fills[0])

    image = Image.new("RGBA", (size, size), bg)
    image.alpha_composite(logo, ((size - logo.width) // 2, (size - logo.height) // 2))
    output = out_dir / output_name(svg, size, background)
    image.save(output)
    print(f"{svg} -> {output}")


def main():
    if len(sys.argv) not in (2, 3):
        raise SystemExit("usage: .venv/bin/python make_png.py <size> [background]")

    size = int(sys.argv[1])
    background = sys.argv[2] if len(sys.argv) == 3 else "transparent"
    bg = color(background)
    out_dir = Path(f"out_{size}" if background == "transparent" else f"out_{size}_{background.lstrip('#')}")
    out_dir.mkdir(exist_ok=True)

    for svg in sorted(Path("svg").glob("*.svg")):
        convert(svg, size, bg, out_dir, background)


if __name__ == "__main__":
    main()
