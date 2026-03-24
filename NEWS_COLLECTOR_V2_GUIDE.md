# 新闻采集系统 v2.0 使用指南

## 🎯 核心升级

### v1.0 → v2.0 重大变化

**v1.0问题：**
- ❌ 单一Google搜索，信息源不够丰富
- ❌ 缺乏时效性筛选，旧新闻混杂
- ❌ 没有价值评分，质量参差不齐

**v2.0解决方案：**
- ✅ **多源采集**：Google搜索 + 行业媒体官网
- ✅ **智能筛选**：时效性 + 相关性 + 权威性三维评分
- ✅ **自动排序**：按价值分数自动排序，取Top N

---

## 📊 评分机制

### 三维评分体系（总分100）

#### 1. 时效性（40分）
- 今天：40分
- 3天内：35分
- 7天内：30分
- 14天内：20分
- 30天内：10分
- 超过30天：0分

#### 2. 相关性（40分）
基于关键词权重匹配：

**核心业务（高权重×3）：**
- 快手、抖音、字节、腾讯、小红书
- 磁力引擎、巨量引擎、视频号

**业务方向（中权重×2）：**
- 广告、商业化、营销、电商
- AI、AIGC、短剧、漫剧
- 直播、本地生活

**行业术语（低权重×1）：**
- ROI、GMV、投放、效果
- 种草、流量、转化

#### 3. 权威性（20分）
- 官方/头部媒体（新华网、QQ News）：20分
- 行业媒体（36氪、虎嗅、Morketing）：15分
- 其他媒体：10分

---

## 💻 使用方式

### 方式1：Python脚本

```python
from news_collector_v2 import NewsCollector

# 初始化采集器
collector = NewsCollector()

# 准备新闻数据（来自Google搜索）
google_results = [
    {
        'title': '新闻标题',
        'source': '来源',
        'url': 'URL',
        'content': '正文',
        'date': '2026-03-24'
    }
]

# 执行采集+筛选
top_news = collector.collect_and_filter(
    google_results=google_results,
    min_score=50.0,  # 最低50分
    top_n=10         # 取前10条
)

# 输出结果
for news in top_news:
    print(f"[{news['_score']:.1f}分] {news['title']}")
```

---

### 方式2：命令行测试

```bash
cd ad-insight-demo/scripts
python3 news_collector_v2.py
```

---

## 🔄 集成到更新流程

### 完整流程

```
1. Google搜索（广度）
   ↓
2. 行业媒体抓取（深度）- TODO
   ↓
3. 合并所有来源
   ↓
4. 去重（标题相似度）
   ↓
5. 计算价值分数
   ↓
6. 筛选（min_score阈值）
   ↓
7. 排序（按分数）
   ↓
8. 取Top N
   ↓
9. 传入记忆系统
   ↓
10. 生成洞察
```

---

## 📁 文件说明

### news_collector_v2.py
**功能：** 新闻采集+筛选核心模块

**主要类：**
- `NewsCollector`: 采集器主类

**主要方法：**
- `collect_from_google()`: Google搜索采集
- `collect_from_media_sites()`: 媒体官网采集（待实现）
- `calculate_news_score()`: 计算价值分数
- `filter_and_rank()`: 筛选+排序
- `deduplicate()`: 去重
- `collect_and_filter()`: 完整流程

---

## 🧪 测试示例

### 示例1：基础筛选

```python
collector = NewsCollector()

news_list = [
    {'title': '腾讯财报', 'date': '2026-03-18', 'source': 'QQ News', 'content': '腾讯营销'},
    {'title': '小红书治理', 'date': '2026-03-13', 'source': 'CBNData', 'content': '小红书AI'},
    {'title': '旧新闻', 'date': '2025-03-27', 'source': '新浪', 'content': '快手'}
]

top_news = collector.collect_and_filter(
    google_results=news_list,
    min_score=40.0,
    top_n=5
)

# 结果：2条（旧新闻被过滤）
# [1] 腾讯财报 - 55分
# [2] 小红书治理 - 40分
```

