# 🤖 自动化更新系统部署指南

## 📋 目录

1. [系统架构](#系统架构)
2. [配置步骤](#配置步骤)
3. [测试验证](#测试验证)
4. [监控维护](#监控维护)

---

## 🏗️ 系统架构

### 组件说明

```
┌─────────────────────────────────────────┐
│  GitHub Actions (定时任务)              │
│  - 每天早上8:00自动运行                  │
│  - 或手动触发                            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Python脚本 (update_news.py)            │
│  - Google搜索API调用                     │
│  - 新闻源多层级搜索                      │
│  - 过滤规则（排除招聘等）                │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  更新index.html                          │
│  - 核心竞对动态（12条）                  │
│  - 行业赛道新闻（6条）                   │
│  - 生成洞察判断（3条）                   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  自动提交到GitHub                        │
│  - Git commit + push                    │
│  - GitHub Pages自动部署                 │
└─────────────────────────────────────────┘
```

---

## ⚙️ 配置步骤

### Step 1: 获取Google API密钥

#### 1.1 创建Google Cloud项目

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 点击"创建项目"或选择现有项目
3. 记录项目ID

#### 1.2 启用Custom Search API

1. 在左侧菜单选择 **APIs & Services** > **Library**
2. 搜索 **Custom Search API**
3. 点击 **Enable**

#### 1.3 创建API密钥

1. 在左侧菜单选择 **APIs & Services** > **Credentials**
2. 点击 **Create Credentials** > **API Key**
3. 复制生成的API密钥
4. （可选）限制密钥用途：只允许Custom Search API

#### 1.4 创建Custom Search Engine

1. 访问 [Programmable Search Engine](https://programmablesearchengine.google.com/)
2. 点击 **Add** 创建新的搜索引擎
3. **配置**：
   - **搜索内容**：整个网络
   - **名称**：商业化洞察平台搜索
4. 创建后，进入 **设置** > **基本信息**
5. 复制 **搜索引擎ID**（CX值）

---

### Step 2: 配置GitHub Secrets

1. 打开你的GitHub仓库：https://github.com/ailiuliuliu/ad-insight-platform

2. 进入 **Settings** > **Secrets and variables** > **Actions**

3. 点击 **New repository secret**，添加以下密钥：

   **Secret 1: GOOGLE_API_KEY**
   ```
   名称: GOOGLE_API_KEY
   值: [粘贴你的Google API密钥]
   ```

   **Secret 2: GOOGLE_CSE_ID**
   ```
   名称: GOOGLE_CSE_ID
   值: [粘贴你的搜索引擎ID]
   ```

---

### Step 3: 上传自动化文件到GitHub

#### 方法1：浏览器上传（推荐）

1. **上传Python脚本**：
   - 进入仓库，点击 **Add file** > **Upload files**
   - 创建目录结构：`scripts/`
   - 上传 `update_news.py`
   - Commit message: `新增：自动更新脚本`

2. **上传GitHub Actions配置**：
   - 创建目录结构：`.github/workflows/`
   - 上传 `daily-update.yml`
   - Commit message: `新增：每日自动更新工作流`

#### 方法2：命令行上传

```bash
cd ad-insight-demo
git add scripts/update_news.py
git add .github/workflows/daily-update.yml
git commit -m "新增：自动化更新系统"
git push origin main
```

---

### Step 4: 启用GitHub Actions

1. 进入仓库的 **Actions** 标签
2. 如果看到"Workflows aren't being run on this repository"提示
3. 点击 **I understand my workflows, go ahead and enable them**

---

## 🧪 测试验证

### 手动触发测试

1. 进入仓库的 **Actions** 标签
2. 点击左侧的 **每日新闻自动更新** 工作流
3. 点击右上角的 **Run workflow** > **Run workflow**
4. 等待运行完成（约3-5分钟）

### 查看运行结果

1. 点击运行记录查看详细日志
2. 检查各步骤是否成功：
   - ✅ 📦 Checkout代码
   - ✅ 🐍 设置Python环境
   - ✅ 📚 安装依赖
   - ✅ 🔍 执行新闻搜索
   - ✅ 📝 提交更新

3. 下载 **Artifacts** 中的 `news-update-result` 查看搜索结果

### 验证网站更新

1. 等待GitHub Pages部署完成（约30-60秒）
2. 访问 https://ailiuliuliu.github.io/ad-insight-platform/
3. 检查新闻是否已更新
4. 查看更新时间戳

---

## 📊 监控维护

### 每日检查清单

**自动检查**（GitHub Actions）：
- ✅ 工作流是否正常运行
- ✅ 是否有错误日志
- ✅ 新闻数量是否正常（≥12条）

**手动检查**（每周1次）：
- ✅ 新闻质量是否符合预期
- ✅ 是否有无效链接
- ✅ 洞察判断是否准确

### 查看运行历史

1. 进入 **Actions** 标签
2. 查看历史运行记录
3. 检查成功率和失败原因

### API配额监控

**Google Custom Search API**：
- 免费额度：100次/天
- 当前消耗：约10-15次/天
- 查看用量：[Google Cloud Console](https://console.cloud.google.com/) > APIs & Services > Dashboard

---

## 🔧 常见问题

### Q1: 工作流运行失败，显示"API key invalid"

**原因**：GitHub Secrets配置错误

**解决**：
1. 检查 GOOGLE_API_KEY 是否正确
2. 确认API密钥已启用Custom Search API
3. 重新创建Secret（注意不要有多余空格）

---

### Q2: 搜索结果为空或很少

**原因**：
- 搜索关键词不匹配
- 新闻源最近7天没有相关新闻
- API配额用完

**解决**：
1. 查看 `news_update.json` 的详细输出
2. 调整搜索关键词（修改 `update_news.py`）
3. 检查Google API配额

---

### Q3: HTML没有更新

**原因**：
- Python脚本只输出JSON，未更新HTML
- Git提交失败

**解决**：
1. 当前版本暂时只输出JSON用于验证
2. 需要完善HTML更新逻辑（见下方TODO）
3. 检查Git提交权限

---

## 🚀 下一步优化

### Phase 1: 完善HTML更新逻辑（当前）

**TODO**：
- [ ] 实现自动替换HTML中的新闻内容
- [ ] 使用BeautifulSoup解析和修改HTML
- [ ] 保留原有的样式和结构

**代码位置**：`update_news.py` 中的 `update_html_file()` 函数

---

### Phase 2: 增加Tier 2官方公众号（下周）

**TODO**：
- [ ] 接入搜狗微信搜索API
- [ ] 或使用新榜API
- [ ] 添加公众号文章到新闻源

---

### Phase 3: 增加AI洞察生成（下个月）

**TODO**：
- [ ] 接入OpenAI API或其他LLM
- [ ] 根据最新新闻生成3条洞察判断
- [ ] 自动更新"今日洞察"模块

---

## 📚 文件清单

```
ad-insight-demo/
├── scripts/
│   └── update_news.py          # 新闻搜索脚本
├── .github/
│   └── workflows/
│       └── daily-update.yml    # GitHub Actions配置
├── index.html                  # 主页面（会被自动更新）
├── news_update.json            # 搜索结果（自动生成）
└── AUTOMATION_GUIDE.md         # 本文档
```

---

## 🎯 成功标准

### 自动化系统运行良好的标志：

✅ **每天准时运行**：早上8:00自动触发
✅ **新闻质量高**：来自权威媒体，相关性强
✅ **无需人工干预**：全自动搜索、更新、部署
✅ **错误率低**：API调用成功率 >95%
✅ **成本可控**：免费API额度够用

---

## 📞 支持

如有问题，请检查：
1. GitHub Actions运行日志
2. `news_update.json` 输出结果
3. Google Cloud Console API用量

---

**文档版本**：v1.0
**更新时间**：2026-03-18
**维护者**：AI Assistant
