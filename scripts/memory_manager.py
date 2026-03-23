#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商业化洞察双层记忆管理系统
- 短期记忆：7-14天，用于去重和递进识别
- 长期记忆：3-6个月，用于趋势分析和背景理解
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MemoryManager:
    """双层记忆管理器"""
    
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = os.path.join(os.path.dirname(__file__), '..', 'memory')
        
        self.base_dir = base_dir
        self.short_term_dir = os.path.join(base_dir, 'short_term')
        self.long_term_dir = os.path.join(base_dir, 'long_term')
        self.topics_file = os.path.join(self.long_term_dir, 'topics.json')
        
        # 确保目录存在
        os.makedirs(self.short_term_dir, exist_ok=True)
        os.makedirs(self.long_term_dir, exist_ok=True)
        
        # 初始化长期记忆
        if not os.path.exists(self.topics_file):
            self._init_topics_file()
    
    def _init_topics_file(self):
        """初始化长期记忆主题文件"""
        topics_data = {
            "meta": {
                "created": datetime.now().strftime('%Y-%m-%d'),
                "last_updated": datetime.now().strftime('%Y-%m-%d'),
                "version": "1.0",
                "description": "商业化洞察长期记忆 - 按主题追踪行业演进"
            },
            "topics": {}
        }
        with open(self.topics_file, 'w', encoding='utf-8') as f:
            json.dump(topics_data, f, ensure_ascii=False, indent=2)
    
    # ==================== 短期记忆 ====================
    
    def save_daily_memory(self, date: str, news: List[Dict], insights: List[Dict]):
        """保存每日记忆到短期记忆库"""
        memory_file = os.path.join(self.short_term_dir, f'{date}.json')
        
        daily_memory = {
            "date": date,
            "news": news,
            "insights": insights,
            "created_at": datetime.now().isoformat()
        }
        
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(daily_memory, f, ensure_ascii=False, indent=2)
        
        logging.info(f"✅ 短期记忆已保存: {date} ({len(news)}条新闻, {len(insights)}条洞察)")
    
    def get_recent_memories(self, days: int = 7) -> List[Dict]:
        """获取最近N天的记忆"""
        memories = []
        today = datetime.now()
        
        for i in range(days):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            memory_file = os.path.join(self.short_term_dir, f'{date}.json')
            
            if os.path.exists(memory_file):
                with open(memory_file, 'r', encoding='utf-8') as f:
                    memories.append(json.load(f))
        
        return memories
    
    def is_news_duplicate(self, title: str, url: str = None, days: int = 7) -> bool:
        """检查新闻是否在最近N天内重复"""
        recent_memories = self.get_recent_memories(days)
        
        for memory in recent_memories:
            for news in memory.get('news', []):
                # 标题完全相同
                if news.get('title') == title:
                    return True
                # URL相同（如果提供）
                if url and news.get('url') == url:
                    return True
                # 标题高度相似（简单判断，可以后续优化）
                if self._is_similar_title(title, news.get('title', '')):
                    return True
        
        return False
    
    def _is_similar_title(self, title1: str, title2: str, threshold: float = 0.8) -> bool:
        """判断两个标题是否相似（基于关键词重叠度）"""
        # 提取关键词（去除常见停用词）
        stopwords = {'的', '了', '在', '是', '和', '与', '及', '等', '、', '，', '：'}
        
        words1 = set([w for w in title1 if w not in stopwords and len(w) > 1])
        words2 = set([w for w in title2 if w not in stopwords and len(w) > 1])
        
        if not words1 or not words2:
            return False
        
        # 计算Jaccard相似度
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        similarity = intersection / union if union > 0 else 0
        return similarity >= threshold
    
    def cleanup_old_memories(self, keep_days: int = 14):
        """清理超过N天的短期记忆"""
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        deleted_count = 0
        
        for filename in os.listdir(self.short_term_dir):
            if not filename.endswith('.json'):
                continue
            
            try:
                date_str = filename.replace('.json', '')
                file_date = datetime.strptime(date_str, '%Y-%m-%d')
                
                if file_date < cutoff_date:
                    file_path = os.path.join(self.short_term_dir, filename)
                    os.remove(file_path)
                    deleted_count += 1
                    logging.info(f"🗑️  删除过期记忆: {filename}")
            except Exception as e:
                logging.warning(f"处理文件 {filename} 时出错: {e}")
        
        if deleted_count > 0:
            logging.info(f"✅ 清理完成，删除 {deleted_count} 个过期记忆文件")
    
    # ==================== 长期记忆 ====================
    
    def get_topic_history(self, topic: str) -> Optional[Dict]:
        """获取某个主题的历史演进"""
        with open(self.topics_file, 'r', encoding='utf-8') as f:
            topics_data = json.load(f)
        
        return topics_data.get('topics', {}).get(topic)
    
    def update_topic(self, topic: str, event: str, stage: str, additional_info: Dict = None):
        """更新主题时间线"""
        with open(self.topics_file, 'r', encoding='utf-8') as f:
            topics_data = json.load(f)
        
        if topic not in topics_data['topics']:
            topics_data['topics'][topic] = {
                "timeline": [],
                "current_stage": "",
                "trend": "",
                "keywords": []
            }
        
        # 添加新事件
        new_event = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "event": event,
            "stage": stage
        }
        
        if additional_info:
            new_event.update(additional_info)
        
        topics_data['topics'][topic]['timeline'].append(new_event)
        topics_data['topics'][topic]['current_stage'] = stage
        topics_data['meta']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        
        # 保存
        with open(self.topics_file, 'w', encoding='utf-8') as f:
            json.dump(topics_data, f, ensure_ascii=False, indent=2)
        
        logging.info(f"✅ 长期记忆已更新: {topic} - {event}")
    
    def get_all_topics(self) -> Dict:
        """获取所有主题"""
        with open(self.topics_file, 'r', encoding='utf-8') as f:
            topics_data = json.load(f)
        
        return topics_data.get('topics', {})
    
    def extract_topic_from_news(self, title: str, content: str = "") -> str:
        """从新闻中提取主题（简单实现，可后续优化）"""
        # 定义常见主题关键词
        topic_keywords = {
            "小红书-种草": ["小红书", "种草", "WILL", "AIPS"],
            "字节-AI商业化": ["豆包", "AI购物", "字节", "抖音AI"],
            "直播电商-合规": ["直播电商", "监管", "合规", "管理办法"],
            "腾讯-视频号": ["视频号", "腾讯", "微信"],
            "快手-电商": ["快手", "电商", "泛货架", "磁力"],
            "AIGC-广告": ["AIGC", "AI广告", "AI素材", "混元", "可灵"],
            "本地生活": ["本地生活", "O2O", "美团", "到店"]
        }
        
        # 简单匹配
        text = title + " " + content
        for topic, keywords in topic_keywords.items():
            if any(kw in text for kw in keywords):
                return topic
        
        return "其他"
    
    def analyze_news_progression(self, topic: str, new_event: str) -> Dict:
        """分析新闻是否为主题的递进"""
        history = self.get_topic_history(topic)
        
        if not history or not history.get('timeline'):
            return {
                "is_new": True,
                "progression_type": "首次",
                "context": None
            }
        
        # 获取最近的事件
        latest_events = history['timeline'][-3:]  # 最近3个事件
        current_stage = history.get('current_stage', '')
        
        return {
            "is_new": False,
            "progression_type": "进展",  # 可以是：进展/深化/转折
            "context": {
                "latest_events": latest_events,
                "current_stage": current_stage
            }
        }


if __name__ == '__main__':
    # 测试代码
    mm = MemoryManager()
    
    # 测试短期记忆
    test_news = [
        {
            "title": "小红书WILL大会种草进入效果化",
            "source": "Morketing",
            "url": "https://test.com/1",
            "topic": "小红书-种草",
            "keywords": ["小红书", "WILL", "种草"],
            "summary": "官宣种草效果化"
        }
    ]
    
    test_insights = [
        {
            "title": "小红书种草进入效果化",
            "topic": "小红书-种草",
            "stage": "官宣"
        }
    ]
    
    mm.save_daily_memory("2026-03-23", test_news, test_insights)
    
    # 测试去重
    is_dup = mm.is_news_duplicate("小红书WILL大会种草进入效果化")
    print(f"是否重复: {is_dup}")
    
    # 测试长期记忆
    mm.update_topic(
        topic="小红书-种草效果化",
        event="WILL大会官宣种草进入效果化时代",
        stage="官宣期",
        additional_info={"产品": "AIPS人群资产模型"}
    )
    
    print("✅ 记忆管理器测试完成")
