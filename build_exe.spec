# -*- mode: python ; coding: utf-8 -*-
# BMI 计算器 exe 打包配置
# 用法: pyinstaller build_exe.spec
import os

block_cipher = None

# SPECPATH 已是 spec 所在目录，无需再取 dirname
BASE_DIR = SPECPATH
html_file = os.path.join(BASE_DIR, "index.html")

a = Analysis(
    [os.path.join(BASE_DIR, "bmi_app.py")],
    pathex=[BASE_DIR],
    binaries=[],
    datas=[(html_file, ".")],
    hiddenimports=["webview", "webview.platforms.cef", "webview.platforms.edgechromium"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="BMI计算器",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # 不显示黑色命令行窗口
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,              # 如需图标，放 bmi.ico 并改为 "bmi.ico"
)
