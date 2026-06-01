#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KIM机器人推送脚本
每周一、周四上午11点自动推送商业化洞察到KIM群聊

Author: AI Assistant
Created: 2026-03-19
Updated: 2026-03-24 (调整为每周一、周四11:00推送)
"""

import sys
import os
# 确保 launchd 环境下也能找到用户级 site-packages（解决 PYTHONPATH 丢失问题）
_user_packages = os.path.expanduser('~/Library/Python/3.9/lib/python/site-packages')
if _user_packages not in sys.path:
    sys.path.insert(0, _user_packages)

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
        
        # 提取洞察内容 - 查找active面板中的今日洞察card
        insights = []
        # 优先查找 active 的 date-panel
        active_panel = soup.find('div', class_='date-panel active')
        if not active_panel:
            active_panel = soup  # 兜底：全文搜索
        
        insight_card = None
        for card in active_panel.find_all('div', class_='content-card'):
            if '今日洞察' in card.get_text():
                insight_card = card
                break
        
        if insight_card:
            # 查找所有洞察details
            details = insight_card.find_all('details', recursive=True)
            
            for detail in details:
                # 提取标题：新结构用 .company-summary-label，旧结构用 h4
                title_elem = detail.find(class_='company-summary-label')
                title = ""
                if title_elem:
                    title = title_elem.get_text().strip()
                else:
                    title_elem = detail.find('h4')
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
    
    markdown = f"""## 📈 今日商业化洞察 ({today} {weekday_zh})

> 数据更新时间：{update_date}

### 💡 今日核心洞察

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


def build_monthly_recap_message(data):
    """
    构造月度回顾的Markdown消息（5条精选洞察，手动触发）
    
    Args:
        data: dict，含 month_label（如"5月"）和 insights（list of {title, description}）
    Returns:
        str: Markdown格式消息
    """
    month_label = data.get('month_label', '本月')
    insights = data.get('insights', [])
    today = datetime.now().strftime('%Y-%m-%d')

    markdown = f"## 📊 {month_label}商业化重点外部洞察回顾\n\n"
    markdown += f"> 整理时间：{today}　|　覆盖区间：{month_label}\n\n"

    for i, insight in enumerate(insights, 1):
        title = insight['title']
        desc = insight['description']
        markdown += f"**{i}. {title}**\n{desc}\n\n"

    markdown += f"\n---\n\n[📊 查看完整洞察平台]({PLATFORM_URL})\n"
    markdown += "💬 更多竞对动态、行业趋势、深度分析请访问平台"

    return markdown


def push_monthly_recap():
    """
    月度回顾推送入口，手动触发（python3 kim_push.py --monthly）
    5条精选洞察硬编码于此，每月初更新一次。
    """
    logging.info("=" * 50)
    logging.info("开始执行月度回顾推送")
    logging.info("=" * 50)

    # ===== 5月精选洞察（每月初手动更新这里）=====
    MONTHLY_INSIGHTS = [
        {
            'title': '🎬 AI短剧行业两极分化：Q1上线12.8万部占比95%+，但爆款率仅0.12%——内容从"稀缺"进入"泛滥"，流量才是真护城河',
            'description': '钛媒体（5/23）+DataEye数据：2026Q1全行业上线微短剧12.8万部，AI占比超95%；但12.78万在播作品中播放破亿不足150部，爆款率仅0.12%——AI把产能天花板打穿，却让"流量分发权"更集中于平台手中，内容从"稀缺变现"转向"情绪付费+精准买量"双轮驱动。',
        },
        {
            'title': '🎮 AI重塑IAA小游戏：抖音Q1流水+80%、内容场+140%，"AI素材+托管投放"成新增长引擎，快手小游戏AI工具链建设刻不容缓',
            'description': '巨量引擎数据：2026Q1 IAA抖音小游戏流水+80%，内容场景流水+140%；AI素材ARPU较传统高50%+，AI托管后老游消耗翻5倍；内容获客+160%/社交获客+360%/搜索获客+210%——小游戏已从"买量驱动"转向"内容驱动+AI放大"的新增长范式。',
        },
        {
            'title': '🎮 微信小游戏月活破5亿，IAP首发"5000万免分成"加速平台生态密化',
            'description': '5月27日2026微信小游戏开发者大会：月活5亿+、DAU破百万游戏升至80款；推出四项让利政策——IAP新游首发5000万内不分成、IAA双分成（90%快回收/85%长留存）、PC小游戏专属广告金+10%；PC付费增长130%。平台进入"用让利换生态密度"的深水区。',
        },
        {
            'title': '🛒 抖音电商618结构性重组：千川划入电商、红果独立电商Tab、自营3C上线',
            'description': '抖音电商618背后是组织层面的深度重构：Q1九大扶持政策降本85亿（+57%）；商品卡免佣扩至直播+短视频全场；千川已划入电商部门，广告与GMV可联动决策；红果电商独立、首页嵌入商城Tab；自营3C覆盖北上广深。抖音正从"广告公司"向"多形态零售生态"进化。',
        },
        {
            'title': '🌸 内容平台618大促集体转向"情绪×AI"双驱模式：字节星图食饮大会+小红书种搜升级，内容消费进入"情绪价值变现"新阶段',
            'description': '巨量引擎食饮星图大会(5/8)：情绪内容在播放量/互动率/完播率全面领先，AI漫剧+明星AI授权价格降至传统1/10；小红书618公开课(5/9)：种草直达ROI保险+AI智能笔记0成本扩素材——内容平台集体确立"情绪锚点×AI工业化"双驱营销范式，达人营销正在经历AI重构。',
        },
    ]
    # =============================================

    data = {
        'month_label': '5月',
        'insights': MONTHLY_INSIGHTS,
    }

    markdown_msg = build_monthly_recap_message(data)
    logging.info(f"月度回顾消息内容:\n{markdown_msg}")

    success = send_to_kim(markdown_msg)
    if success:
        logging.info("✅ 月度回顾推送成功")
    else:
        logging.error("❌ 月度回顾推送失败")
    return success



    """读取上次推送日期（用于防止重复推送）"""
    state_file = os.path.join(script_dir, '.last_push_date')
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            return f.read().strip()
    return None


def save_push_date(script_dir):
    """记录今天已推送"""
    state_file = os.path.join(script_dir, '.last_push_date')
    today = datetime.now().strftime('%Y-%m-%d')
    with open(state_file, 'w') as f:
        f.write(today)


def already_pushed_today(script_dir):
    """检查今天是否已经推送过"""
    today = datetime.now().strftime('%Y-%m-%d')
    last = get_last_push_date(script_dir)
    if last == today:
        logging.info(f"⏭️  今天({today})已推送过，跳过")
        return True
    return False


def main(force=False):
    """
    主函数
    Args:
        force: 强制推送，忽略"今日已推送"检查（手动触发时用）
    """
    logging.info("=" * 50)
    logging.info("开始执行KIM推送任务")
    logging.info("=" * 50)

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 防重复推送检查（非强制模式下）
    if not force and already_pushed_today(script_dir):
        return True

    # 获取HTML文件路径
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
        save_push_date(script_dir)  # 记录今日已推送
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
    # 支持 --force 参数手动强制推送
    # 支持 --monthly 参数触发月度回顾推送
    if '--monthly' in sys.argv:
        success = push_monthly_recap()
    else:
        force = '--force' in sys.argv
        success = main(force=force)
    sys.exit(0 if success else 1)
