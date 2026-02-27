#!/bin/bash
# Lip 每日新闻定时任务脚本
# 每天凌晨2点自动运行

set -e

# 工作目录
WORKDIR="/home/admin/.openclaw/workspace/the-gallaghers/lip"
LOG_FILE="/tmp/lip_daily_news.log"

# 进入工作目录
cd "$WORKDIR"

# 记录开始时间
echo "================================================" >> "$LOG_FILE"
echo "🚀 Lip 每日新闻开始运行 - $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "================================================" >> "$LOG_FILE"

# 运行简化版每日新闻生成
echo "📰 生成每日学习新闻（简化版）..." >> "$LOG_FILE"
python3 simple_daily_news.py >> "$LOG_FILE" 2>&1

# 检查是否生成成功
if [ -f "daily_news_$(date '+%Y-%m-%d').txt" ]; then
    echo "✅ 每日新闻生成成功: daily_news_$(date '+%Y-%m-%d').txt" >> "$LOG_FILE"
    
    # 读取消息内容
    MESSAGE_CONTENT=$(cat "daily_news_$(date '+%Y-%m-%d').txt" | head -1000)
    
    # 自动发送飞书消息
    echo "📤 正在发送飞书消息..." >> "$LOG_FILE"
    /usr/bin/openclaw message send --channel feishu --target user:ou_7a6e5b696a98e618423c1dd1fbd21eef --message "$MESSAGE_CONTENT" >> "$LOG_FILE" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✅ 飞书消息发送成功" >> "$LOG_FILE"
    else
        echo "❌ 飞书消息发送失败" >> "$LOG_FILE"
    fi
    
    echo "📝 消息预览:" >> "$LOG_FILE"
    echo "$MESSAGE_CONTENT" | head -10 >> "$LOG_FILE"
    echo "..." >> "$LOG_FILE"
    
else
    echo "❌ 每日新闻生成失败" >> "$LOG_FILE"
fi

# 清理旧文件（保留最近7天）
echo "🧹 清理旧文件..." >> "$LOG_FILE"
find . -name "daily_news_*.md" -mtime +7 -delete >> "$LOG_FILE" 2>&1
find . -name "daily_news_*.txt" -mtime +7 -delete >> "$LOG_FILE" 2>&1
find . -name "feishu_message_*.txt" -mtime +7 -delete >> "$LOG_FILE" 2>&1
find . -name "channel_*_*.md" -mtime +7 -delete >> "$LOG_FILE" 2>&1

# 记录结束时间
echo "================================================" >> "$LOG_FILE"
echo "✅ Lip 每日新闻运行完成 - $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "================================================" >> "$LOG_FILE"

# 显示日志最后几行
tail -20 "$LOG_FILE"