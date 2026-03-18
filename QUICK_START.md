# 🚀 自动化更新系统 - 5分钟快速启动

## ⚡ 快速概览

你的商业化洞察平台现在可以**每天早上8点自动更新新闻**了！

```
每天早上 8:00
    ↓
自动搜索最新新闻（最近7天）
    ↓
更新网站内容
    ↓
自动部署到 GitHub Pages
```

---

## 📋 完成清单

### ✅ 已完成

- [x] ✅ Python搜索脚本（`scripts/update_news.py`）
- [x] ✅ GitHub Actions工作流（`.github/workflows/daily-update.yml`）
- [x] ✅ 过滤规则（排除招聘、广告联盟等）
- [x] ✅ 7个行业媒体源（36氪、新浪、钛媒体、广告门、新榜等）
- [x] ✅ 完整部署文档（`AUTOMATION_GUIDE.md`）

### 🔲 待完成（需要你操作）

- [ ] 🔑 **获取Google API密钥**（5分钟）
- [ ] ⚙️ **配置GitHub Secrets**（2分钟）
- [ ] 🧪 **手动测试运行**（3分钟）

---

## 🔑 Step 1: 获取Google API密钥（5分钟）

### 1.1 创建Google Cloud项目

1. 访问：https://console.cloud.google.com/
2. 登录你的Google账号
3. 点击顶部"选择项目" → "新建项目"
4. 项目名称：`ad-insight-platform`
5. 点击"创建"

### 1.2 启用Custom Search API

1. 左侧菜单：**APIs & Services** → **Library**
2. 搜索：`Custom Search API`
3. 点击进入 → 点击 **ENABLE**

### 1.3 创建API密钥

1. 左侧菜单：**APIs & Services** → **Credentials**
2. 点击 **+ CREATE CREDENTIALS** → 选择 **API Key**
3. 复制生成的密钥（格式：`AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx`）
4. 点击"限制密钥" → 仅允许"Custom Search API"

### 1.4 创建自定义搜索引擎

1. 访问：https://programmablesearchengine.google.com/
2. 点击 **Add** 创建新搜索引擎
3. 配置：
   - **要搜索的网站**：选择"搜索整个网络"
   - **语言**：简体中文
   - **搜索引擎名称**：`商业化洞察平台`
4. 创建后，点击"控制台" → 复制"搜索引擎ID"（格式：`xxxxxxxxxxxxxx:yyyyyyyyyyy`）

---

## ⚙️ Step 2: 配置GitHub Secrets（2分钟）

1. 打开你的GitHub仓库：
   ```
   https://github.com/ailiuliuliu/ad-insight-platform
   ```

2. 进入：**Settings** → **Secrets and variables** → **Actions**

3. 点击 **New repository secret**，添加2个密钥：

   **密钥1：GOOGLE_API_KEY**
   ```
   Name:  GOOGLE_API_KEY
   Value: [粘贴你的API密钥，如 AIzaSyxxxxxxxxx]
   ```
   点击 **Add secret**

   **密钥2：GOOGLE_CSE_ID**
   ```
   Name:  GOOGLE_CSE_ID
   Value: [粘贴你的搜索引擎ID，如 xxxxxx:yyyyyy]
   ```
   点击 **Add secret**

---

## 🧪 Step 3: 测试运行（3分钟）

### 3.1 上传自动化文件到GitHub

**方法1：浏览器上传（推荐）**

1. 进入仓库：https://github.com/ailiuliuliu/ad-insight-platform

2. 上传文件夹和文件：
   - 点击 **Add file** → **Upload files**
   - 拖拽以下文件/文件夹到上传区：
     ```
     .github/workflows/daily-update.yml
     scripts/update_news.py
     requirements.txt
     ```
   - Commit message：`新增：自动化更新系统`
   - 点击 **Commit changes**

**方法2：命令行上传**

```bash
cd ad-insight-demo
git push origin main
```

### 3.2 启用GitHub Actions

1. 进入仓库的 **Actions** 标签
2. 如果看到提示"Workflows aren't being run..."
3. 点击 **I understand my workflows, go ahead and enable them**

### 3.3 手动触发测试

