#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商业化洞察平台智能更新系统 v2.0
集成双层记忆架构，支持去重和递进识别
"""

import json
import logging
from datetime import datetime
from memory_manager import MemoryManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class InsightGenerator:
    """洞察生成器（集成记忆系统）"""
    
    def __init__(self):
        self.memory = MemoryManager()
        self.today = datetime.now().strftime('%Y-%m-%d')
    
    def process_news(self, raw_news_list: list) -> list:
        """
        处理原始新闻列表
        - 去重
        - 提取主题
        - 分析递进关系
        """
        processed_news = []
        
        for news in raw_news_list:
            title = news.get('title', '')
            url = news.get('url', '')
            
            # 1. 短期记忆去重
            if self.memory.is_news_duplicate(title, url, days=7):
                logging.info(f"⏭️  跳过重复新闻: {title[:30]}...")
                continue
            
            # 2. 提取主题
            topic = self.memory.extract_topic_from_news(
                title, 
                news.get('summary', '')
            )
            
            # 3. 分析递进关系
            progression = self.memory.analyze_news_progression(
                topic, 
                title
            )
            
            # 4. 保存处理后的新闻
            processed_news.append({
                **news,
                'topic': topic,
                'progression': progression,
                'processed_at': datetime.now().isoformat()
            })
        
        logging.info(f"✅ 新闻处理完成: 原始{len(raw_news_list)}条 → 去重后{len(processed_news)}条")
        return processed_news
    
    def generate_insight(self, news: dict) -> dict:
        """
        基于单条新闻生成洞察
        - 根据progression类型生成不同格式的洞察
        """
        topic = news.get('topic', '其他')
        progression = news.get('progression', {})
        is_new = progression.get('is_new', True)
        context = progression.get('context')
        
        # 构造洞察标题
        if is_new:
            # 新主题
            badge = "【新】"
            title_template = news.get('title', '')
        else:
            # 有历史背景的递进
            badge = "【进展】"
            if context and context.get('latest_events'):
                # 提取历史事件
                latest = context['latest_events'][-1]
                prev_event = latest.get('event', '')
                title_template = f"{topic}从{prev_event}到{news.get('title', '')}"
            else:
                title_template = news.get('title', '')
        
        # 构造洞察内容
        insight_content = self._build_insight_content(news, progression)
        
        return {
            'badge': badge,
            'title': title_template,
            'topic': topic,
            'content': insight_content,
            'source_news': news,
            'generated_at': datetime.now().isoformat()
        }
    
    def _build_insight_content(self, news: dict, progression: dict) -> dict:
        """构造洞察内容结构"""
        is_new = progression.get('is_new', True)
        context = progression.get('context')
        
        if is_new:
            # 新主题：竞对动向 + 行业意义 + 快手应对
            return {
                'type': 'new',
                'sections': {
                    '竞对动向': news.get('summary', ''),
                    '行业意义': '（待生成）',
                    '快手应对': '（待生成）'
                }
            }
        else:
            # 递进主题：背景回顾 + 最新进展 + 快手启示
            timeline_text = ""
            if context and context.get('latest_events'):
                events = context['latest_events']
                timeline_text = "、".join([
                    f"{e.get('date', '')} {e.get('event', '')}" 
                    for e in events
                ])
            
            return {
                'type': 'progression',
                'sections': {
                    '背景回顾': timeline_text,
                    '最新进展': news.get('summary', ''),
                    '快手启示': '（待生成）'
                }
            }
    
    def save_to_memory(self, processed_news: list, insights: list):
        """保存今日处理结果到记忆系统"""
        # 1. 保存到短期记忆
        news_for_memory = [
            {
                'title': n.get('title', ''),
                'source': n.get('source', ''),
                'url': n.get('url', ''),
                'topic': n.get('topic', ''),
                'summary': n.get('summary', '')
            }
            for n in processed_news
        ]
        
        insights_for_memory = [
            {
                'title': i.get('title', ''),
                'topic': i.get('topic', ''),
                'badge': i.get('badge', '')
            }
            for i in insights
        ]
        
        self.memory.save_daily_memory(
            self.today,
            news_for_memory,
            insights_for_memory
        )
        
        # 2. 更新长期记忆
        for news in processed_news:
            topic = news.get('topic', '')
            if topic == '其他':
                continue
            
            self.memory.update_topic(
                topic=topic,
                event=news.get('title', ''),
                stage=news.get('progression', {}).get('progression_type', '未知'),
                additional_info={
                    'source': news.get('source', ''),
                    'url': news.get('url', '')
                }
            )
        
        logging.info(f"✅ 记忆已保存: 短期({len(news_for_memory)}条) + 长期({len(processed_news)}个主题更新)")
    
    def cleanup_old_memories(self):
        """清理过期记忆"""
        self.memory.cleanup_old_memories(keep_days=14)


def main():
    """主流程"""
    logging.info("=" * 50)
    logging.info("商业化洞察平台智能更新系统 v2.0")
    logging.info("=" * 50)
    
    generator = InsightGenerator()
    
    # 示例：模拟新闻数据
    raw_news = [
        {
            'title': '小红书启动全国商家培训，推广AIPS人群资产模型',
            'source': 'Morketing',
            'url': 'https://test.com/1',
            'summary': '继WILL大会后，小红书启动全国商家培训...'
        },
        {
            'title': '豆包AI购物功能内测',
            'source': '证券时报',
            'url': 'https://test.com/2',
            'summary': '字节跳动旗下豆包开启AI购物功能...'
        }
    ]
    
    # 1. 处理新闻（去重、提取主题、分析递进）
    processed_news = generator.process_news(raw_news)
    
    # 2. 生成洞察
    insights = []
    for news in processed_news:
        insight = generator.generate_insight(news)
        insights.append(insight)
        logging.info(f"✅ 生成洞察: {insight.get('badge', '')} {insight.get('title', '')[:40]}...")
    
    # 3. 保存到记忆
    generator.save_to_memory(processed_news, insights)
    
    # 4. 清理过期记忆
    generator.cleanup_old_memories()
    
    logging.info("=" * 50)
    logging.info(f"✅ 更新完成！共生成 {len(insights)} 条洞察")
    logging.info("=" * 50)
    
    return insights


if __name__ == '__main__':
    main()
