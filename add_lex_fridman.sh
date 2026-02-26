#!/bin/bash
echo "🚀 快速添加Lex Fridman视频"
echo "目标：50个视频"

# Lex Fridman视频ID（从RSS获取）
LEX_VIDEOS=(
    "KGVpKPNUdzA"
    "YFjfBk8HI5o"
    "EV7WhVT270Q"
    "Z-FRe5AKmCU"
    "14OPT6CcsH4"
    "_bBRVNkAfkQ"
    "Qp0rCU49lMs"
    "m_CFCyc2Shs"
    "o3gbXDjNWyI"
    "7OLVwZeMCfY"
    "qjPH9njnaVU"
    "SvKv7D4pBjE"
    "-Qm1_On71Oo"
    "HsLgZzgpz9Y"
    "jdCKiEJpwf4"
)

echo "📥 开始添加视频..."
COUNT=0
for VIDEO in "${LEX_VIDEOS[@]}"; do
    COUNT=$((COUNT + 1))
    echo "  [$COUNT/${#LEX_VIDEOS[@]}] 添加: $VIDEO"
    ~/.local/bin/notebooklm source add "https://www.youtube.com/watch?v=$VIDEO"
    sleep 0.3
done

echo "✅ Lex Fridman笔记本：已添加 $COUNT 个视频"