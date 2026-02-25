#!/bin/bash
# Lip 智能学习助手 - 安装配置脚本

set -e

echo "🚀 Lip 智能学习助手安装配置"
echo "=============================="

# 检查Python环境
echo "检查Python环境..."
python3 --version || { echo "❌ Python3未安装"; exit 1; }

# 检查yt-dlp
echo "检查yt-dlp..."
if ! command -v yt-dlp &> /dev/null; then
    echo "⚠️  yt-dlp未安装，尝试安装..."
    pip3 install --user yt-dlp || {
        echo "❌ 安装yt-dlp失败，请手动安装: pip3 install --user yt-dlp"
        exit 1
    }
else
    echo "✅ yt-dlp已安装"
fi

# 检查依赖
echo "检查Python依赖..."
pip3 list | grep -E "requests|python-dateutil" || {
    echo "安装requests和python-dateutil..."
    pip3 install --user requests python-dateutil
}

# 创建必要的目录
echo "创建目录结构..."
mkdir -p notebooks

# 初始化配置文件
if [ ! -f config.json ]; then
    echo "创建默认配置文件..."
    cat > config.json << EOF
{
  "version": "1.0",
  "max_channels": 10,
  "daily_limit_per_channel": 5,
  "channels": [],
  "settings": {
    "auto_sync_feishu": false,
    "auto_sync_notebooklm": false,
    "analysis_model": "kimi-k2.5",
    "proxy": null
  }
}
EOF
    echo "✅ 配置文件已创建"
else
    echo "✅ 配置文件已存在"
fi

# 测试系统
echo "运行系统测试..."
python3 test_system.py

# 设置文件权限
chmod +x cron_job.py

echo ""
echo "🎉 安装完成！"
echo ""
echo "📋 下一步操作："
echo "1. 在飞书中测试命令："
echo "   @Lip 添加博主 https://youtube.com/@channelname"
echo "   @Lip 状态"
echo ""
echo "2. 配置OpenClaw定时任务："
echo "   编辑OpenClaw配置，添加："
echo "   cron:"
echo "     lip_daily_analysis:"
echo "       schedule: \"0 2 * * *\""
echo "       command: \"python $(pwd)/cron_job.py\""
echo ""
echo "3. 访问Web面板："
echo "   打开 Gallagher 系统，选择 Lip 角色"
echo ""
echo "📚 详细文档请查看 README.md"