#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商业化洞察平台 - 旧新闻批处理文件清理脚本
作者：AI助手
创建时间：2026-03-30
版本：v1.0

功能：清理14天前的news_batch_*.py文件
执行时机：每次更新平台时自动执行
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path

def clean_old_batch_files(script_dir: str = None, days: int = 14, dry_run: bool = False):
    """
    清理旧的news_batch文件
    
    Args:
        script_dir: 脚本目录路径，默认为当前目录
        days: 保留天数，默认14天
        dry_run: 是否仅预览不执行，默认False
        
    Returns:
        删除的文件列表
    """
    if script_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 计算截止日期
    cutoff_date = datetime.now() - timedelta(days=days)
    cutoff_str = cutoff_date.strftime('%Y%m%d')
    
    # 查找所有news_batch文件
    pattern = re.compile(r'news_batch_(\d{8})\.py$')
    deleted_files = []
    
    print(f"\n{'='*60}")
    print(f"清理旧新闻批处理文件（保留{days}天）")
    print(f"{'='*60}")
    print(f"截止日期：{cutoff_date.strftime('%Y-%m-%d')} ({cutoff_str})")
    print(f"扫描目录：{script_dir}")
    print(f"{'='*60}\n")
    
    for filename in os.listdir(script_dir):
        match = pattern.match(filename)
        if match:
            file_date_str = match.group(1)
            file_date = datetime.strptime(file_date_str, '%Y%m%d')
            file_path = os.path.join(script_dir, filename)
            
            if file_date < cutoff_date:
                if dry_run:
                    print(f"[预览] 将删除: {filename} ({file_date.strftime('%Y-%m-%d')})")
                else:
                    try:
                        os.remove(file_path)
                        deleted_files.append(filename)
                        print(f"✅ 已删除: {filename} ({file_date.strftime('%Y-%m-%d')})")
                    except Exception as e:
                        print(f"❌ 删除失败: {filename} - {str(e)}")
            else:
                print(f"⏸️  保留: {filename} ({file_date.strftime('%Y-%m-%d')})")
    
    print(f"\n{'='*60}")
    if dry_run:
        print(f"预览模式：共发现 {len(deleted_files)} 个文件待删除")
    else:
        print(f"清理完成：共删除 {len(deleted_files)} 个文件")
    print(f"{'='*60}\n")
    
    return deleted_files


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='清理旧的news_batch文件')
    parser.add_argument(
        '--dir',
        type=str,
        default=None,
        help='脚本目录路径，默认为当前目录'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=14,
        help='保留天数，默认14天'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='仅预览不执行'
    )
    
    args = parser.parse_args()
    
    deleted_files = clean_old_batch_files(
        script_dir=args.dir,
        days=args.days,
        dry_run=args.dry_run
    )
    
    return len(deleted_files)


if __name__ == '__main__':
    exit(main())
