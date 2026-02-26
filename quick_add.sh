#!/bin/bash
# 快速添加视频脚本

echo "🚀 快速添加视频到笔记本"

# Joe Rogan笔记本
echo "📺 处理Joe Rogan笔记本..."
NOTEBOOK_ID="c9195c1b-02a5-4a7d-b4ca-5157a3068866"

# 切换到笔记本
~/.local/bin/notebooklm use $NOTEBOOK_ID

# 视频ID列表（从RSS获取的）
VIDEO_IDS=(
    "BvhFuEp55X0"
    "Dnon-AsWnOQ"
    "MkqDA9W4Vo0"
    "IbhDeUcZ_iw"
    "qFwiXyZHYbU"
    "y2SD_z61FRo"
    "CH5JoJ_-hic"
    "0sMrvv53e9Y"
    "UPfN2G0RyQM"
    "f_neykptZPY"
)

echo "📥 开始添加视频..."
for VIDEO_ID in "${VIDEO_IDS[@]}"; do
    echo "  添加: $VIDEO_ID"
    ~/.local/bin/notebooklm source add "https://www.youtube.com/watch?v=$VIDEO_ID"
    sleep 0.5
done

echo "✅ Joe Rogan笔记本视频添加完成"

# Lex Fridman笔记本
echo ""
echo "📺 处理Lex Fridman笔记本..."
NOTEBOOK_ID="0d369fcb-2f0a-40d6-a423-25928ad3375c"

# 切换到笔记本
~/.local/bin/notebooklm use $NOTEBOOK_ID

# 获取Lex Fridman视频
echo "  获取Lex Fridman视频..."
LEX_VIDEOS=$(curl -s "https://www.youtube.com/feeds/videos.xml?channel_id=UCSHZKyawb77ixDdsGog4iWA" | grep "yt:videoId" | head -10 | sed 's/.*<yt:videoId>//g' | sed 's/<\/yt:videoId>.*//g')

echo "📥 开始添加Lex Fridman视频..."
for VIDEO_ID in $LEX_VIDEOS; do
    echo "  添加: $VIDEO_ID"
    ~/.local/bin/notebooklm source add "https://www.youtube.com/watch?v=$VIDEO_ID"
    sleep 0.5
done

echo "✅ Lex Fridman笔记本视频添加完成"

echo ""
echo "🎉 两个笔记本视频添加完成！"