#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开机/唤醒补推脚本
逻辑：如果今天是周一或周四，且当前时间 >= 11:00，且今天还没推过 → 补推
由 com.ad-insight.wakeup-check.plist 在每次系统唤醒/登录时触发

Author: AI Assistant
Created: 2026-04-20
"""

import sys
import os
import time
import logging
from datetime import datetime

# 日志路径与 kim_push.py 一致
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, 'kim_push.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

# 推送日的 weekday 编号（Python datetime：0=周一, 3=周四）
PUSH_WEEKDAYS = {0: '周一', 3: '周四'}
PUSH_HOUR = 11  # 推送时间：11点之后才补推


def should_push():
    """判断是否需要补推"""
    now = datetime.now()
    weekday = now.weekday()  # 0=Mon ... 6=Sun
    hour = now.hour

    if weekday not in PUSH_WEEKDAYS:
        logging.info(f"[wakeup] 今天是{now.strftime('%A')}，非推送日，跳过")
        return False

    if hour < PUSH_HOUR:
        logging.info(f"[wakeup] 现在 {hour}:{now.minute:02d}，未到推送时间({PUSH_HOUR}:00)，跳过")
        return False

    # 检查今天是否已推送
    state_file = os.path.join(script_dir, '.last_push_date')
    today_str = now.strftime('%Y-%m-%d')
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            last = f.read().strip()
        if last == today_str:
            logging.info(f"[wakeup] 今天({today_str})已推送过，跳过")
            return False

    logging.info(f"[wakeup] {PUSH_WEEKDAYS[weekday]} {now.strftime('%H:%M')}，需要补推")
    return True


def main():
    logging.info("[wakeup] === 开机/唤醒检查触发 ===")

    # 系统唤醒后网络可能还没就绪，等待 15 秒
    time.sleep(15)

    if not should_push():
        return

    logging.info("[wakeup] 满足补推条件，调用 kim_push.py ...")

    # 动态 import kim_push 并调用 main()
    sys.path.insert(0, script_dir)
    import kim_push
    kim_push.main(force=False)  # force=False：内部仍会做防重复检查


if __name__ == '__main__':
    main()