---

### 示例2：调整阈值

```python
# 严格筛选（只要60分以上）
top_news = collector.collect_and_filter(
    google_results=news_list,
    min_score=60.0,  # 更高的阈值
    top_n=10
)

# 宽松筛选（40分以上即可）
top_news = collector.collect_and_filter(
    google_results=news_list,
    min_score=40.0,  # 更低的阈值
    top_n=10
)
```

---

## 🔧 参数配置

### 关键参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `min_score` | 50.0 | 最低分数阈值 |
| `max_days` | 30 | 最大天数（超过会被过滤） |
| `top_n` | 10 | 返回前N条 |

### 推荐配置

**日常更新：**
```python
min_score=50.0  # 中等质量
max_days=7      # 最近一周
top_n=10        # 前10条
```

**紧急更新：**
```python
min_score=40.0  # 降低门槛
max_days=3      # 最近3天
top_n=5         # 前5条
```

**深度研究：**
```python
min_score=60.0  # 高质量
max_days=30     # 最近一月
top_n=20        # 前20条
```

---

## 📈 输出示例

### 控制台输出

```
============================================================
商业化新闻采集系统 v2.0 - 多源采集+智能筛选
============================================================
📊 Google来源: 3条
📊 总计: 3条原始新闻
🔄 开始去重...
✅ 去重完成: 3条 → 3条
🔍 开始筛选和排序...
✅ 筛选完成: 3条 → 2条 → Top 2条
============================================================
✅ 最终输出: 2条高价值新闻
============================================================

[1] 腾讯2025年财报：营销服务全年收入达1450亿增19%...
    评分: 55.0 (时效30 + 相关5 + 权威20)
    来源: QQ News | 日期: 2026-03-18
    关键词: 腾讯, 营销

[2] 小红书打击AI托管账号，3月10日正式封禁批量运营账号...
    评分: 40.0 (时效20 + 相关5 + 权威15)
    来源: CBNData | 日期: 2026-03-13
    关键词: 小红书, AI
```

---

### JSON输出

```json
[
  {
    "title": "腾讯2025年财报：营销服务全年收入达1450亿增19%",
    "source": "QQ News",
    "url": "https://news.qq.com/...",
    "content": "腾讯2025年营销服务收入...",
    "date": "2026-03-18",
    "_score": 55.0,
    "_matched_keywords": ["腾讯", "营销"],
    "_time_score": 30,
    "_relevance_score": 5,
    "_authority_score": 20
  }
]
```

---

## 🚀 下一步扩展

### TODO List

1. **行业媒体采集**
   - [ ] 实现RSS订阅解析
   - [ ] 或使用fetch_web抓取官网
   - [ ] 支持36氪、虎嗅、钛媒体等

2. **更智能的去重**
   - [ ] 基于embedding的语义去重
   - [ ] 而非简单的标题匹配

3. **更精准的评分**
   - [ ] 引入AI评分
   - [ ] 考虑内容深度、数据丰富度

4. **自动化采集**
   - [ ] 定时任务（每日/每小时）
   - [ ] 自动保存到数据库

---

## 📞 问题反馈

**常见问题：**

**Q: 为什么某些新闻被过滤了？**
A: 检查分数（`_score`），可能是：
- 时效性低（超过30天）
- 相关性低（缺少核心关键词）
- 权威性低（非主流媒体）

**Q: 如何调整筛选严格度？**
A: 调整`min_score`参数：
- 严格：60分以上
- 中等：50分以上
- 宽松：40分以上

**Q: 如何添加新的关键词？**
A: 修改`keywords_weight`字典，添加：
```python
'新关键词': 权重  # 1/2/3
```

---

**版本：** v2.0  
**更新日期：** 2026-03-24  
**作者：** AI Assistant
