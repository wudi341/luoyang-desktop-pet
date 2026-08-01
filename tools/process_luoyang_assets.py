from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageFilter


@dataclass(frozen=True)
class AssetSpec:
    source: str
    output: str
    method: str


ASSETS = (
    AssetSpec("task-ms91icb61z81a.png", "01_idle.png", "anime"),
    AssetSpec("task-ms94t39r2kl15-orig.png", "02_sleepy.png", "chroma"),
    AssetSpec("task-ms96ur031ecdy-orig.png", "03_arrive.png", "chroma"),
    AssetSpec("task-ms97fqbl6ktuu-orig.png", "04_goodbye.png", "chroma"),
    AssetSpec("task-ms97ft4q72neg-orig.png", "05_eat.png", "chroma"),
    AssetSpec("task-ms97r0kn9tcsy-orig.png", "06_study.png", "chroma"),
    AssetSpec("task-ms98342aag58m-orig.png", "07_shy.png", "chroma"),
    AssetSpec("task-ms983ejgbyklr-orig (1).png", "08_sleep.png", "chroma"),
    AssetSpec("task-ms98ec6wclpuf-orig.png", "09_confused.png", "chroma"),
    AssetSpec("task-ms98egvid6lmk-orig.png", "10_angry.png", "chroma"),
    AssetSpec("task-ms98pw9lejimv-orig.png", "11_cry.png", "chroma"),
    AssetSpec("task-ms98q412fix7t-orig.png", "12_celebrate.png", "chroma"),
    AssetSpec("task-ms98wtucgiril-orig.png", "13_encourage.png", "chroma"),
    AssetSpec("task-ms98wvyzhlbjy-orig.png", "14_run.png", "chroma"),
    AssetSpec("task-ms995bu8i4gi7-orig.png", "15_give_flower.png", "chroma"),
    AssetSpec("task-ms995cjsj484x-orig.png", "16_stretch.png", "chroma"),
)

CANVAS_SIZE = (2048, 2048)


def remove_anime_background(source: Path) -> Image.Image:
    try:
        from rembg import new_session, remove
    except ImportError as exc:
        raise RuntimeError(
            '缺少 rembg，请先运行：python -m pip install "rembg[cpu]"'
        ) from exc

    result = remove(source.read_bytes(), session=new_session("isnet-anime"))
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as file:
        temp_path = Path(file.name)
        file.write(result)
    try:
        with Image.open(temp_path) as image:
            return image.convert("RGBA")
    finally:
        temp_path.unlink(missing_ok=True)


def remove_chroma_background(source: Path, temp_dir: Path) -> Image.Image:
    helper = (
        Path.home()
        / ".codex"
        / "skills"
        / ".system"
        / "imagegen"
        / "scripts"
        / "remove_chroma_key.py"
    )
    if not helper.exists():
        raise RuntimeError(f"找不到绿幕处理工具：{helper}")

    output = temp_dir / f"{source.stem}-transparent.png"
    subprocess.run(
        [
            sys.executable,
            str(helper),
            "--input",
            str(source),
            "--out",
            str(output),
            "--auto-key",
            "border",
            "--soft-matte",
            "--transparent-threshold",
            "12",
            "--opaque-threshold",
            "220",
            "--despill",
            "--force",
        ],
        check=True,
    )
    with Image.open(output) as image:
        return image.convert("RGBA")


def normalize(image: Image.Image) -> Image.Image:
    # Premultiplied alpha prevents hidden green pixels bleeding into white hair.
    if image.size != CANVAS_SIZE:
        image = (
            image.convert("RGBa")
            .resize(CANVAS_SIZE, Image.Resampling.LANCZOS)
            .convert("RGBA")
        )
    alpha = image.getchannel("A")
    sharpened = image.convert("RGB").filter(
        ImageFilter.UnsharpMask(radius=2.0, percent=150, threshold=2)
    )
    result = sharpened.convert("RGBA")
    result.putalpha(alpha)
    return result


def validate(image: Image.Image, name: str) -> None:
    alpha = image.getchannel("A")
    if alpha.getbbox() is None:
        raise RuntimeError(f"{name} 没有可见人物像素")
    corners = (
        alpha.getpixel((0, 0)),
        alpha.getpixel((image.width - 1, 0)),
        alpha.getpixel((0, image.height - 1)),
        alpha.getpixel((image.width - 1, image.height - 1)),
    )
    if any(value > 8 for value in corners):
        raise RuntimeError(f"{name} 的背景未完全透明，角点 Alpha={corners}")


def main() -> None:
    parser = argparse.ArgumentParser(description="处理洛秧桌宠的 16 张透明状态图")
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path.home() / "Desktop",
        help="生图软件原图所在目录",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "luoyang_assets",
        help="透明 PNG 输出目录",
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    missing = [spec.source for spec in ASSETS if not (args.source_dir / spec.source).exists()]
    if missing:
        raise FileNotFoundError("缺少源图：" + "、".join(missing))

    with tempfile.TemporaryDirectory(prefix="luoyang-assets-") as temp:
        temp_dir = Path(temp)
        for index, spec in enumerate(ASSETS, start=1):
            source = args.source_dir / spec.source
            if spec.method == "anime":
                image = remove_anime_background(source)
            else:
                image = remove_chroma_background(source, temp_dir)
            image = normalize(image)
            validate(image, spec.output)
            destination = args.output_dir / spec.output
            image.save(destination, format="PNG", optimize=True)
            print(f"[{index:02d}/{len(ASSETS)}] {destination.name}")


if __name__ == "__main__":
    main()
