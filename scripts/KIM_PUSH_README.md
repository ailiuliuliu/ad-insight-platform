# KIM推送定时任务配置指南

## 📋 功能说明

`kim_push.py` 脚本会自动：
1. 从 `index.html` 提取最新的3条核心洞察
2. 构造Markdown格式的周报消息
3. 推送到KIM群聊

## 🚀 快速开始

### 1. 安装依赖

```bash
cd ad-insight-demo/scripts
pip3 install beautifulsoup4 requests
```

### 2. 测试推送

```bash
cd ad-insight-demo/scripts
python3 kim_push.py
```

成功后会看到：
```
✅ 消息发送成功
✅ KIM推送任务执行成功
```

## ⏰ 配置定时任务（每周一10点推送）

### 方案A：macOS/Linux 使用 cron

#### 1. 编辑crontab

```bash
crontab -e
```

#### 2. 添加以下行

```bash
# 每周一早上10点推送KIM商业化洞察
0 10 * * 1 cd /Users/litianyu6/Documents/超级小李/ad-insight-demo/scripts && /usr/bin/python3 kim_push.py >> kim_push_cron.log 2>&1
```

**说明：**
- `0 10 * * 1`：每周一 10:00
- `cd ...`：切换到脚本目录
- `/usr/bin/python3`：使用系统Python3（用 `which python3` 查看路径）
- `>> kim_push_cron.log 2>&1`：输出日志到文件

#### 3. 保存并验证

```bash
# 查看已配置的定时任务
crontab -l

# 测试cron语法
# 先改成每分钟运行测试：
# * * * * * cd ... && python3 kim_push.py
# 验证成功后再改回每周一10点
```

### 方案B：macOS 使用 launchd（更推荐）

#### 1. 创建plist文件

```bash
nano ~/Library/LaunchAgents/com.kuaishou.kim.push.plist
```

#### 2. 粘贴以下内容

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.kuaishou.kim.push</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/litianyu6/Documents/超级小李/ad-insight-demo/scripts/kim_push.py</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>/Users/litianyu6/Documents/超级小李/ad-insight-demo/scripts</string>
    
    <key>StandardOutPath</key>
    <string>/Users/litianyu6/Documents/超级小李/ad-insight-demo/scripts/kim_push_launchd.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/litianyu6/Documents/超级小李/ad-insight-demo/scripts/kim_push_launchd_error.log</string>
    
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>10</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
```

#### 3. 加载任务

```bash
# 加载定时任务
launchctl load ~/Library/LaunchAgents/com.kuaishou.kim.push.plist

# 查看任务状态
launchctl list | grep kim.push

# 立即测试运行
launchctl start com.kuaishou.kim.push

# 如需卸载
# launchctl unload ~/Library/LaunchAgents/com.kuaishou.kim.push.plist
```

### 方案C：GitHub Actions（云端执行）

如果希望完全自动化（即使电脑关机也能推送），可以使用GitHub Actions：

#### 1. 创建 `.github/workflows/kim-push.yml`

```yaml
name: KIM Weekly Push

on:
  schedule:
    # 每周一北京时间10:00（UTC+8）= 周一 02:00 UTC
    - cron: '0 2 * * 1'
  workflow_dispatch:  # 支持手动触发

jobs:
  push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      
      - name: Install dependencies
        run: |
          pip install beautifulsoup4 requests
      
      - name: Push to KIM
        run: |
          cd ad-insight-demo/scripts
          python3 kim_push.py
```

#### 2. 提交到GitHub

```bash
git add .github/workflows/kim-push.yml
git commit -m "feat: 添加KIM周报自动推送"
git push
```

## 📝 日志查看

### cron日志
```bash
cat ad-insight-demo/scripts/kim_push_cron.log
```

### launchd日志
```bash
cat ad-insight-demo/scripts/kim_push_launchd.log
cat ad-insight-demo/scripts/kim_push_launchd_error.log
```

### 脚本自带日志
```bash
cat ad-insight-demo/scripts/kim_push.log
```

## 🔧 故障排查

### 1. 消息没有推送

**检查1**：测试手动运行
```bash
cd ad-insight-demo/scripts
python3 kim_push.py
```

**检查2**：查看日志
```bash
tail -20 kim_push.log
```

**检查3**：验证webhook key
- 确认key没有过期
- 确认机器人还在群聊中

### 2. cron没有执行

**检查1**：cron服务是否运行
```bash
# macOS
sudo launchctl list | grep cron

# Linux
systemctl status cron
```

**检查2**：Python路径是否正确
```bash
which python3
# 将输出路径替换到crontab中
```

**检查3**：绝对路径
cron中必须使用绝对路径，不能使用 `~` 或相对路径

### 3. 权限问题

```bash
# 确保脚本可执行
chmod +x ad-insight-demo/scripts/kim_push.py

# 确保日志文件可写
touch ad-insight-demo/scripts/kim_push.log
chmod 644 ad-insight-demo/scripts/kim_push.log
```

## ⚙️ 高级配置

### 修改推送时间

**改为每周五下午3点：**

cron: `0 15 * * 5`

launchd: `Weekday=5, Hour=15, Minute=0`

GitHub Actions: `cron: '0 7 * * 5'` (UTC+8 = 15:00)

### 修改推送内容

编辑 `kim_push.py` 中的 `build_markdown_message()` 函数。

### 添加@提醒

在Markdown内容中添加：
```python
markdown += f"\n\n@所有人 请查看本周商业化洞察"
```

## 📞 联系支持

如有问题，请联系：
- KIM服务端团队
- 或查看KIM开放能力文档

---

**推荐使用 launchd（方案B）**，macOS原生支持，更稳定！
