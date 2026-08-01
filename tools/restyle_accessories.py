from __future__ import annotations

import argparse
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ACCESSORIES = ROOT / "accessories"
BACKUP = ROOT / "accessories_original"
CUSTOM_ASSETS = {"milk_tea_charm.png", "milk_tea_hat.png", "rainbow_sticker.png"}
DARK_ASSETS = {
    "bow_pink.png",
    "guardian_cape.png",
    "headphones.png",
    "satchel.png",
    "scarf_milk_tea.png",
    "work_badge.png",
}
ASSET_PALETTES = {
    "bow_pink.png": ((18, 19, 25), (96, 99, 113)),
    "crown_full_sugar.png": ((37, 39, 48), (181, 184, 195)),
    "crown_small.png": ((37, 39, 48), (192, 195, 204)),
    "lucky_star_halo.png": ((54, 56, 66), (190, 193, 203)),
}


def restyle_monochrome(source: Path, target: Path) -> None:
    image = Image.open(source).convert("RGBA")
    rgb = image.convert("RGB")
    alpha = image.getchannel("A")
    gray = ImageEnhance.Contrast(ImageOps.grayscale(rgb)).enhance(1.15)

    if source.name in ASSET_PALETTES:
        black, white = ASSET_PALETTES[source.name]
        recolored = ImageOps.colorize(gray, black=black, white=white)
    elif source.name in DARK_ASSETS:
        recolored = ImageOps.colorize(gray, black=(25, 26, 33), white=(208, 211, 221))
    else:
        recolored = ImageOps.colorize(gray, black=(39, 41, 50), white=(252, 252, 255))

    recolored.putalpha(alpha)
    recolored.save(target)


def high_res_canvas(source: Path, scale: int = 4) -> tuple[Image.Image, ImageDraw.ImageDraw, int, int, int]:
    base = Image.open(source)
    width, height = base.size
    base.close()
    canvas = Image.new("RGBA", (width * scale, height * scale), (0, 0, 0, 0))
    return canvas, ImageDraw.Draw(canvas), width, height, scale


def downsample(canvas: Image.Image, width: int, height: int, target: Path) -> None:
    canvas.resize((width, height), Image.Resampling.LANCZOS).save(target)


def draw_flower_charm(source: Path, target: Path) -> None:
    canvas, draw, width, height, scale = high_res_canvas(source)
    w, h = width * scale, height * scale
    dark = (38, 40, 49, 255)
    mid = (142, 146, 160, 255)
    white = (250, 250, 253, 255)
    line = max(4, int(w * 0.018))

    chain_x = int(w * 0.5)
    draw.line((chain_x, int(h * 0.08), chain_x, int(h * 0.27)), fill=dark, width=line)
    draw.ellipse((int(w * 0.46), int(h * 0.06), int(w * 0.54), int(h * 0.14)), fill=white, outline=dark, width=line)

    cx, cy = int(w * 0.5), int(h * 0.52)
    radius = int(min(w, h) * 0.19)
    petal_r = int(radius * 0.62)
    for index in range(6):
        angle = math.radians(index * 60 - 90)
        px = cx + int(math.cos(angle) * radius * 0.72)
        py = cy + int(math.sin(angle) * radius * 0.72)
        box = (px - petal_r, py - petal_r, px + petal_r, py + petal_r)
        draw.ellipse(box, fill=white, outline=dark, width=line)
    center_r = int(radius * 0.46)
    draw.ellipse((cx - center_r, cy - center_r, cx + center_r, cy + center_r), fill=mid, outline=dark, width=line)

    bow_y = int(h * 0.79)
    draw.polygon(
        [(cx, bow_y), (int(w * 0.24), int(h * 0.69)), (int(w * 0.28), int(h * 0.9))],
        fill=dark,
    )
    draw.polygon(
        [(cx, bow_y), (int(w * 0.76), int(h * 0.69)), (int(w * 0.72), int(h * 0.9))],
        fill=dark,
    )
    draw.ellipse((int(w * 0.45), int(h * 0.74), int(w * 0.55), int(h * 0.84)), fill=mid, outline=dark, width=line)
    downsample(canvas, width, height, target)


