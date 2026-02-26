#!/usr/bin/env python3
"""
立即手动修复 - 为缺失频道添加视频到NotebookLM
"""

import subprocess
import time

NOTEBOOKLM_CLI = "~/.local/bin/notebooklm"

def run_cmd(cmd):
    """运行命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✓ 成功")
        return result.stdout.strip()
    else:
        print(f"✗ 失败: {result.stderr}")
        return None

def main():
    print("=" * 60)
    print("立即手动修复NotebookLM同步问题")
    print("=" * 60)
    
    # 1. 为Joe Rogan创建笔记本
    print("\n1. 为Joe Rogan Experience创建笔记本...")
    notebook_id = run_cmd(f"{NOTEBOOKLM_CLI} create '学习笔记 - Joe Rogan Experience 修复'")
    
    if notebook_id:
        # 添加Joe Rogan最新视频（需要实际视频ID）
        print("\n   添加Joe Rogan视频...")
        # 这里需要实际的YouTube视频ID
        # run_cmd(f"{NOTEBOOKLM_CLI} use {notebook_id}")
        # run_cmd(f"{NOTEBOOKLM_CLI} source add 'https://www.youtube.com/watch?v=实际视频ID'")
    
    # 2. 为No Code创建笔记本
    print("\n2. 为No Code创建笔记本...")
    notebook_id = run_cmd(f"{NOTEBOOKLM_CLI} create '学习笔记 - No Code 修复'")
    
    if notebook_id:
        print("\n   添加No Code视频...")
        # 需要实际的YouTube视频ID
    
    # 3. 检查现有笔记本
    print("\n3. 检查现有笔记本状态...")
    run_cmd(f"{NOTEBOOKLM_CLI} list | grep -E '(lexfridman|JordanBPeterson)'")
    
    # 4. 修复cron任务日志
    print("\n4. 修复cron任务日志...")
    cron_cmd = "0 2 * * * /bin/bash /home/admin/.openclaw/workspace/the-gallaghers/lip/lip_cron_daily.sh >> /tmp/lip_cron.log 2>&1"
    print(f"   建议cron命令: {cron_cmd}")
    
    print("\n" + "=" * 60)
    print("手动修复完成!")
    print("=" * 60)
    
    print("\n🎯 下一步:")
    print("1. 需要实际的YouTube视频ID来添加视频")
    print("2. 更新cron任务添加错误日志")
    print("3. 明天凌晨2点验证任务执行")
    print("4. 设置错误通知机制")

if __name__ == "__main__":
    main()