# -*- coding: utf-8 -*-
"""
BMI 计算器 —— 桌面端封装
使用 pywebview 将 index.html 包装为原生窗口程序。
打包命令见 build_exe.spec / BUILD.md。
"""
import base64
import os
import sys
import webview


class BmiApi:
    """暴露给前端 JS 的桥：自动把数据备份到本地文件（换电脑可带走）。"""
    def __init__(self, storage_path):
        self.storage_path = storage_path

    def autoBackup(self, data):
        try:
            if not self.storage_path:
                return {"ok": False, "error": "no storage path"}
            path = os.path.join(self.storage_path, "bmi_history.json")
            with open(path, "w", encoding="utf-8") as f:
                f.write(data)
            return {"ok": True, "path": path}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _pick_save_path(self, suggested_name, file_types):
        """弹出系统原生保存对话框，返回用户选择的路径；取消返回 None。"""
        try:
            if not webview.windows:
                return None
            result = webview.windows[0].create_file_dialog(
                webview.SAVE_DIALOG,
                save_filename=suggested_name,
                file_types=file_types,
            )
            if isinstance(result, (list, tuple)):
                result = result[0] if result else None
            return result or None
        except Exception:
            return None

    def saveImage(self, data_url, suggested_name):
        """保存分享图片：前端传 dataURL，经原生对话框落盘。"""
        try:
            _, b64 = data_url.split(",", 1)
            data = base64.b64decode(b64)
        except Exception:
            return {"ok": False, "error": "图片数据解析失败"}
        path = self._pick_save_path(suggested_name, ("PNG 图片 (*.png)", "所有文件 (*.*)"))
        if not path:
            return {"cancelled": True}
        if not path.lower().endswith(".png"):
            path += ".png"
        try:
            with open(path, "wb") as f:
                f.write(data)
            return {"ok": True, "path": path}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def saveFile(self, filename, text):
        """保存 CSV/JSON 导出文件：经原生对话框落盘。"""
        path = self._pick_save_path(filename, ("所有文件 (*.*)",))
        if not path:
            return {"cancelled": True}
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            return {"ok": True, "path": path}
        except Exception as e:
            return {"ok": False, "error": str(e)}


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

    api = BmiApi(storage_path)

    webview.create_window(
        "BMI 健康计算器",
        url=url,
        width=480,
        height=720,
        resizable=True,
        min_size=(360, 600),
        text_select=False,
        confirm_close=False,
        js_api=api,
    )
    webview.start(private_mode=False, storage_path=storage_path)


if __name__ == "__main__":
    main()
