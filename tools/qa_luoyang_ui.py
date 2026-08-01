from __future__ import annotations

import argparse
import os
import sys
import tempfile
import time
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from PIL import Image, ImageChops, ImageDraw
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

import main


def main_test(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication.instance() or QApplication([])
    app.setQuitOnLastWindowClosed(False)

    with tempfile.TemporaryDirectory(prefix="luoyang-ui-qa-") as temp:
        main.PROFILE_PATH = Path(temp) / "profile.json"
        main.AI_CONFIG_PATH = Path(temp) / "ai.json"
        pet = main.NaichaMouse()
        pet.show()
        app.processEvents()

        first_state_by_file: dict[str, str] = {}
        for state in pet.states.values():
            first_state_by_file.setdefault(state.file, state.id)

        snapshots: list[tuple[str, Path]] = []
        for filename in sorted(first_state_by_file):
            state_id = first_state_by_file[filename]
            pet.play_state(state_id)
            pet.motion_started_at = time.monotonic() - 0.65
            pet.update_static_motion()
            app.processEvents()
            path = output_dir / f"{Path(filename).stem}.png"
            if not pet.pet_label.grab().save(str(path), "PNG"):
                raise RuntimeError(f"无法保存界面快照：{path}")
            snapshots.append((Path(filename).stem, path))

        pet.play_state("movement_run")
        pet.motion_started_at = time.monotonic()
        pet.update_static_motion()
        app.processEvents()
        frame_a = output_dir / "motion-a.png"
        pet.pet_label.grab().save(str(frame_a), "PNG")
        pet.motion_started_at = time.monotonic() - 0.175
        pet.update_static_motion()
        app.processEvents()
        frame_b = output_dir / "motion-b.png"
        pet.pet_label.grab().save(str(frame_b), "PNG")

        with Image.open(frame_a) as image_a, Image.open(frame_b) as image_b:
            difference = ImageChops.difference(
                image_a.convert("RGB"), image_b.convert("RGB")
            )
            if difference.getbbox() is None:
                raise RuntimeError("静态 PNG 的程序动画没有产生像素变化")

        sheet = Image.new("RGB", (960, 960), (48, 48, 52))
        draw = ImageDraw.Draw(sheet)
        for index, (label, path) in enumerate(snapshots):
            with Image.open(path).convert("RGBA") as snapshot:
                tile = snapshot.resize((240, 240), Image.Resampling.LANCZOS)
            x = index % 4 * 240
            y = index // 4 * 240
            sheet.paste(tile, (x, y), tile)
            draw.text((x + 6, y + 6), label, fill=(255, 255, 255))
        sheet.save(output_dir / "ui-contact-sheet.png")

        pet.startup_active = False
        pet.exiting = False
        pet.hide_bubble()
        pet.play_state("idle_static_cute")
        pet.update_accessory_label()
        app.processEvents()
        accessory_preview = output_dir / "default-accessory.png"
        if not pet.grab().save(str(accessory_preview), "PNG"):
            raise RuntimeError("无法保存默认配饰快照")

        config_dialog = main.AiConfigDialog(
            {
                "provider": "openai",
                "base_url": "https://api.example.com/v1",
                "model": "example-model",
                "api_key": "test-key",
            }
        )
        config_dialog.show()
        app.processEvents()
        if not config_dialog.grab().save(str(output_dir / "ai-config.png"), "PNG"):
            raise RuntimeError("无法保存 AI 配置窗口快照")
        config_dialog.hide()

        chat_dialog = main.AiChatDialog()
        chat_dialog.append_line("洛秧", "嗯，我在这里。")
        chat_dialog.append_line("你", "今天一起完成任务吧。")
        chat_dialog.show()
        app.processEvents()
        if not chat_dialog.grab().save(str(output_dir / "ai-chat.png"), "PNG"):
            raise RuntimeError("无法保存 AI 聊天窗口快照")
        chat_dialog.hide()

        pet.hide()
        print(f"已渲染 {len(snapshots)} 个素材状态，动画像素校验通过")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="离屏检查洛秧 PNG 状态与程序动画")
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    main_test(args.output_dir)
