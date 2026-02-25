#!/bin/bash
# Lip 智能学习助手 - 启动脚本

cd /home/admin/.openclaw/workspace/the-gallaghers/lip

echo "🚀 启动 Lip 智能学习助手"
echo "=========================="

# 检查API服务器是否已运行
if curl -s http://localhost:8888/api/test > /dev/null 2>&1; then
    echo "✅ Web API 服务器已在运行"
else
    echo "🌐 启动 Web API 服务器..."
    nohup python web_api.py > /tmp/web_api.log 2>&1 &
    sleep 2
    if curl -s http://localhost:8888/api/test > /dev/null 2>&1; then
        echo "✅ Web API 启动成功 (http://localhost:8888)"
    else
        echo "❌ Web API 启动失败，查看日志: tail -f /tmp/web_api.log"
        exit 1
    fi
fi

echo ""
echo "📊 当前状态:"
curl -s http://localhost:8888/api/status | python3 -c "
import sys, json
data = json.load(sys.stdin)['data']
print(f\"  监控博主: {data['active_channels']}/{data['total_channels']}\")
print(f\"  视频进度: {data['analyzed_videos']}/{data['total_videos']} ({data['progress_percent']:.1f}%)\")
print(f\"  学习笔记: {data['total_notes']} 条\")
print(f\"  科普词条: {data['knowledge_count']} 条\")
"

echo ""
echo "📝 可用命令:"
echo "  查看日志:    tail -f /tmp/web_api.log"
echo "  停止API:     pkill -f 'python web_api.py'"
echo "  手动分析:    python cron_job.py"
echo "  运行测试:    python test_system.py"
echo ""
echo "🌐 Web面板: 打开 Gallagher 系统 → Lip → 智能学习助手"
echo ""
echo "按 Ctrl+C 退出此提示（API服务器将继续在后台运行）"
echo "=========================="