1. 在 **Actions** 标签，点击左侧的 **每日新闻自动更新**
2. 点击右上角 **Run workflow** 按钮
3. 选择 `main` 分支
4. 点击绿色的 **Run workflow** 按钮

### 3.4 查看运行结果

1. 等待2-3分钟，刷新页面
2. 查看运行状态（应该显示绿色✅）
3. 点击运行记录，查看详细日志
4. 下载 **Artifacts** 中的 `news-update-result`
5. 解压查看 `news_update.json`

---

## ✅ 验证成功

### 检查清单

- [ ] GitHub Actions运行成功（显示绿色✅）
- [ ] 日志中显示"找到 XX 条新闻"
- [ ] `news_update.json` 包含搜索结果
- [ ] 没有"API key invalid"等错误

### 如果成功，你将看到：

```
✅ 字节跳动: 找到 3 条新闻
✅ 小红书: 找到 3 条新闻
✅ 快手: 找到 3 条新闻
✅ 腾讯: 找到 3 条新闻
✅ 阿里: 找到 2 条新闻
✅ 游戏与内容: 找到 2 条新闻
✅ 本地生活: 找到 2 条新闻
✅ 电商广告: 找到 2 条新闻

📈 总计搜索到 20 条新闻
```

---

## 📊 自动化运行时间表

| 时间 | 操作 | 说明 |
|:---|:---|:---|
| **每天早上 8:00** | 自动运行 | GitHub Actions定时触发 |
| 8:00-8:03 | 搜索新闻 | 调用Google API |
| 8:03-8:05 | 更新HTML | 替换新闻内容 |
| 8:05-8:06 | Git提交 | 自动commit + push |
| 8:06-8:07 | 部署 | GitHub Pages自动部署 |
| **8:07** | 完成 | 新网站已上线 |

---

## 🎯 下一步优化

### Phase 1: 完善HTML自动更新（本周）

**当前状态**：
- ✅ 搜索功能完成
- ⚠️ 输出JSON格式（需手动复制到HTML）

**下一步**：
- [ ] 实现自动替换HTML中的新闻
- [ ] 使用BeautifulSoup解析HTML
- [ ] 测试并部署

### Phase 2: 增加官方公众号源（下周）

- [ ] 接入搜狗微信搜索
- [ ] 或使用新榜API
- [ ] 添加11个核心公众号

### Phase 3: AI洞察自动生成（下个月）

- [ ] 接入LLM API
- [ ] 根据最新新闻生成洞察
- [ ] 自动更新"今日洞察"模块

---

## 🆘 遇到问题？

### 常见错误

**❌ "API key invalid"**
- 检查GOOGLE_API_KEY是否正确
- 确认Custom Search API已启用
- 密钥是否有多余空格

**❌ "搜索结果为空"**
- 检查GOOGLE_CSE_ID是否正确
- 确认搜索引擎配置为"搜索整个网络"
- 最近7天可能确实没有相关新闻

**❌ "GitHub Actions运行失败"**
- 查看详细日志定位问题
- 检查文件路径是否正确
- 确认所有依赖已安装

### 获取帮助

1. 查看详细文档：`AUTOMATION_GUIDE.md`
2. 查看GitHub Actions日志
3. 检查 `news_update.json` 输出

---

## 📚 相关文档

- 📖 **完整部署指南**：`AUTOMATION_GUIDE.md`
- 📰 **新闻源规划**：`NEWS_SOURCES_V2.md`
- 🔍 **搜索脚本**：`scripts/update_news.py`
- ⚙️ **工作流配置**：`.github/workflows/daily-update.yml`

---

## 🎉 恭喜！

如果你完成了以上3个步骤，你的商业化洞察平台现在可以：

✅ **每天自动更新**：无需手动操作
✅ **7大媒体源**：36氪、新浪、钛媒体、广告门、新榜等
✅ **智能过滤**：自动排除招聘、广告联盟等无关内容
✅ **完全免费**：使用Google免费API额度（100次/天）

---

**从明天开始，每天早上8点，你的平台都会自动更新最新的商业化资讯！** 🎊

---

**文档版本**：v1.0
**更新时间**：2026-03-18
