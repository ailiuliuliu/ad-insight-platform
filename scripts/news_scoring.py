#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商业化洞察平台 - 新闻自动化评分系统
作者：AI助手
创建时间：2026-03-30
版本：v1.0

评分标准：
- 时效性（40分）：当月40分、上月30分、更早20分
- 相关性（40分）：直接竞对40分、行业趋势35分、通用动态30分
- 权威性（20分）：官方20分、主流媒体15分、行业报道10分
- 总分>=85分：必选；70-84分：候选；<70分：不选
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import re

class NewsScorer:
    """新闻评分器"""
    
    def __init__(self, current_date: str = None):
        """
        初始化评分器
        
        Args:
            current_date: 当前日期，格式YYYY-MM-DD，默认为今天
        """
        if current_date:
            self.current_date = datetime.strptime(current_date, '%Y-%m-%d')
        else:
            self.current_date = datetime.now()
        
        self.current_month = self.current_date.strftime('%Y-%m')
        self.last_month = (self.current_date - timedelta(days=30)).strftime('%Y-%m')
    
    def score_timeliness(self, news_date: str) -> Tuple[int, str]:
        """
        时效性评分（40分）
        
        Args:
            news_date: 新闻日期，格式YYYY-MM-DD
            
        Returns:
            (分数, 评分说明)
        """
        try:
            date_obj = datetime.strptime(news_date, '%Y-%m-%d')
            news_month = date_obj.strftime('%Y-%m')
            
            if news_month == self.current_month:
                return (40, f"当月最新({news_month})")
            elif news_month == self.last_month:
                return (30, f"上月({news_month})")
            else:
                return (20, f"较早({news_month})")
        except:
            return (0, "日期格式错误")
    
    def score_relevance(self, title: str, summary: str = "") -> Tuple[int, str]:
        """
        相关性评分（40分）
        
        Args:
            title: 新闻标题
            summary: 新闻摘要（可选）
            
        Returns:
            (分数, 评分说明)
        """
        text = title + " " + summary
        
        # 直接涉及快手商业化竞对：40分
        direct_keywords = [
            '字节', '抖音', '巨量', '豆包', 'Seedance',
            '腾讯', '视频号', '获客宝', '混元',
            '小红书', '种草', 'WILL',
            '可灵', 'AI视频', '漫剧', '短剧'
        ]
        if any(kw in text for kw in direct_keywords):
            return (40, "直接涉及快手竞对")
        
        # 行业趋势影响快手：35分
        trend_keywords = [
            'AI购物', 'AIGC', '本地生活', '直播带货', '电商',
            '内容消费', '广告投放', '商业化', 'ROI', 'GMV'
        ]
        if any(kw in text for kw in trend_keywords):
            return (35, "行业趋势影响快手")
        
        # 通用行业动态：30分
        return (30, "通用行业动态")
    
    def score_authority(self, source: str, url: str = "") -> Tuple[int, str]:
        """
        权威性评分（20分）
        
        Args:
            source: 新闻来源
            url: 新闻链接（可选）
            
        Returns:
            (分数, 评分说明)
        """
        # 官方发布/财报：20分
        official_keywords = [
            '财报', '官方', '公告', 'oceanengine.com', 'e.qq.com',
            '巨量学', '腾讯广告', '磁力引擎', 'support.oceanengine'
        ]
        if any(kw in source or kw in url for kw in official_keywords):
            return (20, "官方发布/财报")
        
        # 主流媒体：15分
        mainstream_keywords = [
            '21财经', '36氪', '钛媒体', '新华网', '人民日报',
            '证券时报', '财联社', '界面新闻', '中新网'
        ]
        if any(kw in source for kw in mainstream_keywords):
            return (15, "主流媒体")
        
        # 行业报道：10分
        return (10, "行业报道")
    
    def score_news(self, news: Dict) -> Dict:
        """
        对单条新闻进行综合评分
        
        Args:
            news: 新闻字典，包含title、date、source、summary、url等字段
            
        Returns:
            评分结果字典，包含各维度分数和总分
        """
        # 时效性评分
        timeliness_score, timeliness_reason = self.score_timeliness(news.get('date', ''))
        
        # 相关性评分
        relevance_score, relevance_reason = self.score_relevance(
            news.get('title', ''),
            news.get('summary', '')
        )
        
        # 权威性评分
        authority_score, authority_reason = self.score_authority(
            news.get('source', ''),
            news.get('url', '')
        )
        
        # 总分
        total_score = timeliness_score + relevance_score + authority_score
        
        # 评级
        if total_score >= 85:
            grade = "必选"
        elif total_score >= 70:
            grade = "候选"
        else:
            grade = "不选"
        
        return {
            'title': news.get('title', ''),
            'date': news.get('date', ''),
            'source': news.get('source', ''),
            'url': news.get('url', ''),
            'summary': news.get('summary', ''),
            'scores': {
                'timeliness': {
                    'score': timeliness_score,
                    'reason': timeliness_reason
                },
                'relevance': {
                    'score': relevance_score,
                    'reason': relevance_reason
                },
                'authority': {
                    'score': authority_score,
                    'reason': authority_reason
                }
            },
            'total_score': total_score,
            'grade': grade
        }
    
    def batch_score(self, news_list: List[Dict]) -> List[Dict]:
        """
        批量评分并排序
        
        Args:
            news_list: 新闻列表
            
        Returns:
            评分后的新闻列表（按总分降序）
        """
        scored_list = [self.score_news(news) for news in news_list]
        scored_list.sort(key=lambda x: x['total_score'], reverse=True)
        return scored_list
    
    def filter_by_grade(self, scored_list: List[Dict], min_grade: str = "候选") -> List[Dict]:
        """
        按评级筛选新闻
        
        Args:
            scored_list: 评分后的新闻列表
            min_grade: 最低评级，可选"必选"、"候选"、"不选"
            
        Returns:
            筛选后的新闻列表
        """
        grade_order = {"必选": 3, "候选": 2, "不选": 1}
        min_level = grade_order.get(min_grade, 2)
        
        return [
            news for news in scored_list
            if grade_order.get(news['grade'], 0) >= min_level
        ]
    
    def print_scores(self, scored_list: List[Dict], top_n: int = None):
        """
        打印评分结果
        
        Args:
            scored_list: 评分后的新闻列表
            top_n: 只打印前N条，None表示全部打印
        """
        display_list = scored_list[:top_n] if top_n else scored_list
        
        print("\n" + "="*80)
        print(f"{'排名':<4} {'总分':<6} {'评级':<6} {'时效':<6} {'相关':<6} {'权威':<6} {'标题'}")
        print("="*80)
        
        for idx, news in enumerate(display_list, 1):
            scores = news['scores']
            print(f"{idx:<4} {news['total_score']:<6} {news['grade']:<6} "
                  f"{scores['timeliness']['score']:<6} "
                  f"{scores['relevance']['score']:<6} "
                  f"{scores['authority']['score']:<6} "
                  f"{news['title'][:50]}")
            print(f"     日期: {news['date']} | 来源: {news['source']}")
            print(f"     时效: {scores['timeliness']['reason']} | "
                  f"相关: {scores['relevance']['reason']} | "
                  f"权威: {scores['authority']['reason']}")
            print("-"*80)


