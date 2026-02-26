#!/bin/bash
# 验证修复脚本

echo "=========================================="
echo "Lip系统修复验证 - $(date)"
echo "=========================================="

echo ""
echo "1. 检查cron任务..."
crontab -l | grep lip

echo ""
echo "2. 检查日志文件..."
if [ -f /tmp/lip_cron.log ]; then
    echo "日志文件存在: /tmp/lip_cron.log"
    echo "最后10行:"
    tail -10 /tmp/lip_cron.log
else
    echo "日志文件不存在（任务还未运行）"
fi

echo ""
echo "3. 检查NotebookLM状态..."
~/.local/bin/notebooklm list | grep -E "(lexfridman|Jordan|Rogan|No Code)" | head -5

echo ""
echo "4. 检查Lip脚本..."
ls -la /home/admin/.openclaw/workspace/the-gallaghers/lip/*.py | head -5

echo ""
echo "5. 检查配置文件..."
if [ -f /home/admin/.openclaw/workspace/the-gallaghers/lip/config.json ]; then
    echo "配置文件存在"
    active_channels=$(grep -c '"status": "active"' /home/admin/.openclaw/workspace/the-gallaghers/lip/config.json)
    echo "活跃频道数: $active_channels"
fi

echo ""
echo "=========================================="
echo "验证完成!"
echo "=========================================="
echo ""
echo "🎯 监控建议:"
echo "1. 明天凌晨2点后检查 /tmp/lip_cron.log"
echo "2. 验证NotebookLM是否有新内容"
echo "3. 检查是否收到飞书消息"
echo ""
echo "📞 如果任务失败，请检查:"
echo "   - Python版本兼容性"
echo "   - YouTube RSS可用性"
echo "   - NotebookLM API限制"