#!/bin/bash
echo "🚀 快速添加Joe Rogan视频"
echo "当前笔记本: 学习笔记 - Joe Rogan Experience"

# 视频ID列表
VIDEOS=(
    "huJVFuLmpd0"
    "ZyG8FSeTFKA"
    "4lmiRzROTZg"
    "lin3c35IyB0"
    "Sbh7ymCkjuM"
    "f_neykptZPY"
    "qFwiXyZHYbU"
    "y2SD_z61FRo"
    "CH5JoJ_-hic"
    "0sMrvv53e9Y"
    "UPfN2G0RyQM"
    "BvhFuEp55X0"
    "Dnon-AsWnOQ"
    "MkqDA9W4Vo0"
    "IbhDeUcZ_iw"
)

echo "📥 开始添加视频..."
for VIDEO in "${VIDEOS[@]}"; do
    echo "  添加: $VIDEO"
    ~/.local/bin/notebooklm source add "https://www.youtube.com/watch?v=$VIDEO"
    sleep 0.2
done

echo "✅ Joe Rogan笔记本视频添加完成"