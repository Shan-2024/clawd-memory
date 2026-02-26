#!/usr/bin/env python3
"""
验证所有频道ID，确保能获取到视频
"""

import urllib.request
import xml.etree.ElementTree as ET

# 需要验证的频道
CHANNELS_TO_VERIFY = [
    ("Lex Fridman", "UCSHZKyawb77ixDdsGog4iWA"),
    ("Joe Rogan", "UCzQUP1qoWDoEbmsQxvdjxgQ"),
    ("Jordan B Peterson", "UCL_f53ZEJxp8TtlOkHwMV9Q"),
    ("The Diary Of A CEO", "UCWY4H8r9hM4HlGjCk31Q_6g"),
    ("Dwarkesh Patel", "UCWY4H8r9hM4HlGjCk31Q_6g"),
    ("Matthew Berman", "UCWY4H8r9hM4HlGjCk31Q_6g"),
    ("AI Explained", "UCWY4H8r9hM4HlGjCk31Q_6g"),
    ("Futurepedia", "UCWY4H8r9hM4HlGjCk31Q_6g"),
    ("No Code", "UCWY4H8r9hM4HlGjCk31Q_6g"),
    ("Jack", "UCWY4H8r9hM4HlGjCk31Q_6g"),
    ("Unknown Channel", "UCjc1vfduI7BhVMXBLJLDjmA"),
]

def test_channel(channel_name, channel_id):
    """测试频道ID是否有效"""
    try:
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        
        if response.status == 200:
            # 解析XML获取视频数量
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            ns = {'yt': 'http://www.youtube.com/xml/schemas/2015'}
            video_ids = root.findall('.//yt:videoId', ns)
            
            return True, len(video_ids), video_ids[:5] if video_ids else []
        else:
            return False, 0, []
            
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False, 0, []
        else:
            return False, 0, []
    except Exception as e:
        return False, 0, []

def main():
    print("🔍 验证所有YouTube频道ID")
    print("=" * 60)
    
    valid_channels = []
    invalid_channels = []
    
    for channel_name, channel_id in CHANNELS_TO_VERIFY:
        print(f"\n📺 {channel_name}:")
        print(f"  频道ID: {channel_id}")
        
        is_valid, video_count, sample_videos = test_channel(channel_name, channel_id)
        
        if is_valid:
            print(f"  ✅ 有效 - 找到 {video_count} 个视频")
            if sample_videos:
                print(f"  示例视频ID: {', '.join([v.text for v in sample_videos[:3]])}")
            valid_channels.append((channel_name, channel_id, video_count))
        else:
            print(f"  ❌ 无效 - RSS返回404或无数据")
            invalid_channels.append((channel_name, channel_id))
    
    print("\n" + "=" * 60)
    print("📊 验证结果:")
    print("=" * 60)
    
    print(f"\n✅ 有效的频道 ({len(valid_channels)}个):")
    for name, cid, count in valid_channels:
        print(f"  • {name}: {cid} ({count}个视频)")
    
    print(f"\n❌ 无效的频道 ({len(invalid_channels)}个):")
    for name, cid in invalid_channels:
        print(f"  • {name}: {cid}")
    
    print(f"\n🎯 建议:")
    print("  1. 只使用有效的频道创建笔记本")
    print("  2. 为无效的频道查找正确ID")
    print("  3. 或者使用其他内容源")
    
    # 保存结果
    import json
    result = {
        'valid': [{'name': n, 'id': i, 'video_count': c} for n, i, c in valid_channels],
        'invalid': [{'name': n, 'id': i} for n, i in invalid_channels]
    }
    
    with open('channel_verification.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n💾 结果已保存到: channel_verification.json")

if __name__ == "__main__":
    main()