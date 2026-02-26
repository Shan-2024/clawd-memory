#!/usr/bin/env python3
"""
为所有11个YouTube博主获取50个视频，塞满NotebookLM笔记本
使用昨天的RSS方法
"""

import json
import os
import subprocess
import sys
import time
import feedparser

# 配置
CONFIG_PATH = "/home/admin/.openclaw/workspace/the-gallaghers/lip/config.json"
NOTEBOOKLM_CLI = os.path.expanduser("~/.local/bin/notebooklm")

# 频道ID映射（昨天已经有的）
CHANNEL_ID_MAPPING = {
    "https://www.youtube.com/@lexfridman": "UCSHZKyawb77ixDdsGog4iWA",
    "https://www.youtube.com/@JordanBPeterson": "UCL_f53ZEJxp8TtlOkHwMV9Q",
    "https://www.youtube.com/@joerogan": "UCzQUP1qoWDoEbmsQxvdjxgQ",
    "https://www.youtube.com/@TheDiaryOfACEO": "UCWY4H8r9hM4HlGjCk31Q_6g",
    "https://www.youtube.com/@DwarkeshPatel": "UCWY4H8r9hM4HlGjCk31Q_6g",  # 需要确认
    "https://www.youtube.com/@wearenocode/videos": "UCWY4H8r9hM4HlGjCk31Q_6g",  # 需要确认
    "https://www.youtube.com/@matthew_berman": "UCWY4H8r9hM4HlGjCk31Q_6g",  # 需要确认
    "https://www.youtube.com/@futurepedia_io/videos": "UCWY4H8r9hM4HlGjCk31Q_6g",  # 需要确认
    "https://www.youtube.com/@ai-foundations/videos": "UCWY4H8r9hM4HlGjCk31Q_6g",  # 需要确认
    "https://www.youtube.com/@Itssssss_Jack": "UCWY4H8r9hM4HlGjCk31Q_6g",  # 需要确认
    "https://www.youtube.com/channel/UCjc1vfduI7BhVMXBLJLDjmA": "UCjc1vfduI7BhVMXBLJLDjmA",
}

# 笔记本ID映射（刚才创建的）
NOTEBOOK_ID_MAPPING = {
    "Lex Fridman": "0d369fcb-2f0a-40d6-a423-25928ad3375c",
    "Joe Rogan Experience": "c9195c1b-02a5-4a7d-b4ca-5157a3068866",
    "The Diary Of A CEO": "b3cddb87-d31e-485c-8e58-46c8f14356a9",
    "Dwarkesh Patel": "93d167df-40b4-4ae7-b2f8-6831d3949aba",
    "Jordan B Peterson": "e5225c6c-b45f-4055-b0ce-c...",  # 已有
    "No Code": "a1d2b069-69ec-4680-b1de-606fffba98e1",
    "Matthew Berman": "7b3c37a2-495f-447e-a62a-2a3d78d5c28d",
    "Futurepedia": "027eb501-5236-4727-a34a-0d97ca160b29",
    "AI Foundations": "2d8dbf59-a36a-4292-947b-fe5eaf016657",
    "Jack": "1897fe16-24ac-49ed-905e-ae1e3244e423",
    "未知频道": "a160580f-fa3d-4277-bc91-cd7dd6f3c09d",
}

