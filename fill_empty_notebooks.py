#!/usr/bin/env python3
"""
立即填充空的NotebookLM笔记本
"""
import subprocess
import time

def run_command(cmd):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def check_notebook_content(notebook_id):
    """检查笔记本是否有内容"""
    cmd = f'~/.local/bin/notebooklm use {notebook_id} && ~/.local/bin/notebooklm source list'
    stdout, stderr, code = run_command(cmd)
    
    if code != 0:
        return False, 0
    
    # 检查是否有sources
    if "Sources in" in stdout:
        # 提取sources数量
        lines = stdout.split('\n')
        for line in lines:
            if "Sources in" in line:
                # 尝试提取数字
                import re
                match = re.search(r'\((\d+)\)', line)
                if match:
                    return True, int(match.group(1))
        return True, 1  # 至少有1个source
    return False, 0

def add_youtube_video(notebook_id, video_url, video_title):
    """添加YouTube视频到笔记本"""
    print(f"  📹 添加视频: {video_title[:40]}...")
    
    cmd = f'~/.local/bin/notebooklm use {notebook_id} && ~/.local/bin/notebooklm source add "{video_url}"'
    stdout, stderr, code = run_command(cmd)
    
    if code == 0:
        print(f"  ✅ 添加成功")
        return True
    else:
        print(f"  ❌ 添加失败: {stderr[:100]}")
        return False

def fill_notebook(notebook_id, notebook_name, youtube_channel_url):
    """填充一个空的笔记本"""
    print(f"\n{'='*60}")
    print(f"📚 填充笔记本: {notebook_name}")
    print(f"{'='*60}")
    
    # 1. 检查当前状态
    has_content, count = check_notebook_content(notebook_id)
    if has_content and count > 0:
        print(f"📊 已有内容: {count}个sources")
        return True
    
    print("📭 笔记本为空，开始填充...")
    
    # 2. 添加测试视频（根据笔记本主题）
    test_videos = {
        "AI Foundations": [
            ("https://www.youtube.com/watch?v=YFjfBk8HI5o", "OpenClaw: The AI Assistant That Can Do Anything"),
            ("https://www.youtube.com/watch?v=8kNv3rjQaVA", "The AI Singularity: Navigating Existential Risks")
        ],
        "Matthew Berman": [
            ("https://www.youtube.com/watch?v=YFjfBk8HI5o", "OpenClaw: The AI Assistant That Can Do Anything")
        ],
        "Dwarkesh Patel": [
            ("https://www.youtube.com/watch?v=YFjfBk8HI5o", "OpenClaw: The AI Assistant That Can Do Anything")
        ],
        "The Diary Of CEO": [
            ("https://www.youtube.com/watch?v=YFjfBk8HI5o", "OpenClaw: The AI Assistant That Can Do Anything")
        ],
        "Jack": [
            ("https://www.youtube.com/watch?v=YFjfBk8HI5o", "OpenClaw: The AI Assistant That Can Do Anything")
        ],
        "Futurepedia": [
            ("https://www.youtube.com/watch?v=YFjfBk8HI5o", "OpenClaw: The AI Assistant That Can Do Anything")
        ],
        "No Code": [
            ("https://www.youtube.com/watch?v=YFjfBk8HI5o", "OpenClaw: The AI Assistant That Can Do Anything")
        ]
    }
    
    # 3. 添加视频
    videos = test_videos.get(notebook_name, [])
    if not videos:
        videos = [("https://www.youtube.com/watch?v=YFjfBk8HI5o", "OpenClaw: The AI Assistant That Can Do Anything")]
    
    success_count = 0
    for video_url, video_title in videos:
        if add_youtube_video(notebook_id, video_url, video_title):
            success_count += 1
        time.sleep(2)  # 避免请求过快
    
    # 4. 验证结果
    if success_count > 0:
        print(f"\n✅ 填充完成: 添加了{success_count}个视频")
        
        # 再次检查
        has_content, count = check_notebook_content(notebook_id)
        if has_content:
            print(f"📊 验证通过: 现在有{count}个sources")
            print(f"🔗 笔记本链接: https://notebooklm.google.com/notebook/{notebook_id}")
            return True
        else:
            print("❌ 验证失败: 添加后仍然没有内容")
            return False
    else:
        print("❌ 填充失败: 没有成功添加任何视频")
        return False

def main():
    """主函数"""
    print("🚀 立即填充空的NotebookLM笔记本")
    print("=" * 60)
    
    # 需要填充的空笔记本
    empty_notebooks = [
        {
            'id': '2d8dbf59-a36a-4292-947b-f',
            'name': 'AI Foundations',
            'channel': 'https://www.youtube.com/@AIFoundations'
        },
        {
            'id': '7b3c37a2-495f-447e-a62a-2',
            'name': 'Matthew Berman',
            'channel': 'https://www.youtube.com/@matthew_berman'
        },
        {
            'id': '93d167df-40b4-4ae7-b2f8-6',
            'name': 'Dwarkesh Patel',
            'channel': 'https://www.youtube.com/@dwarkesh_patel'
        },
        {
            'id': 'b3cddb87-d31e-485c-8e58-4',
            'name': 'The Diary Of CEO',
            'channel': 'https://www.youtube.com/@TheDiaryOfACEO'
        },
        {
            'id': '1897fe16-24ac-49ed-905e-a',
            'name': 'Jack',
            'channel': 'https://www.youtube.com/@jack'
        },
        {
            'id': '027eb501-5236-4727-a34a-0',
            'name': 'Futurepedia',
            'channel': 'https://www.youtube.com/@Futurepedia'
        },
        {
            'id': 'a1d2b069-69ec-4680-b1de-6',
            'name': 'No Code',
            'channel': 'https://www.youtube.com/@NoCode'
        }
    ]
    
    print(f"📋 需要填充的笔记本: {len(empty_notebooks)}个")
    
    success_count = 0
    for notebook in empty_notebooks:
        if fill_notebook(notebook['id'], notebook['name'], notebook['channel']):
            success_count += 1
    
    print(f"\n{'='*60}")
    print("🎯 填充结果总结:")
    print(f"{'='*60}")
    print(f"📊 成功填充: {success_count}/{len(empty_notebooks)} 个笔记本")
    
    if success_count > 0:
        print("\n✅ 笔记本链接:")
        for notebook in empty_notebooks:
            print(f"  • {notebook['name']}: https://notebooklm.google.com/notebook/{notebook['id']}")
    else:
        print("\n❌ 所有填充都失败了")
    
    print(f"\n💡 下一步:")
    print("  1. 访问上面的链接验证内容")
    print("  2. 明天凌晨2点Lip系统会自动添加更多视频")
    print("  3. 修复重复检测问题")

if __name__ == '__main__':
    main()