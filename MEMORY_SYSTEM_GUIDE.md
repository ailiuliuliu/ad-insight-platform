# 商业化洞察平台 v2.0 - 双层记忆系统使用指南

## 🎯 核心升级

### v1.0 → v2.0 重大变化

**v1.0问题：**
- ❌ 每天洞察相互割裂
- ❌ 重复展示相同新闻
- ❌ 缺乏历史背景和递进关系

**v2.0解决方案：**
- ✅ 双层记忆架构（短期+长期）
- ✅ 智能去重（7天内）
- ✅ 递进识别（从"官宣"到"培训"到"落地"）
- ✅ 连贯洞察（带历史背景）

---

## 🧠 双层记忆架构

### 📝 短期记忆（7-14天）
**用途：** 去重 + 快速查询

**存储位置：** `memory/short_term/`

**文件格式：** `YYYY-MM-DD.json`

**内容示例：**
```json
{
  "date": "2026-03-23",
  "news": [
    {
      "title": "小红书WILL大会种草进入效果化",
      "source": "Morketing",
      "topic": "小红书-种草效果化",
      "summary": "官宣种草效果化时代..."
    }
  ],
  "insights": [
    {
      "title": "小红书种草进入效果化",
      "badge": "【新】",
      "topic": "小红书-种草效果化"
    }
  ]
}
```

**自动维护：**
- 每日自动保存
- 超过14天自动删除

---

### 📚 长期记忆（3-6个月）
**用途：** 趋势分析 + 背景理解

**存储位置：** `memory/long_term/topics.json`

**结构示例：**
```json
{
  "topics": {
    "小红书-种草效果化": {
      "timeline": [
        {
          "date": "2025-12-22",
          "event": "WILL大会首次提出概念",
          "stage": "概念期"
        },
        {
          "date": "2026-01-15",
          "event": "AIPS模型发布",
          "stage": "产品期"
        },
        {
          "date": "2026-03-18",
          "event": "全国商家培训启动",
          "stage": "推广期"
        }
      ],
      "current_stage": "推广期"
    }
  }
}
```

---

## 🔄 工作流程

### 每日更新流程

```
1. 搜索最新商业化新闻
   ↓
2. 短期记忆查重
   - 7天内出现过？→ 跳过
   - 没出现过？→ 继续
   ↓
3. 长期记忆查询背景
   - 这个主题之前有什么进展？
   - 现在处于什么阶段？
   ↓
4. 生成洞察
   - 【新】：首次出现的主题
   - 【进展】：有历史背景的递进
   ↓
5. 更新HTML
   ↓
6. 保存到双层记忆
```

---

## 💻 使用方式

### 方式1：Python脚本（推荐）

```bash
cd ad-insight-demo/scripts
python3 update_platform_v2.py
```

**特点：**
- 自动去重
- 自动识别递进
- 自动保存记忆

---

### 方式2：在AI对话中调用

```python
from scripts.update_platform_v2 import PlatformUpdater

updater = PlatformUpdater()

# 提供新闻数据
news_data = [
    {
        'title': '...',
        'source': '...',
        'url': '...',
        'content': '...',
        'date': '2026-03-23'
    }
]

# 运行更新
insights = updater.run(news_data=news_data)
```

---

## 📊 洞察格式演进

### 场景1：完全新主题

**输入新闻：**
```
京东进军本地生活，以外卖到店自提切入
```

**生成洞察：**
```
【新】京东进军本地生活，以外卖到店自提切入

竞对动向：京东在上海杨浦试点...
行业意义：本地生活竞争加剧...
快手应对：可切入县域本地生活...
```

---

### 场景2：有历史背景的递进

**历史记录：**
- 2025-12-22: 小红书WILL大会提出"种草效果化"
- 2026-01-15: 发布AIPS人群资产模型

**新闻：**
```
小红书启动全国商家培训，推广AIPS模型
```

**生成洞察：**
```
【进展】小红书种草效果化从战略落地到全国推广

背景回顾：
- 2025年12月 WILL大会首次提出概念
- 2026年1月 AIPS人群资产模型发布

最新进展：
本周启动全国商家培训，推广AIPS模型...

快手启示：
从战略→产品→培训的完整闭环值得学习
```

---

## 🛠️ 核心模块

### 1. memory_manager.py
**功能：** 双层记忆管理

