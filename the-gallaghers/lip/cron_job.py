#!/usr/bin/env python3
"""
Lip 定时任务入口
每日执行：分析所有博主的视频
"""
import os
import sys
from datetime import datetime
from typing import List, Dict

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.manager import config_manager
from youtube.parser import YouTubeURLParser
from youtube.extractor import YouTubeExtractor
from ai.analyzer import AIAnalyzer
from storage.local import LocalStorage


class DailyAnalyzer:
    """每日分析任务"""
    
    def __init__(self):
        self.config = config_manager
        self.extractor = YouTubeExtractor()
        self.analyzer = AIAnalyzer()
        self.storage = LocalStorage()
        self.parser = YouTubeURLParser()
        
        # 每日每个博主的分析上限
        self.daily_limit = 5
    
    def run(self) -> Dict:
        """
        执行每日分析任务
        
        Returns:
            执行结果统计
        """
        print(f"\n{'='*60}")
        print(f"🤖 Lip 每日分析任务开始 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*60}\n")
        
        channels = self.config.get_all_channels()
        
        if not channels:
            print("⚠️  没有监控任何博主，任务结束")
            return {'success': True, 'analyzed': 0, 'channels': 0}
        
        total_analyzed = 0
        results = []
        
        for channel in channels:
            if channel['status'] != 'active':
                continue
            
            print(f"\n📺 正在处理博主: {channel['name']}")
            print("-" * 40)
            
            try:
                result = self._analyze_channel(channel)
                results.append(result)
                total_analyzed += result['analyzed_count']
                
            except Exception as e:
                print(f"❌ 处理博主 {channel['name']} 时出错: {e}")
                results.append({
                    'channel_name': channel['name'],
                    'analyzed_count': 0,
                    'error': str(e)
                })
        
        # 生成日报
        self._send_daily_report(results, total_analyzed)
        
        print(f"\n{'='*60}")
        print(f"✅ 分析完成，共处理 {total_analyzed} 条视频")
        print(f"{'='*60}\n")
        
        return {
            'success': True,
            'analyzed': total_analyzed,
            'channels': len(channels),
            'details': results
        }
    
    def _analyze_channel(self, channel: Dict) -> Dict:
        """分析单个博主的视频"""
        channel_name = channel['name']
        channel_url = channel['url']
        analyzed_ids = channel.get('analyzed_video_ids', [])
        
        # 获取频道最新视频
        print(f"  正在获取视频列表...")
        videos = self.extractor.get_channel_videos(channel_url, limit=50)
        
        if not videos:
            print(f"  ⚠️  无法获取视频列表")
            return {'channel_name': channel_name, 'analyzed_count': 0}
        
        # 更新总视频数
        self.config.update_channel_stats(channel_name, total_videos=len(videos))
        
        # 筛选未分析的视频（按最新排序）
        new_videos = [v for v in videos if v['id'] not in analyzed_ids]
        
        if not new_videos:
            print(f"  ✅ 所有视频已分析完毕")
            return {'channel_name': channel_name, 'analyzed_count': 0}
        
        # 取前N条
        videos_to_analyze = new_videos[:self.daily_limit]
        print(f"  找到 {len(new_videos)} 条新视频，本次分析 {len(videos_to_analyze)} 条")
        
        analyzed_count = 0
        
        for video in videos_to_analyze:
            try:
                print(f"\n  📹 分析视频: {video['title'][:50]}...")
                
                # 1. 获取视频信息
                video_info = self.extractor.get_video_info(video['url'])
                
                # 2. 提取字幕
                print(f"    提取字幕...")
                transcript = self.extractor.extract_transcript(video['url'])
                
                if not transcript:
                    print(f"    ⚠️  该视频无字幕，跳过")
                    self.config.add_analyzed_video(channel_name, video['id'])
                    continue
                
                print(f"    字幕长度: {len(transcript)} 字符")
                
                # 3. AI分析
                print(f"    AI分析中...")
                analysis = self.analyzer.analyze_video(transcript)
                
                # 4. 保存笔记
                print(f"    保存笔记...")
                filepath = self.storage.save_note(channel_name, video_info, analysis, transcript)
                print(f"    ✅ 已保存: {filepath}")
                
                # 5. 标记为已分析
                self.config.add_analyzed_video(channel_name, video['id'])
                analyzed_count += 1
                
            except Exception as e:
                print(f"    ❌ 分析失败: {e}")
                # 仍然标记为已分析，避免反复重试失败视频
                self.config.add_analyzed_video(channel_name, video['id'])
        
        # 更新最后分析时间
        self.config.update_channel_stats(
            channel_name,
            last_analyzed_at=datetime.now().isoformat()
        )
        
        print(f"\n  ✅ 博主 {channel_name} 完成，本次分析 {analyzed_count} 条")
        
        return {
            'channel_name': channel_name,
            'analyzed_count': analyzed_count
        }
    
    def _send_daily_report(self, results: List[Dict], total: int):
        """发送日报到飞书"""
        lines = [f"📊 Lip 每日分析报告 ({datetime.now().strftime('%m-%d')})\n"]
        lines.append(f"今日共分析 **{total}** 条视频\n")
        
        for result in results:
            name = result['channel_name']
            count = result['analyzed_count']
            error = result.get('error')
            
            if error:
                lines.append(f"❌ **{name}**: 失败 - {error}")
            elif count > 0:
                lines.append(f"✅ **{name}**: 分析 {count} 条")
            else:
                lines.append(f"⏸️  **{name}**: 无新视频")
        
        report = '\n'.join(lines)
        
        # 发送到飞书
        try:
            # 使用OpenClaw的消息发送
            import subprocess
            subprocess.run(
                ['openclaw', 'message', 'send', report],
                capture_output=True,
                timeout=30
            )
            print("\n📨 日报已发送到飞书")
        except Exception as e:
            print(f"\n⚠️  发送日报失败: {e}")
            print(f"日报内容:\n{report}")


def main():
    """主入口"""
    analyzer = DailyAnalyzer()
    result = analyzer.run()
    
    # 返回退出码
    sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    main()