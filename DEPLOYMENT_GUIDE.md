# 部署指南 (GitHub Actions)

由于检测到你的电脑可能未配置 `git` 命令行工具，推荐使用 **GitHub 网页版** 直接上传代码。

## 第一步：创建 GitHub 仓库
1. 登录 [GitHub](https://github.com/)。
2. 点击右上角的 **+** 号，选择 **New repository**。
3. 填写仓库名称（例如 `gold-monitor`）。
4. **Visibility** 选 Public 或 Private 均可。
5. 点击 **Create repository**。

## 第二步：上传文件
1. 在新仓库页面，找到 **"uploading an existing file"** 链接（或者点击 Add file > Upload files）。
2. 将你本地 `Desktop/Agent` 文件夹中的以下文件拖入网页：
    - `main.py`
    - `config.py`
    - `requirements.txt`
    - `services/` (文件夹内的所有文件)
    - `.github/workflows/monitor.yml` (**重要**：必须保持 `.github/workflows/` 的目录结构。如果网页版不支持拖拽文件夹，你可能需要手动在网页上创建路径 `github/workflows/monitor.yml`，或者先上传其他文件，然后点击 "Add file" > "Create new file"，输入路径 `.github/workflows/monitor.yml` 并粘贴内容)
3. 点击 **Commit changes**。

> **提示**：如果在网页上传 `.github` 文件夹有困难，可以先创建一个任意文件，然后使用 "Add file" -> "Create new file"，文件名填写 `.github/workflows/monitor.yml`，然后把本地对应文件的内容复制进去。

## 第三步：配置密钥 (Secrets)
为了安全链接 Telegram，需要设置密钥，不要直接写在代码里。

1. 在仓库页面，点击上方的 **Settings** (设置)。
2. 在左侧菜单栏，点击 **Secrets and variables** > **Actions**。
3. 在 **Repository secrets** 区域，点击 **New repository secret**。
4. 添加以下两个密钥：
    - Name: `TG_BOT_TOKEN`, Secret: (填入你的 Bot Token)
    - Name: `TG_CHAT_ID`, Secret: (填入你的 Chat ID)

## 第四步：测试运行
1. 点击仓库上方的 **Actions** 标签。
2. 你应该能看到左侧有一个 "Gold Price Monitor" 的工作流。
3. 点击它，然后点击右侧的 **Run workflow** 按钮 (因为我们在代码里加了 `workflow_dispatch`，所以可以手动触发)。
4. 刷新页面，等待运行完成。
5. 点击运行记录查看 **Logs**。
    - 如果一切正常，你应该能看到 "Current Gold Price..." 的日志。
    - 如果你想强制测试报警，可以在 Settings > Secrets and variables > Actions > **Variables** (注意是 Variables 不是 Secrets) 中添加：
        - Name: `SELL_PRICE`
        - Value: `0`
    - 再次运行，因为当前金价肯定大于 0，你应该会收到 "黄金止盈提醒"。

## 常见问题
- **Folder Upload**: 网页版上传文件夹如果不方便，最关键的是 `.github/workflows/monitor.yml` 这个文件必须在正确的路径下（`.github/workflows/` 目录中），否则 Actions 不会启动。
