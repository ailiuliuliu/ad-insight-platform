#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新脚本 - 2026-03-24
多源采集 + 记忆系统 + 洞察生成
"""

from memory_manager import MemoryManager
from datetime import datetime
import json

# 初始化记忆管理器
mm = MemoryManager()

# 采集到的新闻（来自多源）
raw_news = [
    # 1. 腾讯广告 - 漫剧赛道
    {
        'title': '日耗突破350万！漫剧赛道持续增长，腾讯广告助你稳抓"开年首金"',
        'source': '腾讯广告',
        'url': 'https://e.qq.com/latestnews',
        'content': '腾讯广告发布最新数据，漫剧赛道日耗突破350万，持续增长趋势明显，成为2026年开年商业化重点',
        'date': '2026-03-17',
        'keywords': ['腾讯', '漫剧', '广告', '商业化']
    },
    # 2. 腾讯广告 - 获客宝Chatbot
    {
        'title': '上新啦！获客宝 Chatbot 正式上线，AI 让线索转化更高效、更简单！',
        'source': '腾讯广告',
        'url': 'https://e.qq.com/latestnews',
        'content': '腾讯广告推出获客宝Chatbot，AI驱动线索转化，极速两步即刻开启AI转化',
        'date': '2026-03-17',
        'keywords': ['腾讯', 'AI', 'Chatbot', '获客']
    },
    # 3. 腾讯服饰行业白皮书
    {
        'title': '"高增长、高复购"的生意逻辑拆解：腾讯服饰行业白皮书（2026版）重磅发布',
        'source': '腾讯广告',
        'url': 'https://e.qq.com/latestnews',
        'content': '腾讯服饰行业白皮书2026版发布，拆解高增长、高复购的生意逻辑',
        'date': '2026-03-17',
        'keywords': ['腾讯', '服饰', '白皮书', '营销']
    },
    # 4. AI漫剧 - 上海微短剧大会
    {
        'title': 'AI如何重塑微短剧生产？2026上海微短剧大会在沪举行',
        'source': '上海市文化和旅游局',
        'url': 'https://whlyj.sh.gov.cn/wlyw/20260310/6481c6d52ee548b58fa968bfff038099.html',
        'content': '上海市发布微短剧"繁花"3.0计划，启动首届微短剧（含漫剧）剧本征集大赛，持续推动上海微短剧产业发展',
        'date': '2026-03-10',
        'keywords': ['AIGC', '漫剧', '短剧', '上海']
    },
    # 5. 人民日报 - 漫剧成为新看点
    {
        'title': '漫剧成为微短剧领域新看点',
        'source': '人民日报',
        'url': 'http://paper.people.com.cn/rmrbhwb/pc/content/202603/23/content_30146543.html',
        'content': 'AIGC短片《霍去病》等作品引发关注，漫剧成为微短剧领域新看点',
        'date': '2026-03-23',
        'keywords': ['漫剧', 'AIGC', '短剧']
    },
    # 6. 微短剧迈过千亿门槛
    {
        'title': '迈过千亿门槛微短剧行业成2026文化新宠',
        'source': '新华网',
        'url': 'http://jjckb.xinhuanet.com/20260207/f799547cd03e4fb6b850524a7892426f/c.html',
        'content': '微短剧行业迈过千亿门槛，成为2026年文化经济新业态，数字技术与文化创意深度交融',
        'date': '2026-02-07',
        'keywords': ['短剧', '千亿', '文化产业']
    }
]

# 处理新闻（去重 + 提取主题）
processed_news = []
for news in raw_news:
    title = news['title']
    url = news['url']
    
    # 检查是否重复
    if mm.is_news_duplicate(title, url, days=7):
        print(f"⏭️  跳过重复新闻: {title[:40]}...")
        continue
    
    # 提取主题
    topic = mm.extract_topic_from_news(title, news['content'])
    
    # 分析递进关系
    progression = mm.analyze_news_progression(topic, title)
    
    processed_news.append({
        **news,
        'topic': topic,
        'progression': progression
    })
    
    badge = "【新】" if progression['is_new'] else "【进展】"
    print(f"✅ {badge} {topic}: {title[:40]}...")

# 保存到记忆
if processed_news:
    news_for_memory = [{
        'title': n['title'],
        'source': n['source'],
        'url': n['url'],
        'topic': n['topic'],
        'summary': n['content'][:200]
    } for n in processed_news]
    
    insights_for_memory = [{
        'title': n['title'],
        'topic': n['topic'],
        'badge': "【新】" if n['progression']['is_new'] else "【进展】"
    } for n in processed_news]
    
    today = datetime.now().strftime('%Y-%m-%d')
    mm.save_daily_memory(today, news_for_memory, insights_for_memory)
    
    # 更新长期记忆
    for news in processed_news:
        topic = news['topic']
        if topic and topic != '其他':
            mm.update_topic(
                topic=topic,
                event=news['title'],
                stage=news['progression'].get('progression_type', '进展')
            )
    
    print(f"\n✅ 处理完成！共{len(processed_news)}条有效新闻")
    
    # 输出JSON供后续使用
    print("\n=== 处理后的新闻数据 ===")
    print(json.dumps(processed_news, ensure_ascii=False, indent=2))
else:
    print("⚠️  所有新闻都是重复的，没有需要更新的内容")