def demo():
    """演示用例"""
    
    # 示例新闻数据
    news_list = [
        {
            'title': '快手可灵AI实现3亿美元ARR，押注AIGC作为第二增长曲线',
            'date': '2026-03-27',
            'source': '21财经',
            'url': 'https://www.21jingji.com/article/...',
            'summary': 'Sora关停当日公布成绩，2026年有望收入翻倍，对标字节Seedance 2.0'
        },
        {
            'title': '豆包开启AI购物内测，MAU 2.26亿领先行业',
            'date': '2026-03-20',
            'source': '21财经',
            'url': 'https://www.21jingji.com/article/...',
            'summary': '用户可在豆包APP内完成商品浏览、下单、支付全流程，AI对话式购物重构流量分发'
        },
        {
            'title': '腾讯2025年营销服务收入达1450亿增19%',
            'date': '2026-03-18',
            'source': '腾讯财报',
            'url': 'https://static.www.tencent.com/...',
            'summary': '视频号广告投放需求持续增加，围绕素材供给、行业化能力及经营优化持续推进'
        },
        {
            'title': '腾讯、网易、米哈游、B站春招启动，开放超10000个游戏岗位',
            'date': '2026-03-08',
            'source': 'QQ News',
            'url': 'https://news.qq.com/...',
            'summary': 'GDC26多家厂商大佬参会，游戏行业人才需求旺盛'
        },
        {
            'title': '美团年亏234亿，抖音本地生活2026目标超越美团',
            'date': '2026-03-28',
            'source': '钛媒体',
            'url': 'https://www.tmtpost.com/...',
            'summary': '抖音2月推出"抖省省"APP布局本地生活，美团护城河受到质疑'
        }
    ]
    
    # 创建评分器
    scorer = NewsScorer(current_date='2026-03-30')
    
    # 批量评分
    scored_list = scorer.batch_score(news_list)
    
    # 打印结果
    scorer.print_scores(scored_list)
    
    # 筛选必选和候选新闻
    print("\n" + "="*80)
    print("筛选结果：必选+候选新闻")
    print("="*80)
    filtered_list = scorer.filter_by_grade(scored_list, min_grade="候选")
    scorer.print_scores(filtered_list)
    
    # Top 3用于今日洞察
    print("\n" + "="*80)
    print("Top 3（用于今日洞察）")
    print("="*80)
    top3 = scored_list[:3]
    for idx, news in enumerate(top3, 1):
        print(f"\n洞察{idx}：{news['title']}")
        print(f"总分：{news['total_score']} | 评级：{news['grade']}")


if __name__ == '__main__':
    demo()
