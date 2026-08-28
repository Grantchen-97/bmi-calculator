@echo off
REM ============================================================
REM  BMI 计算器 —— 一键打包 exe (Windows)
REM  依赖: Python 3.8+ , 已 pip install pywebview pyinstaller
REM ============================================================
cd /d %~dp0

echo [1/3] 检查依赖...
python -c "import webview, PyInstaller" 2>nul
if errorlevel 1 (
    echo 正在安装依赖 pywebview + pyinstaller ...
    pip install pywebview pyinstaller
)

echo [2/3] 使用 PyInstaller 打包 (build_exe.spec)...
pyinstaller build_exe.spec --noconfirm --clean

echo [3/3] 完成。
echo exe 输出在: dist\BMI计算器\BMI计算器.exe
pause
