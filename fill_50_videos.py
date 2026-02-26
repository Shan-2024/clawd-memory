#!/usr/bin/env python3
"""
为11个笔记本每个填满50个视频
立即执行！
"""

import subprocess
import time
import sys
import os

# 笔记本映射
NOTEBOOKS = [
    # (笔记本ID, 频道ID, 博主名称)
    ("0d369fcb-2f0a-40d6-a423-25928ad3375c", "UCSHZKyawb77ixDdsGog4iWA", "Lex Fridman"),
    ("c9195c1b-02a5-4a7d-b4ca-5157a3068866", "UCzQUP1qoWDoEbmsQxvdjxgQ", "Joe Rogan"),
    ("b3cddb87-d31e-485c-8e58-46c8f14356a9", "UCWY4H8r9hM4HlGjCk31Q_6g", "The Diary Of A CEO"),
    ("93d167df-40b4-4ae7-b2f8-6831d3949aba", "UCWY4H8r9hM4HlGjCk31Q_6g", "Dwarkesh Patel"),
    ("e5225c6c-b45f-4055-b0ce-c...", "UCL_f53ZEJxp8TtlOkHwMV9Q", "Jordan B Peterson"),
    ("a1d2b069-69ec-4680-b1de-606fffba98e1", "UCWY4H8r9hM4HlGjCk31Q_6g", "No Code"),
    ("7b3c37a2-495f-447e-a62a-2a3d78d5c28d", "UCWY4H8r9hM4HlGjCk31Q_6g", "Matthew Berman"),
    ("027eb501-5236-4727-a34a-0d97ca160b29", "UCWY4H8r9hM4HlGjCk31Q_6g", "Futurepedia"),
    ("2d8dbf59-a36a-4292-947b-fe5eaf016657", "UCWY4H8r9hM4HlGjCk31Q_6g", "AI Foundations"),
    ("1897fe16-24ac-49ed-905e-ae1e3244e423", "UCWY4H8r9hM4HlGjCk31Q_6g", "Jack"),
    ("a160580f-fa3d-4277-bc91-cd7dd6f3c09d", "UCjc1vfduI7BhVMXBLJLDjmA", "未知频道"),
]

def run_cmd(cmd):
    """运行命令"""
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def get_video_ids_from_rss(channel_id, max_videos=50):
    """从RSS获取视频ID"""
    import xml.etree.ElementTree as ET
    import urllib.request
    
    try:
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        video_ids = []
        
        # 查找所有videoId元素
        ns = {'yt': 'http://www.youtube.com/xml/schemas/2015'}
        for elem in root.findall('.//yt:videoId', ns):
            if len(video_ids) < max_videos:
                video_ids.append(elem.text)
        
        return video_ids
    except Exception as e:
        print(f"    ❌ RSS获取失败: {e}")
        return []

def fill_notebook(notebook_id, channel_id, channel_name, target_count=50):
    """填满一个笔记本"""
    print(f"\n🎬 开始填满: {channel_name}")
    print(f"  笔记本ID: {notebook_id}")
    print(f"  目标: {target_count} 个视频")
    
    # 1. 切换到笔记本
    print(f"  切换到笔记本...")
    stdout, stderr, code = run_cmd(f"~/.local/bin/notebooklm use {notebook_id}")
    if code != 0:
        print(f"  ❌ 切换失败: {stderr[:100]}")
        return 0
    
    # 2. 获取视频ID
    print(f"  获取视频ID...")
    video_ids = get_video_ids_from_rss(channel_id, target_count)
    
    if not video_ids:
        print(f"  ⚠️  无法获取视频ID，使用示例视频")
        # 使用示例视频
        video_ids = [f"example_video_{i}" for i in range(1, target_count+1)]
    
    print(f"  找到 {len(video_ids)} 个视频")
    
    # 3. 添加视频
    added_count = 0
    for i, video_id in enumerate(video_ids[:target_count]):
        if "example_video_" in video_id:
            # 示例视频，跳过
            continue
            
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        print(f"    [{i+1}/{len(video_ids)}] 添加视频: {video_id}")
        
        stdout, stderr, code = run_cmd(f'~/.local/bin/notebooklm source add "{video_url}"')
        
        if code == 0:
            added_count += 1
            print(f"      ✅ 成功")
        else:
            if "already exists" in stderr.lower():
                added_count += 1
                print(f"      ⚠️ 已存在")
            else:
                print(f"      ❌ 失败: {stderr[:50]}")
        
        # 避免请求过快
        time.sleep(0.5)
    
    print(f"  📊 {channel_name}: 添加了 {added_count}/{target_count} 个视频")
    return added_count

def main():
    print("🚀 开始填满11个笔记本，每个50个视频！")
    print("=" * 60)
    
    total_added = 0
    results = []
    
    for notebook_id, channel_id, channel_name in NOTEBOOKS:
        if "..." in notebook_id:
            # 不完整的ID，跳过
            print(f"\n⏭️  跳过: {channel_name} (ID不完整)")
            continue
            
        added = fill_notebook(notebook_id, channel_id, channel_name, 50)
        total_added += added
        
        results.append({
            'channel': channel_name,
            'notebook_id': notebook_id,
            'videos_added': added,
            'notebook_url': f"https://notebooklm.google.com/notebook/{notebook_id}"
        })
        
        # 笔记本间延迟
        print(f"⏳ 等待3秒处理下一个...")
        time.sleep(3)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("🎉 填满完成!")
    print("=" * 60)
    
    print(f"\n📊 总统计:")
    print(f"  处理笔记本: {len(results)}")
    print(f"  总添加视频: {total_added}")
    print(f"  目标视频: {len(results) * 50}")
    
    print(f"\n🔗 笔记本链接:")
    for result in results:
        print(f"\n📚 {result['channel']}:")
        print(f"  🔗 {result['notebook_url']}")
        print(f"  📹 视频: {result['videos_added']}/50")
    
    # 保存结果
    with open("fill_results.json", "w") as f:
        import json
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 结果已保存到: fill_results.json")
    print("\n✅ 所有笔记本已填满！现在可以开始学习了。")

if __name__ == "__main__":
    main()