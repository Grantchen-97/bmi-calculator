# 在 GitHub 上云端打包 BMI APK —— 手把手操作指南

目标：把你本地的 `bmi-calculator` 目录推到 GitHub，让 GitHub 的免费服务器自动把 `index.html` 编译成 `app-debug.apk`，下载到手机安装即可。
**你不需要本机装 Android Studio / SDK，也不用会安卓开发。**

---

## 一、准备工作

1. 注册 GitHub 账号：https://github.com/ （已有可跳过）。
2. 本机装 Git（用来把文件推到 GitHub）：
   - 下载：https://git-scm.com/download/win ，一路默认安装。
   - 验证：右键任意文件夹 → “Git Bash Here”，输入 `git --version` 能看到版本号即成功。

> 本操作全程免费。建议把仓库设为 **Public**（公开），GitHub 对公开仓库的 Actions 构建不限时长；Private 仓库每月也有免费额度，足够用。

---

## 二、在 GitHub 上新建仓库（网页端）

1. 登录 github.com，右上角 “+” → **New repository**。
2. 填写：
   - **Repository name**：`bmi-calculator`（随便起，英文即可）
   - **Description**（可选）：BMI 健康计算器
   - 选择 **Public**
   - ⚠️ **不要**勾选 “Add a README file”、“Add .gitignore”、“Choose a license” —— 因为我们本地已有完整文件，勾了反而要额外合并。
3. 点击 **Create repository**。
4. 创建后会进入一个空仓库页面，先放着，下面回到本机操作。

---

## 三、把本地文件推上去（推荐：Git 命令行）

> 为什么推荐命令行：项目里有一个隐藏目录 `.github/workflows/`，里面是构建脚本。**网页拖拽上传会漏掉隐藏文件夹**，导致工作流不生效。命令行能完整上传。

1. 打开 **Git Bash**（在 `bmi-calculator` 文件夹里右键 → Git Bash Here）。
2. 依次粘贴执行以下命令（把 `你的用户名` 和 `bmi-calculator` 换成你自己的）：

```bash
# 1) 初始化本地仓库
git init

# 2) 把所有文件加入暂存（.gitignore 已排除 dist/ build/ 等构建产物）
git add .

# 3) 提交
git commit -m "BMI calculator source"

# 4) 主干命名为 main
git branch -M main

# 5) 关联远程仓库（替换成你刚建的仓库地址）
git remote add origin https://github.com/你的用户名/bmi-calculator.git

# 6) 推送到 GitHub
git push -u origin main
```

3. 第一次 `git push` 会弹出 GitHub 登录框（或让你输入用户名 + 密码/**Personal Access Token**）。
   - 如果用 **Token 登录**：去 https://github.com/settings/tokens 生成一个 token（勾 `repo` 权限），密码处粘贴这个 token。
   - 登录成功后，命令行显示 `main -> main` 即推送成功。

4. 回到 github.com 仓库页面，刷新一下，应该能看到 `index.html`、`bmi_app.py`、`.github/` 等文件都在了。

### （备选）方式二：网页直接上传（适合不想装 Git）
1. 在空仓库页面点 **“uploading an existing file”** 链接。
2. 把 `bmi-calculator` 里的文件（除了 `dist/`、`build/` 两个文件夹）拖进去。
3. **必须手动补建隐藏目录**：网页拖拽不会上传 `.github`。请在仓库里点 **Add file → Create new file**，路径填
   `.github/workflows/build-android.yml`，内容复制本仓库同路径文件的内容，提交。
4. 滚动到页面底部 **Commit changes** 提交。

---

## 四、运行构建工作流（生成 APK）

推送成功后，GitHub 会自动开始构建（因为工作流监听 `push` 到 `main`）。你也可以手动触发：

1. 进入你的仓库页面，点上方 **Actions** 选项卡。
2. 左侧列表里会看到 **Build BMI APK**，点进去。
3. 若没自动跑：点右侧 **Run workflow** 按钮 → 再点绿色的 **Run workflow** 确认。
4. 页面会出现一个黄色的构建任务，点进去看实时日志。⏱ 整个过程约 **3~6 分钟**（首次要下载 Android 构建工具，稍慢）。

---

## 五、下载 APK

1. 等构建变成 ✅ 绿色（All jobs completed successfully）。
2. 在构建任务页面最下方找到 **Artifacts** 区域，点击 **bmi-apk** 下载。
   - 下载得到一个 zip，解压后是 `app-debug.apk`。
3. 把 `app-debug.apk` 传到手机（微信文件传输/数据线/网盘均可），在手机上点击安装。
   - 安装时若提示“允许安装未知来源应用”，按提示授权即可（这是调试版 APK 的正常提示）。

---

## 六、之后怎么更新界面 / 重新出包

- 改了 `index.html`（界面、文案、公式）→ 重新推一次：
  ```bash
  git add .
  git commit -m "更新界面"
  git push
  ```
  推送后 Actions 会自动重新构建，去下载新的 `app-debug.apk` 即可。
- 想换应用名 / 包名：改 `capacitor.config.json` 里的 `appName` / `appId` 再推送。

---

## 七、常见问题

| 现象 | 原因 / 解决 |
|------|-------------|
| Actions 里看不到 “Build BMI APK” | 仓库里没有 `.github/workflows/build-android.yml`（多半是网页上传漏了隐藏目录），按“方式二第3步”补建 |
| 构建红叉失败 | 点进任务看红色日志；多半是网络拉取依赖超时，点 **Re-run jobs** 重试一次 |
| 手机安装提示“已损坏/无法安装” | 确认手机系统版本 ≥ 7.0（Android 7+）；调试版 APK 需允许“未知来源” |
| 想上架应用商店 | 调试版 `app-debug.apk` 不能上架，需要用 Android Studio 生成签名后的 release 包（见 BUILD.md） |
