#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商业化洞察平台 - 新闻批量处理脚本
2026-03-27 更新批次
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from news_collector_v2 import NewsCollector

def main():
    """批量处理新闻"""
    
    collector = NewsCollector()
    
    # 2026-03-27采集的新闻
    raw_news = [
        {
            'title': '快手短剧日活破3亿，漫剧日耗创新高',
            'url': 'http://www.cnsa.cn/module/download/down.jsp?i_ID=48515&colID=2019',
            'source': '中国网络视听节目服务协会',
            'date': '2026-03-02',
            'category': '行业动态',
            'summary': '2月26日，快手磁力引擎发布最新数据，快手短剧日活突破3亿，漫剧日耗创下新高。漫剧凭借AI低成本优势快速崛起，成为内容消费变现新风口。'
        },
        {
            'title': '港股AI漫剧第一股：中文在线构筑"IP+AI+平台"全产业链壁垒',
            'url': 'https://static.weeklyonstock.com/26/0312/qdy150501.html',
            'source': '港股研报',
            'date': '2026-03-12',
            'category': '行业趋势',
            'summary': '根据巨量引擎数据，字节漫剧赛道日耗峰值达到3000万元。巨量引擎预测，2026年漫剧市场整体规模有望继续扩大，AI技术降低制作成本推动行业爆发。'
        },
        {
            'title': '腾讯服饰行业白皮书（2026版）重磅发布',
            'url': 'https://e.qq.com/latestnews',
            'source': '腾讯广告',
            'date': '2026-03-17',
            'category': '行业洞察',
            'summary': '"高增长、高复购"的生意逻辑拆解，腾讯广告发布服饰行业白皮书（2026版），系统分析服饰品牌在视频号、朋友圈等场景的营销策略与增长路径。'
        }
    ]
    
    print("=" * 80)
    print("开始处理 2026-03-27 新闻批次")
    print("=" * 80)
    print()
    
    # 处理每条新闻
    for i, news in enumerate(raw_news, 1):
        print(f"\n{'='*60}")
        print(f"处理第 {i}/{len(raw_news)} 条新闻")
        print(f"{'='*60}")
        print(f"标题: {news['title']}")
        print(f"来源: {news['source']}")
        print(f"日期: {news['date']}")
        print()
        
        # 记忆系统去重
        is_duplicate = collector.memory.check_duplicate(
            title=news['title'],
            source=news['source'],
            date=news['date']
        )
        
        if is_duplicate:
            print(f"⚠️  【重复】 已存在于记忆系统，跳过")
            continue
        
        # 提取主题
        topics = collector.memory.extract_topics(news['title'], news['summary'])
        print(f"📌 提取主题: {topics}")
        
        # 判断是否为新主题还是已有主题的进展
        progression_type = "【新】"  # 默认为新主题
        
        for topic in topics:
            history = collector.memory.get_topic_history(topic)
            if history:
                progression_type = "【进展】"
                print(f"💡 主题 '{topic}' 存在历史记录，标记为【进展】")
                print(f"   历史: {len(history)} 条相关新闻")
                break
        
        print(f"🏷️  标记: {progression_type}")
        
        # 保存到记忆系统
        collector.memory.add_news(
            title=news['title'],
            url=news['url'],
            source=news['source'],
            date=news['date'],
            topics=topics
        )
        
        print(f"✅ 已保存到记忆系统")
    
    print()
    print("=" * 80)
    print("✅ 批处理完成")
    print("=" * 80)
    
    # 统计信息
    print()
    print("📊 本次更新统计:")
    print(f"   - 处理新闻数: {len(raw_news)}")
    print(f"   - 新增有效: {len([n for n in raw_news if not collector.memory.check_duplicate(n['title'], n['source'], n['date'])])}")

if __name__ == "__main__":
    main()
