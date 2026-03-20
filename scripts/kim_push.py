#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KIM机器人推送脚本
每周一早上10点自动推送商业化洞察到KIM群聊

Author: AI Assistant
Created: 2026-03-19
"""

import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import sys
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kim_push.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# KIM机器人配置
KIM_ROBOT_KEY = "271996bf-7424-4c93-984f-21830b354394"
KIM_SEND_URL = f"https://kim-robot.kwaitalk.com/api/robot/send?key={KIM_ROBOT_KEY}"
# 如果是容器云部署，使用内网域名：
# KIM_SEND_URL = f"http://kim-robot.internal/api/robot/send?key={KIM_ROBOT_KEY}"

PLATFORM_URL = "https://ailiuliuliu.github.io/ad-insight-platform/"


def extract_insights_from_html(html_file_path):
    """
    从index.html中提取今日洞察内容
    
    Args:
        html_file_path: HTML文件路径
        
    Returns:
        dict: 包含标题和洞察列表的字典
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 提取更新日期
        update_date = "未知日期"
        # 查找包含"更新于"的p标签
        for p_tag in soup.find_all('p', class_='section-desc'):
            text = p_tag.get_text()
            if '更新于' in text:
                update_date = text.split('更新于')[-1].strip().rstrip('）')
                break
        
        # 提取洞察内容 - 查找第一个content-card（今日洞察）
        insights = []
        insight_card = soup.find('div', class_='content-card')
        
        if insight_card and '今日洞察' in insight_card.get_text():
            # 查找所有洞察details
            details = insight_card.find_all('details', recursive=True)
            
            for detail in details:
                # 提取标题
                title_elem = detail.find('h4')
                title = ""
                if title_elem:
                    title = title_elem.get_text().strip()
                
                # 提取描述
                desc_elem = detail.find('div', class_='company-summary-desc')
                description = ""
                if desc_elem:
                    description = desc_elem.get_text().strip()
                    # 清理多余空白
                    description = ' '.join(description.split())
                
                if title and description:
                    insights.append({
                        'title': title,
                        'description': description
                    })
        
        logging.info(f"提取到 {len(insights)} 条洞察，更新日期: {update_date}")
        
        return {
            'update_date': update_date,
            'insights': insights
        }
    
    except Exception as e:
        logging.error(f"提取洞察内容失败: {e}", exc_info=True)
        return None


def build_markdown_message(data):
    """
    构造Markdown格式的消息
    
    Args:
        data: 包含洞察数据的字典
        
    Returns:
        str: Markdown格式的消息内容
    """
    update_date = data.get('update_date', '未知')
    insights = data.get('insights', [])
    
    # 构造消息标题
    today = datetime.now().strftime('%Y-%m-%d')
    weekday = datetime.now().strftime('%A')
    weekday_zh = {
        'Monday': '周一',
        'Tuesday': '周二',
        'Wednesday': '周三',
        'Thursday': '周四',
        'Friday': '周五',
        'Saturday': '周六',
        'Sunday': '周日'
    }.get(weekday, weekday)
    
    markdown = f"""## 📈 商业化洞察周报 ({today} {weekday_zh})

> 数据更新时间：{update_date}

### 💡 本周核心洞察

"""
    
    # 添加洞察条目（最多3条）
    for i, insight in enumerate(insights[:3], 1):
        title = insight['title']
        desc = insight['description']
        markdown += f"**{i}. {title}**\n"
        markdown += f"{desc}\n\n"
    
    # 添加查看链接
    markdown += f"\n---\n\n[📊 查看完整洞察平台]({PLATFORM_URL})\n"
    markdown += f"💬 更多竞对动态、行业趋势、深度分析请访问平台"
    
    return markdown


def send_to_kim(markdown_content):
    """
    发送消息到KIM群聊
    
    Args:
        markdown_content: Markdown格式的消息内容
        
    Returns:
        bool: 是否发送成功
    """
    try:
        send_json = {
            'msgtype': 'markdown',
            'markdown': {
                'content': markdown_content
            }
        }
        
        logging.info(f"发送消息到KIM: {KIM_SEND_URL}")
        response = requests.post(KIM_SEND_URL, json=send_json, timeout=10)
        
        result = response.json()
        logging.info(f"KIM响应: {result}")
        
        # 检查是否成功（messageKey非空即为成功）
        if result.get('messageKey'):
            logging.info("✅ 消息发送成功")
            return True
        else:
            logging.error(f"❌ 消息发送失败: {result.get('errmsg', '未知错误')}")
            return False
            
    except Exception as e:
        logging.error(f"❌ 发送失败: {e}")
        return False


def main():
    """主函数"""
    logging.info("=" * 50)
    logging.info("开始执行KIM推送任务")
    logging.info("=" * 50)
    
    # 获取HTML文件路径（相对于脚本的上级目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(script_dir, '..', 'index.html')
    
    if not os.path.exists(html_file):
        logging.error(f"❌ 找不到HTML文件: {html_file}")
        return False
    
    # 提取洞察内容
    logging.info("正在提取洞察内容...")
    data = extract_insights_from_html(html_file)
    
    if not data or not data.get('insights'):
        logging.error("❌ 未能提取到洞察内容")
        return False
    
    logging.info(f"✅ 成功提取 {len(data['insights'])} 条洞察")
    
    # 构造消息
    logging.info("正在构造Markdown消息...")
    markdown_msg = build_markdown_message(data)
    logging.info(f"消息内容:\n{markdown_msg}")
    
    # 发送到KIM
    logging.info("正在发送到KIM...")
    success = send_to_kim(markdown_msg)
    
    if success:
        logging.info("=" * 50)
        logging.info("✅ KIM推送任务执行成功")
        logging.info("=" * 50)
        return True
    else:
        logging.error("=" * 50)
        logging.error("❌ KIM推送任务执行失败")
        logging.error("=" * 50)
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
