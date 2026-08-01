@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

python -m pip install -r requirements.txt pyinstaller

pyinstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --name "LuoYang" ^
  --icon "app_icon.ico" ^
  --add-data "luoyang_assets;luoyang_assets" ^
  --add-data "accessories;accessories" ^
  --add-data "naicha_mouse_state_map.json;." ^
  --add-data "naicha_mouse_dialogues.json;." ^
  --add-data "naicha_mouse_gacha_pool.json;." ^
  --add-data "naicha_mouse_accessories.json;." ^
  main.py

if not exist "release" mkdir "release"
copy /Y "dist\LuoYang.exe" "release\洛秧桌宠.exe" >nul

echo.
echo 打包完成：release\洛秧桌宠.exe
if /I not "%~1"=="--no-pause" pause
