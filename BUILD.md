# BMI 健康计算器 · 构建与打包说明

基于你原来的 `bmi.py` 计算逻辑，做了一套**美观界面**，同一套 `index.html` 可同时打包为 **Windows exe** 和 **Android apk**。

## 功能特性
- **双界面**：计算器 / 历史记录（顶部标签页切换）
- **BMI 计算**：`BMI = 体重(kg) / 身高(m)²`，中国标准分级（过轻/正常/过重/肥胖）
- **标准体重区间**：显示 18.5~24×身高² 的健康区间，及“距标准上限差多少斤”
- **体脂率估算**：用 Deurenberg 公式（BMI + 年龄 + 性别）估算
- **WHO / 中国标准对照**：一键切换两种评级标准
- **多档案**：支持家人各自独立记录（顶部下拉切换、可增删）
- **历史图表**：纯 Canvas 双线图（BMI + 体重），标注 18.5/24/28 参考线
- **目标 BMI 追踪**：进度条显示朝目标靠拢的完成度与预计差值
- **周期统计**：按周 / 月 / 年聚合，显示平均、最高、最低
- **数据持久化**：
  - Web/APK 端用浏览器 localStorage（跨会话保留）
  - exe 端固定 WebView2 用户数据目录到 `%APPDATA%\BMI Calculator`，重启不丢
  - exe 端自动镜像 `bmi_history.json` 到上述目录（换电脑可带走）
- **数据备份**：历史可导出 CSV / JSON，也支持从 JSON 导入合并
- **每日提醒**（轻量版）：设置时间后，页面打开或每分钟检查，到点弹通知/提示
- **分享图**：把 BMI 结果卡片生成 PNG 图片下载保存/分享
- **明暗主题**：右上角一键切换

## 计算规则（与原程序一致）
- `BMI = 体重(kg) / 身高(m)²`，结果保留 2 位小数
- 分级（中国成人标准）：`<18.5` 过轻｜`18.5~24` 正常｜`24~28` 过重｜`≥28` 肥胖
- 标准体重区间 = `18.5×身高² ~ 24×身高²`

## 目录结构
```
bmi-calculator/
├── index.html                      # 核心界面（无外部依赖，可双击用浏览器打开）
├── bmi_app.py                      # 桌面端 pywebview 封装（含 JSON 自动备份桥）
├── build_exe.spec                  # PyInstaller 打包配置
├── build_exe.bat                   # Windows 一键打包 exe 脚本
├── package.json                    # Capacitor 依赖（用于 apk）
├── capacitor.config.json           # Capacitor 配置（webDir 指向 www，由 CI 动态生成）
├── .github/workflows/build-android.yml  # 云端一键生成 apk（支持签名 release）
├── GITHUB_APK.md                   # GitHub 云端出包详细图文指南
└── BUILD.md                        # 本文档
```
> `www/` 与 `android/` 为构建时动态生成，已被 `.gitignore` 忽略，不会进仓库。

---

## 一、桌面 exe（Windows）

### 方式 A：一键脚本
双击 `build_exe.bat`（需本机已装 Python 3.8+）。脚本会自动安装依赖并打包。

### 方式 B：手动命令
```bat
pip install pywebview pyinstaller
pyinstaller build_exe.spec --noconfirm --clean
```
成品位于：`dist\BMI计算器.exe`

> 桌面端用 pywebview 调用系统 Edge WebView2 渲染界面，Windows 10/11 自带，无需额外安装浏览器。
> **记录持久化**：`bmi_app.py` 把 WebView2 用户数据目录固定到 `%APPDATA%\BMI Calculator`，所以 BMI 历史记录重启不丢；同时自动把整个状态写入该目录下的 `bmi_history.json`。

---

## 二、Android apk

APK 编译需要 Android SDK（体积大，Linux 下最稳），**无法直接在本机 Windows 沙箱产出**。推荐用 GitHub Actions 云端构建。

### 方式 1：GitHub Actions 云端一键构建（推荐，零环境）
1. 把 `bmi-calculator` 整个目录推送到一个 GitHub 仓库（确保含 `.github/workflows/build-android.yml`）。
2. 仓库页面 → **Actions** → 选择 **Build BMI APK** → **Run workflow**；或 `git push` 到 `main`/`main1` 自动触发。
3. 完成后在 **Artifacts** 下载 `bmi-apk`，得到 `app-debug.apk`（或签名后的 `app-release.apk`），拷到手机安装即可。

CI 会自动：`npm install` → 动态生成 `www/`（复制 index.html）→ `cap add android` + `cap sync` → 构建 APK。

### 方式 2：本机 Android Studio 构建
```bat
npm install
npx cap init bmi-calculator com.example.bmicalc --web-dir .
npx cap add android
npx cap sync
npx cap open android      # 用 Android Studio 打开
```
在 Android Studio 内 `Build → Build Bundle(s) / APK(s) → Build APK`。

### 正式签名 release 版（可选）
默认产出 debug 包。若要**已签名的 release 包**，在 GitHub 仓库
`Settings → Secrets and variables → Actions` 添加 4 个 secret：
- `KEYSTORE_BASE64`：你的 `release-key.jks` 经 `base64` 编码后的内容（`base64 -w0 release-key.jks`）
- `KEY_ALIAS`：key 别名
- `KEY_PASSWORD`：key 密码
- `KEYSTORE_PASSWORD`：keystore 密码

配置后重新运行工作流，将自动注入签名并产出 `app-release.apk`。（生成 keystore：`keytool -genkeypair -v -keystore release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias bmi`）

---

## 三、改界面 / 改公式
- 界面与样式全部在 `index.html`（HTML/CSS/JS），改颜色、文案、加功能直接改这里，**exe 与 apk 同步生效**。
- 计算逻辑在 `index.html` 的 `calc()`、`classify()`、`estimateFat()` 中。
- exe 端若改动存储路径/桥，改 `bmi_app.py` 后重新打包。

## 四、其他平台
- **纯网页**：双击 `index.html` 即可在任意浏览器使用，手机浏览器同样自适应。
- **Linux / macOS 桌面**：`pip install pywebview pyinstaller` 后 `pyinstaller build_exe.spec` 同样可用（macOS 需调整 spec 的 console/图标）。
