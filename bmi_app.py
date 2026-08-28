# -*- coding: utf-8 -*-
"""
BMI 计算器 —— 桌面端封装
使用 pywebview 将 index.html 包装为原生窗口程序。
打包命令见 build_exe.spec / BUILD.md。
"""
import os
import sys
import webview

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE_DIR, "index.html")


def main():
    # 开发态用 file:// 直接加载本地 HTML；打包后用临时文件或资源目录加载
    if getattr(sys, "frozen", False):
        # PyInstaller 单目录/单文件模式：资源会被解包到 sys._MEIPASS
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        html_file = os.path.join(base, "index.html")
    else:
        html_file = HTML_PATH

    url = "file:///" + html_file.replace("\\", "/")

    # 关键：把 WebView2 用户数据目录固定到 AppData 下的固定路径。
    # 否则 pywebview 默认 private_mode=True 会用临时目录，单文件 exe 每次启动都换新目录，
    # 导致 localStorage（BMI 历史记录）丢失。固定后历史记录永久保存。
    appdata = os.environ.get("APPDATA") or os.path.expanduser("~")
    storage_path = os.path.join(appdata, "BMI Calculator")
    os.makedirs(storage_path, exist_ok=True)

    webview.create_window(
        "BMI 健康计算器",
        url=url,
        width=480,
        height=720,
        resizable=True,
        min_size=(360, 600),
        text_select=False,
        confirm_close=False,
    )
    webview.start(private_mode=False, storage_path=storage_path)


if __name__ == "__main__":
    main()