def draw_bow_hat(source: Path, target: Path) -> None:
    canvas, draw, width, height, scale = high_res_canvas(source)
    w, h = width * scale, height * scale
    dark = (32, 33, 41, 255)
    mid = (126, 130, 143, 255)
    light = (242, 243, 247, 255)
    line = max(4, int(w * 0.016))

    draw.ellipse((int(w * 0.12), int(h * 0.59), int(w * 0.88), int(h * 0.82)), fill=dark)
    draw.rounded_rectangle(
        (int(w * 0.25), int(h * 0.22), int(w * 0.75), int(h * 0.68)),
        radius=int(w * 0.12),
        fill=light,
        outline=dark,
        width=line,
    )
    draw.rectangle((int(w * 0.24), int(h * 0.5), int(w * 0.76), int(h * 0.64)), fill=mid, outline=dark, width=line)

    knot = (int(w * 0.68), int(h * 0.49))
    draw.polygon(
        [knot, (int(w * 0.79), int(h * 0.39)), (int(w * 0.82), int(h * 0.57))],
        fill=dark,
    )
    draw.polygon(
        [knot, (int(w * 0.58), int(h * 0.39)), (int(w * 0.56), int(h * 0.57))],
        fill=dark,
    )
    draw.ellipse((int(w * 0.64), int(h * 0.45), int(w * 0.72), int(h * 0.53)), fill=light, outline=dark, width=line)
    downsample(canvas, width, height, target)


def draw_flower_sticker(source: Path, target: Path) -> None:
    canvas, draw, width, height, scale = high_res_canvas(source)
    w, h = width * scale, height * scale
    dark = (42, 44, 53, 255)
    mid = (151, 155, 169, 255)
    light = (248, 248, 251, 255)
    line = max(4, int(w * 0.018))

    draw.rounded_rectangle(
        (int(w * 0.12), int(h * 0.12), int(w * 0.88), int(h * 0.88)),
        radius=int(w * 0.11),
        fill=light,
        outline=dark,
        width=line,
    )
    cx, cy = int(w * 0.5), int(h * 0.51)
    radius = int(min(w, h) * 0.18)
    petal_r = int(radius * 0.58)
    for index in range(6):
        angle = math.radians(index * 60 - 90)
        px = cx + int(math.cos(angle) * radius * 0.7)
        py = cy + int(math.sin(angle) * radius * 0.7)
        draw.ellipse(
            (px - petal_r, py - petal_r, px + petal_r, py + petal_r),
            fill=light,
            outline=dark,
            width=line,
        )
    center_r = int(radius * 0.42)
    draw.ellipse((cx - center_r, cy - center_r, cx + center_r, cy + center_r), fill=mid, outline=dark, width=line)

    for x, y in ((0.22, 0.25), (0.77, 0.72)):
        size = int(w * 0.045)
        px, py = int(w * x), int(h * y)
        draw.line((px - size, py - size, px + size, py + size), fill=dark, width=line)
        draw.line((px + size, py - size, px - size, py + size), fill=dark, width=line)
    downsample(canvas, width, height, target)


def validate() -> None:
    expected = sorted(path.name for path in BACKUP.glob("*.png"))
    actual = sorted(path.name for path in ACCESSORIES.glob("*.png"))
    if expected != actual:
        raise RuntimeError("Accessory output set does not match the backup set")

    for path in ACCESSORIES.glob("*.png"):
        image = Image.open(path).convert("RGBA")
        alpha = image.getchannel("A")
        if alpha.getbbox() is None:
            raise RuntimeError(f"Empty accessory image: {path.name}")
        corners = [alpha.getpixel((0, 0)), alpha.getpixel((image.width - 1, 0)), alpha.getpixel((0, image.height - 1)), alpha.getpixel((image.width - 1, image.height - 1))]
        if any(corners):
            raise RuntimeError(f"Accessory corners are not transparent: {path.name}")
        image.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--restore", action="store_true")
    args = parser.parse_args()

    if args.restore:
        if not BACKUP.exists():
            raise RuntimeError("No accessories_original backup exists")
        for source in BACKUP.glob("*.png"):
            shutil.copy2(source, ACCESSORIES / source.name)
        print("Restored original accessories")
        return

    if not BACKUP.exists():
        shutil.copytree(ACCESSORIES, BACKUP)

    for source in BACKUP.glob("*.png"):
        if source.name not in CUSTOM_ASSETS:
            restyle_monochrome(source, ACCESSORIES / source.name)

    draw_flower_charm(BACKUP / "milk_tea_charm.png", ACCESSORIES / "milk_tea_charm.png")
    draw_bow_hat(BACKUP / "milk_tea_hat.png", ACCESSORIES / "milk_tea_hat.png")
    draw_flower_sticker(BACKUP / "rainbow_sticker.png", ACCESSORIES / "rainbow_sticker.png")
    validate()
    print(f"Restyled {len(list(ACCESSORIES.glob('*.png')))} accessories")


if __name__ == "__main__":
    main()
