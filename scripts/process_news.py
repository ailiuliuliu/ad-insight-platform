from memory_manager import MemoryManager
from datetime import datetime
import json

# 初始化记忆管理器
mm = MemoryManager()

# 搜集到的新闻
raw_news = [
    {
        'title': '小红书打击AI托管账号，3月10日正式封禁批量运营账号',
        'source': 'CBNData',
        'url': 'https://m.cbndata.com/information/295097',
        'content': '小红书针对批量运营的AI托管账号正式出手，2026年3月10日开始封禁。这些账号自动化程度高、真实性无法考证，主要用于广告变现或导流商品链接。',
        'date': '2026-03-13',
        'keywords': ['小红书', 'AI托管', '账号治理', '商业化']
    },
    {
        'title': '腾讯2025年财报：营销服务全年收入达1450亿增19%',
        'source': 'QQ News',
        'url': 'https://news.qq.com/rain/a/20260318A083KU00',
        'content': '腾讯2025年营销服务收入1450亿元，同比增长19%。视频号广告投放需求持续增加，围绕素材供给、行业化能力及经营优化持续推进。',
        'date': '2026-03-18',
        'keywords': ['腾讯', '视频号', '广告', '营销']
    },
    {
        'title': 'AI漫剧告别"草台班子"，走向掘金赛道',
        'source': '人民大学新闻',
        'url': 'https://news.ruc.edu.cn/2034793552568098818.html',
        'content': '漫剧从2015年的"PPT动画"走向AI赋能的掘金赛道。过去每分钟成本数万元、制作周期几个月，现在AI技术大幅降低成本和周期。',
        'date': '2026-03-21',
        'keywords': ['AI漫剧', 'AIGC', '内容生产', '成本优化']
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