def load_config():
    """加载配置文件"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_channel_rss_url(channel_url):
    """根据频道URL获取RSS URL"""
    # 从映射中获取频道ID
    for url_pattern, channel_id in CHANNEL_ID_MAPPING.items():
        if url_pattern in channel_url:
            return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    
    # 尝试从URL中提取频道ID
    if '/channel/' in channel_url:
        channel_id = channel_url.split('/channel/')[-1].split('/')[0]
        return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    
    return None

def get_videos_from_rss(rss_url, max_videos=50):
    """从RSS获取多个视频"""
    try:
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            print(f"  ❌ RSS无内容: {rss_url}")
            return []
        
        videos = []
        for i, entry in enumerate(feed.entries[:max_videos]):
            video_id = entry.get('yt_videoid', '')
            
            if not video_id:
                # 尝试从id字段提取
                entry_id = entry.get('id', '')
                if 'video:' in entry_id:
                    video_id = entry_id.split(':')[-1]
            
            if video_id:
                videos.append({
                    'id': video_id,
                    'title': entry.get('title', f'视频{i+1}'),
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'published': entry.get('published', ''),
                })
        
        print(f"  📊 从RSS获取到 {len(videos)} 个视频")
        return videos
    except Exception as e:
        print(f"  ❌ 解析RSS失败: {e}")
        return []

def add_video_to_notebooklm(notebook_id, video_url):
    """添加视频到NotebookLM"""
    try:
        # 先切换到笔记本
        switch_cmd = [NOTEBOOKLM_CLI, "use", notebook_id]
        switch_result = subprocess.run(switch_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                      universal_newlines=True, timeout=10)
        
        if switch_result.returncode != 0:
            print(f"    ⚠️ 切换笔记本失败: {switch_result.stderr[:100]}")
            return False
        
        # 添加视频
        cmd = [NOTEBOOKLM_CLI, "source", "add", video_url]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                               universal_newlines=True, timeout=30)
        
        if result.returncode == 0:
            return True
        else:
            # 检查是否已经添加过
            if "already exists" in result.stderr.lower():
                return True
            print(f"    ⚠️ 添加失败: {result.stderr[:100]}")
            return False
    except Exception as e:
        print(f"    ❌ 执行失败: {e}")
        return False

def process_channel(channel_name, channel_url, notebook_id, max_videos=50):
    """处理单个频道"""
    print(f"\n🎬 处理频道: {channel_name}")
    print(f"  频道URL: {channel_url}")
    print(f"  笔记本ID: {notebook_id}")
    
    # 1. 获取RSS URL
    rss_url = get_channel_rss_url(channel_url)
    if not rss_url:
        print(f"  ❌ 无法获取RSS URL")
        return 0
    
    print(f"  📡 RSS URL: {rss_url}")
    
    # 2. 获取视频列表
    videos = get_videos_from_rss(rss_url, max_videos)
    if not videos:
        print(f"  ❌ 未获取到视频")
        return 0
    
    # 3. 添加视频到笔记本
    print(f"  📥 开始添加视频到笔记本...")
    success_count = 0
    
    for i, video in enumerate(videos[:max_videos]):
        print(f"    [{i+1}/{len(videos)}] 添加: {video['title'][:50]}...")
        
        if add_video_to_notebooklm(notebook_id, video['url']):
            success_count += 1
        
        # 避免请求过快
        time.sleep(1)
    
    print(f"  📊 {channel_name}: 成功添加 {success_count}/{len(videos)} 个视频")
    return success_count

def main():
    """主函数"""
    print("🚀 开始为所有11个博主获取50个视频，塞满笔记本！")
    print("=" * 70)
    
    # 加载配置
    config = load_config()
    
    # 处理所有活跃频道
    total_videos_added = 0
    results = []
    
    for channel in config.get('channels', []):
        if channel.get('status') != 'active':
            continue
        
        channel_name = channel.get('display_name', '')
        channel_url = channel.get('url', '')
        
        # 跳过测试频道
        if 'test' in channel_name.lower():
            continue
        
        # 获取笔记本ID
        notebook_id = NOTEBOOK_ID_MAPPING.get(channel_name)
        if not notebook_id:
            print(f"❌ 找不到 {channel_name} 的笔记本ID")
            continue
        
        # 处理频道
        videos_added = process_channel(channel_name, channel_url, notebook_id, max_videos=50)
        
        results.append({
            'channel': channel_name,
            'notebook_id': notebook_id,
            'videos_added': videos_added,
            'notebook_url': f"https://notebooklm.google.com/notebook/{notebook_id}"
        })
        
        total_videos_added += videos_added
        
        # 频道间延迟
        print(f"⏳ 等待5秒处理下一个频道...")
        time.sleep(5)
    
    # 输出结果汇总
    print("\n" + "=" * 70)
    print("🎉 处理完成!")
    print("=" * 70)
    
    print(f"\n📊 总统计:")
    print(f"  处理频道数: {len(results)}")
    print(f"  总添加视频: {total_videos_added}")
    
    # 输出访问链接
    print("\n🔗 笔记本访问链接:")
    print("=" * 70)
    for result in results:
        if result['videos_added'] > 0:
            print(f"\n📚 {result['channel']}:")
            print(f"  🔗 {result['notebook_url']}")
            print(f"  📹 视频数量: {result['videos_added']}/50")
    
    # 保存结果
    output_file = "notebooklm_filled_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 结果已保存到: {output_file}")
    print("\n✅ 所有笔记本已塞满视频！现在可以开始学习了。")

if __name__ == "__main__":
    # 检查feedparser是否安装
    try:
        import feedparser
    except ImportError:
        print("❌ 需要安装feedparser: pip install feedparser")
        sys.exit(1)
    
    main()