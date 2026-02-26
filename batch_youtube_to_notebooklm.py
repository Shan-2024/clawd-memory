#!/usr/bin/env python3
"""
批量将YouTube频道视频添加到NotebookLM
每个频道5个最新视频
"""

import subprocess
import json
import time
import sys

def run_command(cmd):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def create_notebook(title):
    """创建新的NotebookLM笔记本"""
    print(f"📝 创建笔记本: {title}")
    cmd = f'~/.local/bin/notebooklm create "{title}"'
    stdout, stderr, code = run_command(cmd)
    
    if code != 0:
        print(f"❌ 创建失败: {stderr}")
        return None
    
    # 解析笔记本ID
    lines = stdout.split('\n')
    for line in lines:
        if '│' in line:
            parts = line.split('│')
            if len(parts) > 1:
                notebook_id = parts[1].strip()
                if notebook_id and len(notebook_id) > 10:
                    print(f"✅ 笔记本ID: {notebook_id}")
                    return notebook_id
    
    return None

def add_youtube_source(notebook_id, video_url):
    """添加YouTube视频源到笔记本"""
    print(f"  ➕ 添加视频: {video_url}")
    cmd = f'~/.local/bin/notebooklm use {notebook_id} && ~/.local/bin/notebooklm source add "{video_url}"'
    stdout, stderr, code = run_command(cmd)
    
    if code != 0:
        print(f"  ⚠️  添加失败: {stderr[:100]}")
        return False
    
    print("  ✅ 添加成功")
    return True

def get_channel_videos(channel_id, count=5):
    """获取频道最新视频（简化版，实际需要YouTube API）"""
    # 这里需要YouTube API，暂时返回示例视频
    # 实际使用时需要替换为真实的YouTube数据获取逻辑
    print(f"🔍 获取频道 {channel_id} 的最新{count}个视频")
    
    # 示例：返回一些测试视频
    # 实际应该调用YouTube API获取真实视频
    return [
        f"https://www.youtube.com/watch?v=test1_{channel_id}",
        f"https://www.youtube.com/watch?v=test2_{channel_id}",
        f"https://www.youtube.com/watch?v=test3_{channel_id}",
        f"https://www.youtube.com/watch?v=test4_{channel_id}",
        f"https://www.youtube.com/watch?v=test5_{channel_id}",
    ]

def process_channel(channel_name, channel_id=None, video_urls=None):
    """处理单个频道"""
    print(f"\n🎬 处理频道: {channel_name}")
    
    # 1. 创建笔记本
    notebook_title = f"学习笔记 - {channel_name}"
    notebook_id = create_notebook(notebook_title)
    
    if not notebook_id:
        print(f"❌ 无法为 {channel_name} 创建笔记本")
        return None
    
    # 2. 获取视频URL
    if video_urls:
        urls = video_urls[:5]  # 只取前5个
    elif channel_id:
        urls = get_channel_videos(channel_id, 5)
    else:
        print(f"❌ 需要提供channel_id或video_urls")
        return None
    
    # 3. 添加视频源
    success_count = 0
    for url in urls:
        if add_youtube_source(notebook_id, url):
            success_count += 1
        time.sleep(2)  # 避免请求过快
    
    print(f"📊 {channel_name}: 成功添加 {success_count}/{len(urls)} 个视频")
    
    # 4. 返回笔记本信息
    notebook_url = f"https://notebooklm.google.com/notebook/{notebook_id}"
    return {
        "channel": channel_name,
        "notebook_id": notebook_id,
        "notebook_url": notebook_url,
        "videos_added": success_count
    }

def main():
    """主函数"""
    print("🚀 YouTube批量处理工具")
    print("=" * 50)
    
    # 示例：处理一些频道
    # 实际使用时，从参数或文件读取
    channels = [
        # 格式: [频道名称, 频道ID, [可选: 视频URL列表]]
        # ["LexFridman", "UCSHZKyawb77ixDdsGog4iWA"],
        # ["JordanBPeterson", "UCG8RbK1JNfW_BbaMk2fO_8g"],
    ]
    
    if len(sys.argv) > 1:
        # 从命令行参数读取
        channel_file = sys.argv[1]
        print(f"📁 从文件读取: {channel_file}")
        # 这里应该读取文件内容
    else:
        print("📋 请提供频道列表文件或直接在代码中配置")
        print("\n使用方法:")
        print("  python3 batch_youtube_to_notebooklm.py channels.txt")
        print("\nchannels.txt格式:")
        print("  频道名称,频道ID")
        print("  或者")
        print("  频道名称,视频URL1,视频URL2,视频URL3,视频URL4,视频URL5")
        return
    
    results = []
    for channel_info in channels:
        if len(channel_info) == 2:
            # 只有名称和ID
            result = process_channel(channel_info[0], channel_info[1])
        elif len(channel_info) > 2:
            # 有视频URL列表
            result = process_channel(channel_info[0], video_urls=channel_info[2:])
        
        if result:
            results.append(result)
        time.sleep(5)  # 频道间延迟
    
    # 输出结果汇总
    print("\n" + "=" * 50)
    print("📊 处理完成!")
    print("=" * 50)
    
    for result in results:
        print(f"\n📚 {result['channel']}:")
        print(f"  笔记本ID: {result['notebook_id']}")
        print(f"  访问链接: {result['notebook_url']}")
        print(f"  视频数量: {result['videos_added']}/5")
    
    # 保存结果到文件
    with open("notebooklm_results.json", "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 结果已保存到: notebooklm_results.json")

if __name__ == "__main__":
    main()