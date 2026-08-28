# BMI 健康计算器 · 构建与打包说明

基于你原来的 `bmi.py` 计算逻辑，做了一套**美观界面**，同一套 `index.html` 可同时打包为 **Windows exe** 和 **Android apk**。

## 计算规则（与原程序一致）
- `BMI = 体重(kg) / 身高(m)²`，结果保留 2 位小数
- 分级（中国成人标准）：
  - `< 18.5` → 过轻（蓝）
  - `18.5 ~ 24` → 正常（绿）
  - `24 ~ 28` → 过重（橙）
  - `≥ 28` → 肥胖（红）
- 标准体重 = `24 × 身高²`

## 目录结构
```
bmi-calculator/
├── index.html            # 美观界面（核心，无外部依赖，可直接双击用浏览器打开）
├── bmi_app.py            # 桌面端 pywebview 封装（加载 index.html 成窗口）
├── build_exe.spec        # PyInstaller 打包配置
├── build_exe.bat         # Windows 一键打包 exe 脚本
├── package.json          # Capacitor 依赖（用于 apk）
├── capacitor.config.json # Capacitor 配置（webDir 指向 index.html）
├── .github/workflows/build-android.yml  # 云端一键生成 apk
└── BUILD.md              # 本文档
```

---

## 一、桌面 exe（Windows）

### 方式 A：一键脚本
双击 `build_exe.bat`（需本机已装 Python 3.8+）。脚本会自动安装依赖并打包。

### 方式 B：手动命令
```bat
pip install pywebview pyinstaller
pyinstaller build_exe.spec --noconfirm --clean
```
成品位于：`dist\BMI计算器\BMI计算器.exe`

> 说明：桌面端用 pywebview 调用系统 Edge WebView2 渲染界面，Windows 10/11 自带，无需额外安装浏览器。若目标机器较老（无 WebView2），到微软官网下载 “WebView2 Runtime” 安装即可。

---

## 二、Android apk

APK 编译需要 **Android SDK / 构建工具**（体积大，且官方工具链在 Linux 下最稳），因此**无法在普通 Windows 沙箱里直接产出**。给你两种落地方式：

### 方式 1：GitHub Actions 云端一键构建（推荐，零环境）
1. 把 `bmi-calculator` 整个目录推送到一个 GitHub 仓库（确保含 `.github/workflows/build-android.yml`）。
2. 仓库页面 → **Actions** → 选择 **Build BMI APK** → **Run workflow**。
3. 完成后在 **Artifacts** 下载 `bmi-apk`，得到 `app-debug.apk`，拷到手机安装即可。
4. 也可直接 `git push` 到 `main` 分支自动触发。

### 方式 2：本机 Android Studio 构建
1. 安装 [Node.js 20+](https://nodejs.org/) 与 [Android Studio](https://developer.android.com/studio)（含 SDK）。
2. 在 `bmi-calculator` 目录执行：
   ```bat
   npm install
   npx cap init bmi-calculator com.example.bmicalc --web-dir .
   npx cap add android
   npx cap sync
   npx cap open android      # 用 Android Studio 打开
   ```
3. 在 Android Studio 内 `Build → Build Bundle(s) / APK(s) → Build APK`。

> 如需正式签名上架，用 Android Studio 生成签名密钥后构建 release APK / AAB。

---

## 三、改界面 / 改公式
- 界面与样式全部在 `index.html`（HTML/CSS/JS），想改颜色、文案、增加功能直接改这里，**exe 与 apk 同步生效**。
- 计算逻辑在 `index.html` 的 `calc()` 与 `classify()` 中，已与原 `bmi.py` 保持一致。

## 四、其他平台
- **纯网页**：直接双击 `index.html` 即可在任意浏览器使用，手机浏览器访问同样美观自适应。
- **Linux / macOS 桌面**：`pip install pywebview pyinstaller` 后，`pyinstaller build_exe.spec` 同样可用（macOS 需改 `console`/图标，可另行调整 spec）。
