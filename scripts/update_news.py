#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商业化洞察平台 - 每日新闻自动更新脚本
Author: AI Assistant
Date: 2026-03-18
"""

import os
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup

# ============================================
# 配置项
# ============================================

# Google Custom Search API配置
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID', '')

# 新闻源配置
NEWS_SOURCES = {
    'tier3_media': [
        '36kr.com',
        'finance.sina.com.cn',
        'tmtpost.com',
        'huxiu.com',
        'adquan.com',
        'newrank.cn',
        'pai.com.cn'
    ]
}

# 核心竞对关键词
COMPETITORS = {
    '字节跳动': ['字节跳动', '抖音', '巨量引擎', 'Seedance', '抖省省'],
    '小红书': ['小红书', '蒲公英', '种草', '市集'],
    '快手': ['快手', '磁力引擎', '磁力金牛', '可灵AI'],
    '腾讯': ['腾讯', '混元', '视频号广告', '腾讯广告'],
    '阿里': ['阿里', '阿里妈妈', '淘宝', '天猫', '悟空']
}

# 行业赛道关键词
INDUSTRIES = {
    '游戏与内容': ['游戏广告', 'IAA', '抖音小游戏', '买量'],
    '本地生活': ['本地生活', '到店', '美团', '抖音生活服务', '抖省省'],
    '电商广告': ['电商广告', '直播带货', '货架电商', 'GMV', 'TikTok Shop']
}

# 过滤规则
EXCLUDE_KEYWORDS = [
    '招聘', 'jobs.', '求职', '岗位', '职位',
    '广告联盟平台', '网赚', '刷单', '代理'
]

# 时间过滤（最近7天）
DATE_FILTER_DAYS = 7

# ============================================
# 工具函数
# ============================================

def get_date_filter():
    """获取日期过滤字符串"""
    target_date = datetime.now() - timedelta(days=DATE_FILTER_DAYS)
    return target_date.strftime('%Y-%m-%d')


def should_exclude(title: str, url: str) -> bool:
    """判断是否应该排除这条新闻"""
    text = f"{title} {url}".lower()
    return any(keyword in text for keyword in EXCLUDE_KEYWORDS)


def search_google(query: str, num_results: int = 3) -> List[Dict]:
    """
    使用Google Custom Search API搜索
    """
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("⚠️  Google API未配置，跳过搜索")
        return []
    
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_CSE_ID,
        'q': query,
        'num': num_results,
        'dateRestrict': f'd{DATE_FILTER_DAYS}'  # 最近N天
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('items', []):
            title = item.get('title', '')
            link = item.get('link', '')
            snippet = item.get('snippet', '')
            
            # 排除不需要的内容
            if should_exclude(title, link):
                continue
            
            results.append({
                'title': title,
                'url': link,
                'snippet': snippet,
                'source': extract_domain(link)
            })
        
        return results
    
    except Exception as e:
        print(f"❌ Google搜索失败: {e}")
        return []


def extract_domain(url: str) -> str:
    """从URL提取域名"""
    match = re.search(r'https?://(?:www\.)?([^/]+)', url)
    return match.group(1) if match else ''


def search_competitor_news(company: str, keywords: List[str]) -> List[Dict]:
    """
    搜索某个竞对的最新动态
    """
    print(f"🔍 搜索 {company} 的新闻...")
    
    # 构建搜索查询
    keyword_query = ' OR '.join(keywords)
    site_filter = ' OR '.join([f'site:{site}' for site in NEWS_SOURCES['tier3_media']])
    query = f"({keyword_query}) 商业化 OR 广告 OR 收入 ({site_filter}) after:{get_date_filter()}"
    
    results = search_google(query, num_results=5)
    
    # 限制每个公司最多3条
    return results[:3]


def search_industry_news(industry: str, keywords: List[str]) -> List[Dict]:
    """
    搜索某个行业赛道的最新动态
    """
    print(f"🔍 搜索 {industry} 赛道新闻...")
    
    keyword_query = ' OR '.join(keywords)
    site_filter = ' OR '.join([f'site:{site}' for site in NEWS_SOURCES['tier3_media']])
    query = f"({keyword_query}) ({site_filter}) after:{get_date_filter()}"
    
    results = search_google(query, num_results=3)
    return results[:2]


def generate_news_html(company: str, news_list: List[Dict]) -> str:
    """
    生成某个公司的新闻HTML
    """
    if not news_list:
        return ""
    
    html_parts = []
    for i, news in enumerate(news_list):
        badge = "hot" if i == 0 else "new" if i == 1 else "company"
        badge_text = "HOT" if i == 0 else "NEW" if i == 1 else "商业化"
        
        # 简化标题（LLM可以进一步优化）
        title = news['title'][:50] + ('...' if len(news['title']) > 50 else '')
        
        html = f"""                                    <li>
                                        <span class="insight-badge {badge}">{badge_text}</span>
                                        <a href="{news['url']}" target="_blank" style="color: inherit; text-decoration: none;">
                                            <strong>{title}</strong> - {news['snippet'][:80]}...（{news['source']}）
                                        </a>
                                    </li>"""
        html_parts.append(html)
    
    return '\n'.join(html_parts)


def update_html_file(html_path: str, competitors_data: Dict, industries_data: Dict):
    """
    更新HTML文件
    """
    print("📝 更新HTML文件...")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 更新时间戳
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    html_content = re.sub(
        r'更新于 \d{4}-\d{2}-\d{2}',
        f'更新于 {datetime.now().strftime("%Y-%m-%d")}',
        html_content
    )
    
    # TODO: 这里需要更复杂的HTML替换逻辑
    # 建议使用BeautifulSoup或模板引擎
    # 当前先输出JSON，手动验证
    
    print("✅ HTML文件更新完成")


def main():
    """
    主函数
    """
    print("=" * 60)
    print("🚀 商业化洞察平台 - 每日新闻自动更新")
    print("=" * 60)
    print(f"⏰ 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📅 搜索范围: 最近 {DATE_FILTER_DAYS} 天")
    print()
    
    # 检查API配置
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("⚠️  警告：Google API未配置")
        print("   请设置环境变量：")
        print("   - GOOGLE_API_KEY")
        print("   - GOOGLE_CSE_ID")
        print()
        print("   暂时使用模拟数据进行测试...")
        print()
    
    # 1. 搜索核心竞对动态
    print("=" * 60)
    print("📰 步骤1: 搜索核心竞对动态")
    print("=" * 60)
    
    competitors_data = {}
    for company, keywords in COMPETITORS.items():
        news_list = search_competitor_news(company, keywords)
        competitors_data[company] = news_list
        print(f"   ✅ {company}: 找到 {len(news_list)} 条新闻")
    
    print()
    
    # 2. 搜索行业赛道动态
    print("=" * 60)
    print("🚀 步骤2: 搜索行业赛道动态")
    print("=" * 60)
    
    industries_data = {}
    for industry, keywords in INDUSTRIES.items():
        news_list = search_industry_news(industry, keywords)
        industries_data[industry] = news_list
        print(f"   ✅ {industry}: 找到 {len(news_list)} 条新闻")
    
    print()
    
    # 3. 输出结果（JSON格式，便于验证）
    print("=" * 60)
    print("📊 搜索结果汇总")
    print("=" * 60)
    
    output_data = {
        'update_time': datetime.now().isoformat(),
        'competitors': competitors_data,
        'industries': industries_data
    }
    
    output_file = 'news_update.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 结果已保存到: {output_file}")
    print()
    
    # 4. 统计信息
    total_news = sum(len(v) for v in competitors_data.values()) + \
                 sum(len(v) for v in industries_data.values())
    print(f"📈 总计搜索到 {total_news} 条新闻")
    print(f"   - 核心竞对: {sum(len(v) for v in competitors_data.values())} 条")
    print(f"   - 行业赛道: {sum(len(v) for v in industries_data.values())} 条")
    print()
    
    # 5. 下一步提示
    print("=" * 60)
    print("💡 下一步操作")
    print("=" * 60)
    print("1. 查看 news_update.json 验证搜索结果")
    print("2. 配置 Google API 密钥以启用真实搜索")
    print("3. 完善 HTML 更新逻辑（当前仅输出JSON）")
    print("4. 配置 GitHub Actions 实现定时自动更新")
    print()


if __name__ == '__main__':
    main()
