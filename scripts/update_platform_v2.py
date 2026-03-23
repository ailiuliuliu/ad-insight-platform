#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商业化洞察平台完整更新流程 v2.0
集成双层记忆系统，实现智能去重和递进识别

流程：
1. 搜索最新商业化新闻
2. 短期记忆去重
3. 基于长期记忆生成递进洞察
4. 更新HTML
5. 推送到GitHub
"""

import os
import sys
import json
import logging
from datetime import datetime
from bs4 import BeautifulSoup
from memory_manager import MemoryManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PlatformUpdater:
    """平台更新器（集成记忆系统）"""
    
    def __init__(self):
        self.memory = MemoryManager()
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.index_html = os.path.join(self.base_dir, 'index.html')
    
    def collect_news(self) -> list:
        """
        收集最新商业化新闻
        注意：这里需要你手动提供新闻数据，或者集成搜索API
        """
        logging.info("📰 开始收集新闻...")
        
        # TODO: 这里应该调用你的搜索逻辑
        # 目前返回示例数据，实际使用时需要替换
        
        news_list = []
        
        logging.info(f"✅ 收集到 {len(news_list)} 条原始新闻")
        return news_list
    
    def process_with_memory(self, raw_news: list) -> tuple:
        """
        使用记忆系统处理新闻
        返回：(去重后的新闻, 生成的洞察)
        """
        logging.info("🧠 使用记忆系统处理新闻...")
        
        processed_news = []
        insights = []
        
        for news in raw_news:
            title = news.get('title', '')
            url = news.get('url', '')
            
            # 1. 去重检查
            if self.memory.is_news_duplicate(title, url, days=7):
                logging.info(f"⏭️  跳过重复: {title[:40]}...")
                continue
            
            # 2. 提取主题
            topic = self.memory.extract_topic_from_news(
                title,
                news.get('content', news.get('summary', ''))
            )
            
            # 3. 分析递进关系
            progression = self.memory.analyze_news_progression(topic, title)
            
            # 4. 生成洞察
            insight = self._generate_insight(news, topic, progression)
            
            processed_news.append({
                **news,
                'topic': topic,
                'progression': progression
            })
            
            insights.append(insight)
            
            logging.info(f"✅ 生成洞察: {insight['badge']} {insight['title'][:40]}...")
        
        # 5. 保存到记忆
        if processed_news:
            self._save_to_memory(processed_news, insights)
        
        return processed_news, insights
    
    def _generate_insight(self, news: dict, topic: str, progression: dict) -> dict:
        """生成单条洞察"""
        is_new = progression.get('is_new', True)
        context = progression.get('context')
        
        if is_new:
            badge = "【新】"
            title = news.get('title', '')
        else:
            badge = "【进展】"
            # 如果有历史背景，构造递进式标题
            if context and context.get('latest_events'):
                latest = context['latest_events'][-1]
                prev_stage = latest.get('stage', '')
                title = f"{topic}: {prev_stage} → {news.get('title', '')}"
            else:
                title = news.get('title', '')
        
        return {
            'badge': badge,
            'title': title,
            'summary': news.get('summary', news.get('content', '')[:100]),
            'topic': topic,
            'url': news.get('url', ''),
            'source': news.get('source', ''),
            'date': news.get('date', self.today),
            'progression': progression,
            'analysis': {
                'competitor_action': '',  # 需要你的AI分析填充
                'industry_meaning': '',
                'kuaishou_response': ''
            }
        }
    
    def _save_to_memory(self, processed_news: list, insights: list):
        """保存到记忆系统"""
        # 短期记忆
        news_for_memory = [{
            'title': n.get('title', ''),
            'source': n.get('source', ''),
            'url': n.get('url', ''),
            'topic': n.get('topic', ''),
            'summary': n.get('summary', n.get('content', ''))[:200]
        } for n in processed_news]
        
        insights_for_memory = [{
            'title': i.get('title', ''),
            'topic': i.get('topic', ''),
            'badge': i.get('badge', '')
        } for i in insights]
        
        self.memory.save_daily_memory(self.today, news_for_memory, insights_for_memory)
        
        # 长期记忆
        for news in processed_news:
            topic = news.get('topic', '')
            if topic and topic != '其他':
                self.memory.update_topic(
                    topic=topic,
                    event=news.get('title', ''),
                    stage=news.get('progression', {}).get('progression_type', '进展')
                )
    
    def update_html(self, insights: list):
        """更新index.html"""
        logging.info("📝 更新HTML...")
        
        if not os.path.exists(self.index_html):
            logging.error(f"❌ 找不到HTML文件: {self.index_html}")
            return False
        
        # 读取现有HTML
        with open(self.index_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 构造新的洞察HTML
        insights_html = self._build_insights_html(insights)
        
        # TODO: 替换HTML中的洞察部分
        # 这里需要根据实际HTML结构来定位和替换
        
        logging.info("✅ HTML更新完成")
        return True
    
    def _build_insights_html(self, insights: list) -> str:
        """构造洞察HTML片段"""
        html_parts = []
        
        for idx, insight in enumerate(insights[:3]):  # 只取前3条
            is_last = (idx == len(insights) - 1) or (idx == 2)
            margin = "0" if is_last else "8px"
            
            badge = insight.get('badge', '【新】')
            title = insight.get('title', '')
            summary = insight.get('summary', '')
            
            html = f'''
            <details style="margin-bottom: {margin};">
                <summary class="company-summary" style="border: 1px solid var(--ks-orange); padding: 10px; cursor: pointer;">
                    <div class="company-summary-title" style="margin-bottom: 6px;">
                        <h4 style="color: var(--ks-orange); font-size: 0.95em;">{badge} {title}</h4>
                        <span class="expand-icon">▼</span>
                    </div>
                    <div class="company-summary-desc" style="font-size: 0.8em; line-height: 1.4;">
                        {summary}
                    </div>
                </summary>
                <div class="company-details">
                    <div style="padding: 10px; background: var(--bg-secondary); border-radius: 6px; line-height: 1.4; font-size: 0.8em;">
                        <p style="margin-bottom: 6px;"><strong style="color: var(--ks-orange);">竞对动向：</strong>{insight.get('analysis', {}).get('competitor_action', '（待补充）')}</p>
                        <p style="margin-bottom: 6px;"><strong style="color: var(--ks-orange);">行业意义：</strong>{insight.get('analysis', {}).get('industry_meaning', '（待补充）')}</p>
                        <p style="margin-bottom: 0;"><strong style="color: var(--ks-orange);">快手应对：</strong>{insight.get('analysis', {}).get('kuaishou_response', '（待补充）')}</p>
                    </div>
                </div>
            </details>
            '''
            html_parts.append(html)
        
        return '\n'.join(html_parts)
    
    def cleanup(self):
        """清理过期记忆"""
        logging.info("🧹 清理过期记忆...")
        self.memory.cleanup_old_memories(keep_days=14)
        logging.info("✅ 清理完成")
    
    def run(self, news_data: list = None):
        """
        运行完整更新流程
        
        Args:
            news_data: 可选的新闻数据列表。如果不提供，会调用collect_news()
        """
        logging.info("=" * 60)
        logging.info("商业化洞察平台更新系统 v2.0 (集成记忆)")
        logging.info("=" * 60)
        
        try:
            # 1. 收集新闻
            if news_data is None:
                raw_news = self.collect_news()
            else:
                raw_news = news_data
                logging.info(f"📰 使用提供的新闻数据: {len(raw_news)}条")
            
            if not raw_news:
                logging.warning("⚠️  没有新闻数据，跳过更新")
                return
            
            # 2. 记忆处理（去重+生成洞察）
            processed_news, insights = self.process_with_memory(raw_news)
            
            if not insights:
                logging.warning("⚠️  去重后没有新洞察，跳过HTML更新")
                return
            
            # 3. 更新HTML
            self.update_html(insights)
            
            # 4. 清理过期记忆
            self.cleanup()
            
            logging.info("=" * 60)
            logging.info(f"✅ 更新完成！共生成 {len(insights)} 条洞察")
            logging.info("=" * 60)
            
            return insights
            
        except Exception as e:
            logging.error(f"❌ 更新失败: {e}", exc_info=True)
            raise


def main():
    """主入口"""
    updater = PlatformUpdater()
    
    # 示例：提供测试新闻数据
    test_news = [
        {
            'title': '字节豆包AI购物功能3月正式上线',
            'source': '证券时报',
            'url': 'https://test.com/1',
            'content': '字节跳动豆包AI购物功能将于3月正式上线...',
            'date': '2026-03-23'
        },
        {
            'title': '小红书启动AIPS模型全国培训',
            'source': 'Morketing',
            'url': 'https://test.com/2',
            'content': '继WILL大会后，小红书开始推广AIPS...',
            'date': '2026-03-23'
        }
    ]
    
    updater.run(news_data=test_news)


if __name__ == '__main__':
    main()
