#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KIM Webhook服务 - 接收KIM消息触发平台更新

部署到快手内网容器云，监听KIM机器人消息
当收到"更新平台"指令时，自动执行更新流程

Author: AI Assistant
Created: 2026-03-20
"""

from flask import Flask, request, jsonify
import requests
import json
import subprocess
import logging
import os
from datetime import datetime
import threading

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('webhook.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

# KIM机器人配置
KIM_ROBOT_KEY = os.getenv('KIM_ROBOT_KEY', '271996bf-7424-4c93-984f-21830b354394')
KIM_SEND_URL = f"https://kim-robot.kwaitalk.com/api/robot/send?key={KIM_ROBOT_KEY}"

# 更新脚本路径
UPDATE_SCRIPT = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'update_platform.py')

# 权限控制：允许触发更新的用户（username或user_id）
ALLOWED_USERS = os.getenv('ALLOWED_USERS', 'litianyu6,litianyu03').split(',')


def send_kim_message(content):
    """发送消息到KIM"""
    try:
        send_json = {
            'msgtype': 'markdown',
            'markdown': {
                'content': content
            }
        }
        response = requests.post(KIM_SEND_URL, json=send_json, timeout=10)
        result = response.json()
        logging.info(f"KIM消息发送结果: {result}")
        return result.get('success', False)
    except Exception as e:
        logging.error(f"发送KIM消息失败: {e}")
        return False


def execute_update():
    """
    执行平台更新流程
    在后台线程中运行，避免阻塞webhook响应
    """
    try:
        logging.info("=" * 50)
        logging.info("开始执行平台更新流程")
        logging.info("=" * 50)
        
        # 发送开始通知
        send_kim_message("🚀 **平台更新已启动**\n\n正在执行：\n1. 搜索最新商业化资讯\n2. AI分析生成洞察\n3. 更新HTML页面\n4. 推送到GitHub\n\n预计需要2-3分钟，请稍候...")
        
        # 执行更新脚本
        result = subprocess.run(
            ['python3', UPDATE_SCRIPT],
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )
        
        if result.returncode == 0:
            logging.info("✅ 平台更新成功")
            success_msg = f"""## ✅ 平台更新完成

**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**执行结果**: 成功

### 📊 更新内容
- ✅ 搜索最新商业化资讯
- ✅ AI生成核心洞察
- ✅ 更新HTML页面
- ✅ 推送到GitHub

[🔗 查看更新后的平台](https://ailiuliuliu.github.io/ad-insight-platform/)

---
💡 提示：页面部署可能需要1-2分钟，请稍后刷新查看
"""
            send_kim_message(success_msg)
        else:
            error_output = result.stderr[:500]  # 只取前500字符
            logging.error(f"❌ 平台更新失败: {error_output}")
            error_msg = f"""## ❌ 平台更新失败

**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**错误信息**:
```
{error_output}
```

请联系管理员检查日志
"""
            send_kim_message(error_msg)
            
    except subprocess.TimeoutExpired:
        logging.error("❌ 更新超时（5分钟）")
        send_kim_message("## ⏰ 更新超时\n\n更新流程执行超过5分钟，已自动终止\n请联系管理员检查")
    except Exception as e:
        logging.error(f"❌ 更新过程异常: {e}")
        send_kim_message(f"## ❌ 更新异常\n\n{str(e)}\n\n请联系管理员检查")


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'kim-webhook'
    })


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    KIM Webhook接口
    
    接收KIM机器人消息，判断是否触发更新
    """
    try:
        data = request.get_json()
        logging.info(f"收到webhook请求: {json.dumps(data, ensure_ascii=False)}")
        
        # 解析消息内容
        msg_type = data.get('msgtype', '')
        
        # 获取消息文本
        content = ""
        if msg_type == 'text':
            content = data.get('text', {}).get('content', '')
        elif msg_type == 'markdown':
            content = data.get('markdown', {}).get('content', '')
        
        # 获取发送者信息
        sender = data.get('sender', {})
        sender_username = sender.get('username', '')
        sender_name = sender.get('name', '')
        
        logging.info(f"消息内容: {content}")
        logging.info(f"发送者: {sender_username} ({sender_name})")
        
        # 权限检查
        if sender_username not in ALLOWED_USERS:
            logging.warning(f"⚠️  未授权用户尝试触发更新: {sender_username}")
            send_kim_message(f"⚠️ 抱歉，用户 @{sender_username} 没有权限触发更新\n\n如需开通权限，请联系管理员")
            return jsonify({'status': 'unauthorized', 'message': '无权限'}), 403
        
        # 判断是否包含更新指令
        update_keywords = ['更新平台', '更新洞察', 'update', '刷新平台']
        should_update = any(keyword in content.lower() for keyword in update_keywords)
        
        if should_update:
            logging.info("🎯 触发平台更新")
            # 在后台线程执行更新，立即返回响应
            threading.Thread(target=execute_update, daemon=True).start()
            
            return jsonify({
                'status': 'triggered',
                'message': '更新已触发',
                'timestamp': datetime.now().isoformat()
            })
        else:
            logging.info("💬 普通消息，不触发更新")
            return jsonify({
                'status': 'ignored',
                'message': '未匹配更新指令'
            })
            
    except Exception as e:
        logging.error(f"❌ Webhook处理异常: {e}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/trigger', methods=['POST'])
def manual_trigger():
    """
    手动触发接口（用于测试）
    
    使用方法：
    curl -X POST http://localhost:5000/trigger \
         -H "Content-Type: application/json" \
         -d '{"user": "litianyu6"}'
    """
    try:
        data = request.get_json() or {}
        user = data.get('user', 'unknown')
        
        if user not in ALLOWED_USERS:
            return jsonify({'status': 'unauthorized'}), 403
        
        logging.info(f"🎯 手动触发更新 (用户: {user})")
        threading.Thread(target=execute_update, daemon=True).start()
        
        return jsonify({
            'status': 'triggered',
            'message': '更新已触发',
            'user': user
        })
    except Exception as e:
        logging.error(f"❌ 手动触发异常: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    # 生产环境建议使用 gunicorn 启动
    # gunicorn -w 4 -b 0.0.0.0:8080 app:app
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
