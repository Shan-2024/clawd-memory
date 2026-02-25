#!/usr/bin/env python3
"""
修复NotebookLM集成 - 手动添加视频到NotebookLM
"""

import json
import os
import subprocess
import sys

# 配置
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')
NOTEBOOKLM_CLI = os.path.expanduser("~/.local/bin/notebooklm")

def load_config():
    """加载配置文件"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_channel_rss_url(channel_url):
    """根据频道URL获取RSS URL"""
    # 已知的频道ID映射
    channel_mapping = {
        "https://www.youtube.com/@lexfridman": "UCSHZKyawb77ixDdsGog4iWA",
        "https://www.youtube.com/@JordanBPeterson": "UCL_f53ZEJxp8TtlOkHwMV9Q",
        "https://www.youtube.com/@joerogan": "UCzQUP1qoWDoEbmsQxvdjxgQ",
    }
    
    # 尝试从映射中获取
    if channel_url in channel_mapping:
        channel_id = channel_mapping[channel_url]
        return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    
    # 默认返回None
    return None

def get_latest_video_from_rss(rss_url):
    """从RSS获取最新视频"""
    import feedparser
    
    try:
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            return None
        
        # 获取最新视频
        latest_entry = feed.entries[0]
        video_id = latest_entry.get('yt_videoid', '')
        
        if not video_id:
            # 尝试从id字段提取
            entry_id = latest_entry.get('id', '')
            if 'video:' in entry_id:
                video_id = entry_id.split(':')[-1]
        
        if video_id:
            return {
                'id': video_id,
                'title': latest_entry.get('title', ''),
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'published': latest_entry.get('published', ''),
            }
    except Exception as e:
        print(f"解析RSS失败: {e}")
    
    return None

def add_video_to_notebooklm(notebook_id, video_url):
    """添加视频到NotebookLM"""
    try:
        cmd = [NOTEBOOKLM_CLI, "source", "add", video_url]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ 成功添加视频: {video_url}")
            return True
        else:
            print(f"❌ 添加视频失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 执行命令失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始修复NotebookLM集成...")
    
    # 加载配置
    config = load_config()
    
    # 查找lexfridman笔记本
    lex_notebook_id = None
    for channel in config.get('channels', []):
        if 'lexfridman' in channel.get('name', '').lower():
            print(f"📺 找到频道: {channel.get('display_name', '未知')}")
            
            # 获取频道URL
            channel_url = channel.get('url', '')
            if not channel_url:
                print("❌ 频道URL为空")
                continue
            
            # 获取RSS URL
            rss_url = get_channel_rss_url(channel_url)
            if not rss_url:
                print(f"❌ 无法获取RSS URL: {channel_url}")
                continue
            
            print(f"📡 RSS URL: {rss_url}")
            
            # 获取最新视频
            video = get_latest_video_from_rss(rss_url)
            if not video:
                print("❌ 未获取到视频")
                continue
            
            print(f"🎬 最新视频: {video['title']}")
            print(f"🔗 视频URL: {video['url']}")
            
            # 查找或创建笔记本
            # 这里简化处理，使用现有的lexfridman笔记本
            lex_notebook_id = "0d369fcb-2f0a-40d6-a423-25928ad3375c"
            
            if lex_notebook_id:
                print(f"📓 使用笔记本: {lex_notebook_id}")
                
                # 切换到笔记本
                subprocess.run([NOTEBOOKLM_CLI, "use", lex_notebook_id], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                
                # 添加视频
                success = add_video_to_notebooklm(lex_notebook_id, video['url'])
                
                if success:
                    print("✅ 修复完成！NotebookLM现在有内容了。")
                    print(f"🎯 可以访问: https://notebooklm.google.com/notebook/{lex_notebook_id}")
                    return True
    
    print("❌ 修复失败")
    return False

if __name__ == "__main__":
    main()