**关键方法：**
- `save_daily_memory()`: 保存每日记忆
- `is_news_duplicate()`: 检查新闻是否重复
- `get_topic_history()`: 获取主题历史
- `update_topic()`: 更新主题时间线
- `cleanup_old_memories()`: 清理过期记忆

---

### 2. update_platform_v2.py
**功能：** 完整更新流程

**关键方法：**
- `collect_news()`: 收集新闻
- `process_with_memory()`: 记忆处理
- `update_html()`: 更新HTML
- `run()`: 执行完整流程

---

## 📁 文件结构

```
ad-insight-demo/
├── memory/
│   ├── short_term/          # 短期记忆（滚动14天）
│   │   ├── 2026-03-23.json
│   │   ├── 2026-03-22.json
│   │   └── ...
│   │
│   └── long_term/           # 长期记忆
│       └── topics.json      # 主题时间线
│
├── scripts/
│   ├── memory_manager.py    # 记忆管理器
│   ├── update_platform_v2.py  # 平台更新器v2
│   └── ...
│
└── index.html
```

---

## 🧪 测试验证

### 测试去重功能

```bash
cd ad-insight-demo/scripts
python3 -c "
from memory_manager import MemoryManager

mm = MemoryManager()

# 保存测试新闻
mm.save_daily_memory('2026-03-23', [
    {'title': '小红书WILL大会', 'source': 'Test'}
], [])

# 检查是否重复
is_dup = mm.is_news_duplicate('小红书WILL大会')
print(f'是否重复: {is_dup}')  # 应该输出 True
"
```

---

### 测试递进识别

```bash
cd ad-insight-demo/scripts
python3 -c "
from memory_manager import MemoryManager

mm = MemoryManager()

# 更新主题历史
mm.update_topic(
    topic='小红书-种草效果化',
    event='WILL大会官宣',
    stage='官宣期'
)

# 分析新事件
progression = mm.analyze_news_progression(
    '小红书-种草效果化',
    '启动全国培训'
)

print(progression)
# 应该显示 is_new=False, progression_type='进展'
"
```

---

## 🔧 维护

### 手动清理过期记忆

```bash
cd ad-insight-demo/scripts
python3 -c "
from memory_manager import MemoryManager

mm = MemoryManager()
mm.cleanup_old_memories(keep_days=14)
"
```

---

### 查看所有主题

```bash
cd ad-insight-demo/scripts
python3 -c "
from memory_manager import MemoryManager
import json

mm = MemoryManager()
topics = mm.get_all_topics()

print(json.dumps(topics, ensure_ascii=False, indent=2))
"
```

---

## 📈 效果对比

### v1.0（无记忆）

**Day 1:**
```
💡 今日洞察
1. 小红书WILL大会，种草进入效果化
```

**Day 2:**
```
💡 今日洞察
1. 小红书WILL大会，种草进入效果化  ❌ 完全重复
```

---

### v2.0（有记忆）

**Day 1:**
```
💡 今日洞察
1. 【新】小红书WILL大会，种草进入效果化
```

**Day 2:**
```
💡 今日洞察
（无重复新闻，跳过更新）✅ 或
1. 【进展】小红书种草效果化从战略到培训 ✅ 递进式洞察
```

---

## ⚠️ 注意事项

1. **首次使用**：
   - memory目录会自动创建
   - topics.json会自动初始化

2. **记忆容量**：
   - 短期记忆：最多14天
   - 长期记忆：建议每季度整理一次

3. **主题命名**：
   - 格式：`公司-业务`
   - 示例：`小红书-种草效果化`、`字节-AI商业化`

4. **去重阈值**：
   - 默认7天内去重
   - 可调整：`is_news_duplicate(title, url, days=7)`

---

## 🚀 下一步优化

1. **语义去重**：
   - 当前基于关键词
   - 可升级为embedding相似度

2. **趋势预测**：
   - 基于timeline预测下一步
   - 例如：官宣→产品→培训→效果披露

3. **自动归档**：
   - 长期记忆定期压缩
   - 按季度归档

---

## 📞 问题反馈

如有问题，检查日志：
```bash
# 查看最近的记忆文件
ls -lt ad-insight-demo/memory/short_term/

# 查看长期记忆
cat ad-insight-demo/memory/long_term/topics.json
```

---

**版本：** v2.0  
**更新日期：** 2026-03-23  
**作者：** AI Assistant
