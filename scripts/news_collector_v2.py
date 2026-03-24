#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商业化新闻采集系统 v2.0 - 多源采集+智能筛选

采集策略：
1. Google搜索（广度）
2. 定向抓取行业媒体（深度）
3. 智能筛选（时效+价值）

输出：排序后的高价值新闻列表
"""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class NewsCollector:
    """新闻采集器 v2.0"""
    
    def __init__(self):
        self.today = datetime.now()
        
        # 行业媒体RSS源（可扩展）
        self.media_sources = {
            '36氪': 'https://36kr.com/feed',
            '虎嗅': 'https://www.huxiu.com/rss/0.xml',
            '钛媒体': 'https://www.tmtpost.com/rss.xml',
            'Morketing': 'https://morketing.com/feed',
            '数英网': 'https://www.digitaling.com/rss'
        }
        
        # 定向信息源（官方平台）
        self.official_sources = {
            '腾讯广告': 'https://e.qq.com/latestnews',
            '字节巨量学': 'https://school.oceanengine.com/'  # 需要特殊处理
        }
        
        # 关键词权重（用于相关性评分）
        self.keywords_weight = {
            # 核心业务（高权重）
            '快手': 3, '抖音': 3, '字节': 3, '腾讯': 3, '小红书': 3,
            '磁力引擎': 3, '巨量引擎': 3, '视频号': 3,
            
            # 业务方向（中权重）
            '广告': 2, '商业化': 2, '营销': 2, '电商': 2,
            'AI': 2, 'AIGC': 2, '短剧': 2, '漫剧': 2,
            '直播': 2, '本地生活': 2,
            
            # 行业术语（低权重）
            'ROI': 1, 'GMV': 1, '投放': 1, '效果': 1,
            '种草': 1, '流量': 1, '转化': 1
        }
    
    def collect_from_google(self, queries: List[str]) -> List[Dict]:
        """
        从Google搜索采集新闻
        
        Args:
            queries: 搜索关键词列表
            
        Returns:
            新闻列表
        """
        logging.info("📰 开始Google搜索采集...")
        
        # 注意：这里需要你传入实际的搜索结果
        # 实际使用时需要调用search_web工具
        
        news_list = []
        
        logging.info(f"✅ Google搜索采集完成: {len(news_list)}条")
        return news_list
    
    def collect_from_media_sites(self) -> List[Dict]:
        """
        从行业媒体官网采集新闻
        
        注意：实际使用需要实现RSS解析或网页爬取
        这里提供接口示例
        """
        logging.info("🌐 开始行业媒体采集...")
        
        news_list = []
        
        # TODO: 实现RSS订阅解析
        # TODO: 或使用fetch_web工具抓取官网
        
        logging.info(f"✅ 行业媒体采集完成: {len(news_list)}条")
        return news_list
    
    def collect_from_tencent_ads(self, fetch_content: str = None) -> List[Dict]:
        """
        从腾讯广告咨询洞察采集新闻
        
        Args:
            fetch_content: fetch_web抓取的网页内容
            
        Returns:
            新闻列表
        """
        logging.info("🎯 开始腾讯广告采集...")
        
        news_list = []
        
        if not fetch_content:
            logging.warning("⚠️  未提供腾讯广告网页内容，跳过采集")
            return news_list
        
        # 从内容中提取关键信息
        # 注意：这里需要解析HTML，实际使用时需要BeautifulSoup
        # 简化版：直接提取关键词匹配的文本片段
        
        keywords = ['漫剧', '短剧', '获客宝', 'Chatbot', 'AI', '视频号', '直播']
        
        for keyword in keywords:
            if keyword in fetch_content:
                # 简化版：创建一条新闻记录
                news_list.append({
                    'title': f'腾讯广告最新：{keyword}相关更新',
                    'source': '腾讯广告',
                    'url': 'https://e.qq.com/latestnews',
                    'content': f'腾讯广告发布{keyword}相关内容...',
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
        
        logging.info(f"✅ 腾讯广告采集完成: {len(news_list)}条")
        return news_list
    
    def collect_from_oceanengine(self, search_keywords: List[str] = None) -> List[Dict]:
        """
        从字节巨量学采集新闻
        
        由于直接访问可能受限，建议通过Google搜索：
        site:school.oceanengine.com 短剧/漫剧/小说/游戏
        
        Args:
            search_keywords: 搜索关键词列表
            
        Returns:
            新闻列表
        """
        logging.info("📚 开始巨量学采集...")
        
        news_list = []
        
        # 注意：需要通过search_web工具搜索
        # 搜索query示例：site:school.oceanengine.com 短剧 最新
        
        logging.info(f"✅ 巨量学采集完成: {len(news_list)}条（建议使用Google site:搜索）")
        return news_list
    
    def calculate_news_score(self, news: Dict) -> float:
        """
        计算新闻价值分数
        
        评分维度：
        1. 时效性（40%）：越新越高分
        2. 相关性（40%）：关键词匹配度
        3. 权威性（20%）：媒体来源
        
        Returns:
            0-100分
        """
        score = 0.0
        
        # 1. 时效性评分（0-40分）
        try:
            news_date = datetime.strptime(news.get('date', ''), '%Y-%m-%d')
            days_ago = (self.today - news_date).days
            
            if days_ago == 0:
                time_score = 40  # 今天
            elif days_ago <= 3:
                time_score = 35  # 3天内
            elif days_ago <= 7:
                time_score = 30  # 7天内
            elif days_ago <= 14:
                time_score = 20  # 14天内
            elif days_ago <= 30:
                time_score = 10  # 30天内
            else:
                time_score = 0   # 太旧
        except:
            time_score = 10  # 无法解析日期，给保底分
        
        score += time_score
        
        # 2. 相关性评分（0-40分）
        title = news.get('title', '')
        content = news.get('content', news.get('summary', ''))
        text = title + ' ' + content
        
        relevance_score = 0
        matched_keywords = []
        
        for keyword, weight in self.keywords_weight.items():
            if keyword in text:
                relevance_score += weight
                matched_keywords.append(keyword)
        
        # 归一化到0-40
        relevance_score = min(relevance_score, 40)
        score += relevance_score
        
        # 3. 权威性评分（0-20分）
        source = news.get('source', '')
        authority_score = 0
        
        # 官方/头部媒体
        if any(x in source for x in ['新华网', 'QQ News', '36氪', '虎嗅', '钛媒体']):
            authority_score = 20
        # 行业媒体
        elif any(x in source for x in ['Morketing', '数英', 'CBNData', '艾瑞']):
            authority_score = 15
        # 其他媒体
        else:
            authority_score = 10
        
        score += authority_score
        
        # 附加信息
        news['_score'] = score
        news['_matched_keywords'] = matched_keywords
        news['_time_score'] = time_score
        news['_relevance_score'] = relevance_score
        news['_authority_score'] = authority_score
        
        return score
    
    def filter_and_rank(self, news_list: List[Dict], 
                       min_score: float = 50.0,
                       max_days: int = 30,
                       top_n: int = 10) -> List[Dict]:
        """
        筛选并排序新闻
        
        Args:
            news_list: 原始新闻列表
            min_score: 最低分数阈值
            max_days: 最大天数
            top_n: 返回前N条
            
        Returns:
            排序后的新闻列表
        """
        logging.info("🔍 开始筛选和排序...")
        
        filtered_news = []
        
        for news in news_list:
            # 计算分数
            score = self.calculate_news_score(news)
            
            # 筛选：分数阈值
            if score < min_score:
                continue
            
            # 筛选：日期范围
            try:
                news_date = datetime.strptime(news.get('date', ''), '%Y-%m-%d')
                days_ago = (self.today - news_date).days
                if days_ago > max_days:
                    continue
            except:
                pass  # 无日期的保留
            
            filtered_news.append(news)
        
        # 按分数排序
        filtered_news.sort(key=lambda x: x.get('_score', 0), reverse=True)
        
        # 取前N条
        top_news = filtered_news[:top_n]
        
        logging.info(f"✅ 筛选完成: {len(news_list)}条 → {len(filtered_news)}条 → Top {len(top_news)}条")
        
        return top_news
    
    def deduplicate(self, news_list: List[Dict]) -> List[Dict]:
        """
        去重：基于标题相似度
        """
        logging.info("🔄 开始去重...")
        
        unique_news = []
        seen_titles = set()
        
        for news in news_list:
            title = news.get('title', '')
            
            # 简单去重：标题前30字符
            title_key = title[:30]
            
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_news.append(news)
            else:
                logging.debug(f"去重：{title[:40]}...")
        
        logging.info(f"✅ 去重完成: {len(news_list)}条 → {len(unique_news)}条")
        
        return unique_news
    
    def collect_and_filter(self, 
                          google_results: List[Dict] = None,
                          media_results: List[Dict] = None,
                          tencent_ads_content: str = None,
                          oceanengine_results: List[Dict] = None,
                          min_score: float = 50.0,
                          top_n: int = 10) -> List[Dict]:
        """
        完整流程：采集+去重+筛选+排序
        
        Args:
            google_results: Google搜索结果
            media_results: 媒体官网结果
            tencent_ads_content: 腾讯广告网页内容（fetch_web）
            oceanengine_results: 巨量学搜索结果（Google site:）
            min_score: 最低分数
            top_n: 返回前N条
            
        Returns:
            最终新闻列表
        """
        logging.info("=" * 60)
        logging.info("商业化新闻采集系统 v2.0 - 多源采集+智能筛选")
        logging.info("=" * 60)
        
        # 1. 合并所有来源
        all_news = []
        
        if google_results:
            all_news.extend(google_results)
            logging.info(f"📊 Google来源: {len(google_results)}条")
        
        if media_results:
            all_news.extend(media_results)
            logging.info(f"📊 媒体来源: {len(media_results)}条")
        
        if tencent_ads_content:
            tencent_news = self.collect_from_tencent_ads(tencent_ads_content)
            all_news.extend(tencent_news)
            logging.info(f"📊 腾讯广告来源: {len(tencent_news)}条")
        
        if oceanengine_results:
            all_news.extend(oceanengine_results)
            logging.info(f"📊 巨量学来源: {len(oceanengine_results)}条")
        
        logging.info(f"📊 总计: {len(all_news)}条原始新闻")
        
        # 2. 去重
        all_news = self.deduplicate(all_news)
        
        # 3. 筛选+排序
        top_news = self.filter_and_rank(all_news, min_score=min_score, top_n=top_n)
        
        # 4. 输出结果
        logging.info("=" * 60)
        logging.info(f"✅ 最终输出: {len(top_news)}条高价值新闻")
        logging.info("=" * 60)
        
        # 打印Top新闻
        for idx, news in enumerate(top_news, 1):
            logging.info(f"\n[{idx}] {news.get('title', '')[:50]}...")
            logging.info(f"    评分: {news.get('_score', 0):.1f} (时效{news.get('_time_score', 0)} + 相关{news.get('_relevance_score', 0)} + 权威{news.get('_authority_score', 0)})")
            logging.info(f"    来源: {news.get('source', '')} | 日期: {news.get('date', '')}")
            logging.info(f"    关键词: {', '.join(news.get('_matched_keywords', [])[:5])}")
        
        return top_news


def main():
    """示例：如何使用采集器"""
    collector = NewsCollector()
    
    # 模拟Google搜索结果
    google_results = [
        {
            'title': '小红书打击AI托管账号，3月10日正式封禁批量运营账号',
            'source': 'CBNData',
            'url': 'https://m.cbndata.com/information/295097',
            'content': '小红书针对批量运营的AI托管账号正式出手...',
            'date': '2026-03-13'
        },
        {
            'title': '腾讯2025年财报：营销服务全年收入达1450亿增19%',
            'source': 'QQ News',
            'url': 'https://news.qq.com/rain/a/20260318A083KU00',
            'content': '腾讯2025年营销服务收入1450亿元...',
            'date': '2026-03-18'
        },
        {
            'title': '快手2025磁力大会将于3月31日召开',
            'source': '新浪网',
            'url': 'https://test.com',
            'content': '快手宣布2025磁力大会...',
            'date': '2025-03-27'  # 旧新闻，会被降分
        }
    ]
    
    # 执行采集+筛选
    top_news = collector.collect_and_filter(
        google_results=google_results,
        min_score=40.0,  # 最低40分
        top_n=5
    )
    
    # 输出JSON
    print("\n" + "=" * 60)
    print("JSON输出（可用于后续处理）")
    print("=" * 60)
    print(json.dumps(top_news, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
