from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "luoyang_assets" / "01_idle.png"
OUTPUT = ROOT / "app_icon.ico"


def main() -> None:
    image = Image.open(SOURCE).convert("RGBA")
    visible_mask = image.getchannel("A").point(lambda value: 255 if value > 8 else 0)
    box = visible_mask.getbbox()
    if box is None:
        raise RuntimeError("待机图没有可见人物像素")

    crop = image.crop(box)
    side = max(crop.size)
    padding = max(24, int(side * 0.08))
    icon = Image.new("RGBA", (side + padding * 2, side + padding * 2), (0, 0, 0, 0))
    icon.alpha_composite(
        crop,
        ((icon.width - crop.width) // 2, (icon.height - crop.height) // 2),
    )
    icon.save(
        OUTPUT,
        format="ICO",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    print(f"已生成：{OUTPUT}")


if __name__ == "__main__":
    main()
