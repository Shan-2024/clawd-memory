#!/usr/bin/env python3
"""
快速为所有笔记本添加视频
"""

import subprocess
import time

# 笔记本和频道映射
NOTEBOOKS = [
    # (笔记本ID, 频道ID, 博主名称)
    ("c9195c1b-02a5-4a7d-b4ca-5157a3068866", "UCzQUP1qoWDoEbmsQxvdjxgQ", "Joe Rogan"),
    ("b3cddb87-d31e-485c-8e58-46c8f14356a9", "UCWY4H8r9hM4HlGjCk31Q_6g", "The Diary Of A CEO"),
    ("93d167df-40b4-4ae7-b2f8-6831d3949aba", "UCWY4H8r9hM4HlGjCk31Q_6g", "Dwarkesh Patel"),
    ("a1d2b069-69ec-4680-b1de-606fffba98e1", "UCWY4H8r9hM4HlGjCk31Q_6g", "No Code"),
    ("7b3c37a2-495f-447e-a62a-2a3d78d5c28d", "UCWY4H8r9hM4HlGjCk31Q_6g", "Matthew Berman"),
    ("027eb501-5236-4727-a34a-0d97ca160b29", "UCWY4H8r9hM4HlGjCk31Q_6g", "Futurepedia"),
    ("2d8dbf59-a36a-4292-947b-fe5eaf016657", "UCWY4H8r9hM4HlGjCk31Q_6g", "AI Foundations"),
    ("1897fe16-24ac-49ed-905e-ae1e3244e423", "UCWY4H8r9hM4HlGjCk31Q_6g", "Jack"),
    ("a160580f-fa3d-4277-bc91-cd7dd6f3c09d", "UCjc1vfduI7BhVMXBLJLDjmA", "未知频道"),
]

def get_video_ids(channel_id, count=10):
    """获取频道最新视频ID"""
    import xml.etree.ElementTree as ET
    import urllib.request
    
    try:
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        response = urllib.request.urlopen(rss_url)
        xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        video_ids = []
        
        # 查找所有videoId元素
        for elem in root.iter('{http://www.youtube.com/xml/schemas/2015}videoId'):
            if len(video_ids) < count:
                video_ids.append(elem.text)
        
        return video_ids
    except Exception as e:
        print(f"获取视频ID失败: {e}")
        return []

def add_videos(notebook_id, video_ids):
    """添加视频到笔记本"""
    success = 0
    for video_id in video_ids:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # 切换到笔记本
        cmd1 = f"~/.local/bin/notebooklm use {notebook_id}"
        result1 = subprocess.run(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        if result1.returncode != 0:
            print(f"切换笔记本失败: {result1.stderr}")
            continue
        
        # 添加视频
        cmd2 = f'~/.local/bin/notebooklm source add "{video_url}"'
        result2 = subprocess.run(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        if result2.returncode == 0:
            success += 1
            print(f"  ✅ 添加: {video_id}")
        else:
            print(f"  ⚠️ 失败: {video_id} - {result2.stderr[:50]}")
        
        time.sleep(1)  # 避免请求过快
    
    return success

def main():
    print("🚀 快速填充所有笔记本")
    print("=" * 50)
    
    total_added = 0
    for notebook_id, channel_id, channel_name in NOTEBOOKS:
        print(f"\n📺 处理: {channel_name}")
        
        # 获取视频ID
        print(f"  获取最新视频...")
        video_ids = get_video_ids(channel_id, 10)  # 先获取10个
        
        if not video_ids:
            print(f"  ❌ 无法获取视频ID")
            continue
        
        print(f"  找到 {len(video_ids)} 个视频")
        
        # 添加视频
        added = add_videos(notebook_id, video_ids)
        total_added += added
        
        print(f"  📊 成功添加: {added}/{len(video_ids)}")
        
        # 延迟
        time.sleep(3)
    
    print(f"\n" + "=" * 50)
    print(f"🎉 完成! 总共添加 {total_added} 个视频")
    
    # 输出链接
    print(f"\n🔗 笔记本链接:")
    for notebook_id, _, channel_name in NOTEBOOKS:
        print(f"  📚 {channel_name}: https://notebooklm.google.com/notebook/{notebook_id}")

if __name__ == "__main__":
    main()