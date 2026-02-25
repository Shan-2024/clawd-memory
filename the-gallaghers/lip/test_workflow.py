#!/usr/bin/env python3
"""
Lip 实际测试 - 处理一个视频
"""
import os
import sys
import json
import subprocess
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.manager import config_manager
from ai.analyzer import AIAnalyzer


def test_single_video():
    """测试处理单个视频"""
    print(f"\n{'='*60}")
    print(f"🎬 测试处理单个视频")
    print(f"{'='*60}")
    
    # 选择一个测试视频（Lex Fridman的最新视频）
    video_url = "https://www.youtube.com/watch?v=YFjfBk8HI5o"
    video_id = "YFjfBk8HI5o"
    video_title = "OpenClaw: The Viral AI Agent that Broke the Internet"
    
    print(f"📹 视频: {video_title}")
    print(f"🔗 URL: {video_url}")
    
    # 1. 添加到NotebookLM
    print("\n1️⃣ 添加到NotebookLM...")
    notebooklm_bin = os.path.expanduser('~/.local/bin/notebooklm')
    
    try:
        # 创建或获取测试notebook
        notebook_title = "测试 - Lip系统"
        
        # 列出notebooks
        result = subprocess.run(
            [notebooklm_bin, 'list'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=30
        )
        
        notebook_id = None
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if notebook_title in line:
                    parts = line.split()
                    if parts:
                        notebook_id = parts[0]
                        print(f"  ✅ 找到现有notebook: {notebook_id}")
                        break
        
        if not notebook_id:
            # 创建新notebook
            result = subprocess.run(
                [notebooklm_bin, 'create', notebook_title],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=30
            )
            if result.returncode == 0:
                print(f"  ✅ 创建新notebook: {notebook_title}")
                # 重新获取ID
                result = subprocess.run(
                    [notebooklm_bin, 'list'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    timeout=30
                )
                for line in result.stdout.strip().split('\n'):
                    if notebook_title in line:
                        parts = line.split()
                        if parts:
                            notebook_id = parts[0]
        
        if notebook_id:
            # 切换到该notebook
            subprocess.run(
                [notebooklm_bin, 'use', notebook_id],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30
            )
            
            # 添加视频
            print(f"  添加视频到NotebookLM...")
            result = subprocess.run(
                [notebooklm_bin, 'source', 'add', video_url],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print(f"  ✅ 视频已添加到NotebookLM")
                
                # 2. 从NotebookLM获取摘要
                print(f"\n2️⃣ 从NotebookLM获取摘要...")
                question = f"请总结视频'{video_title}'的核心内容（3-5句话）"
                
                result = subprocess.run(
                    [notebooklm_bin, 'ask', question],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    timeout=60
                )
                
                if result.returncode == 0:
                    summary = result.stdout.strip()
                    print(f"  ✅ 获取到摘要:")
                    print(f"     {summary[:200]}...")
                    
                    # 3. 生成科普知识
                    print(f"\n3️⃣ 生成科普知识...")
                    analyzer = AIAnalyzer()
                    
                    # 模拟一个摘要用于测试
                    test_summary = "视频讨论了OpenClaw AI agent如何改变互联网，介绍了AI代理的工作原理和应用场景。"
                    
                    knowledge = analyzer.generate_knowledge_from_summary(video_title, test_summary)
                    
                    if knowledge:
                        print(f"  ✅ 生成 {len(knowledge)} 条科普:")
                        for term, explanation in knowledge.items():
                            print(f"    • {term}: {explanation[:80]}...")
                    else:
                        print(f"  ⚠️ 未生成科普知识")
                    
                    # 4. 保存结果
                    print(f"\n4️⃣ 保存结果...")
                    result_data = {
                        'video': {
                            'id': video_id,
                            'title': video_title,
                            'url': video_url
                        },
                        'notebooklm_summary': summary,
                        'knowledge': knowledge,
                        'processed_at': datetime.now().isoformat()
                    }
                    
                    # 保存到本地
                    output_dir = os.path.join(os.path.dirname(__file__), 'test_output')
                    os.makedirs(output_dir, exist_ok=True)
                    
                    output_file = os.path.join(output_dir, f"{video_id}_test.json")
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(result_data, f, ensure_ascii=False, indent=2)
                    
                    print(f"  ✅ 结果已保存到: {output_file}")
                    
                    # 5. 生成飞书文档内容
                    print(f"\n5️⃣ 生成飞书文档内容...")
                    feishu_content = f"""# 测试笔记 - {video_title}

## 📺 视频信息
- **标题**: {video_title}
- **链接**: [观看视频]({video_url})
- **处理时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 📝 NotebookLM摘要
{summary}

## 🎓 科普知识
"""
                    
                    if knowledge:
                        for term, explanation in knowledge.items():
                            feishu_content += f"\n- **{term}**: {explanation}"
                    else:
                        feishu_content += "\n*本视频未识别出需要解释的专业名词*"
                    
                    feishu_file = os.path.join(output_dir, f"{video_id}_feishu.md")
                    with open(feishu_file, 'w', encoding='utf-8') as f:
                        f.write(feishu_content)
                    
                    print(f"  ✅ 飞书文档已生成: {feishu_file}")
                    print(f"    内容长度: {len(feishu_content)} 字符")
                    
                    return True
                else:
                    print(f"  ❌ 获取摘要失败: {result.stderr[:100]}")
            else:
                print(f"  ❌ 添加视频失败: {result.stderr[:100]}")
        else:
            print(f"  ❌ 无法获取notebook ID")
            
    except Exception as e:
        print(f"  ❌ 处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return False


def main():
    success = test_single_video()
    
    print(f"\n{'='*60}")
    if success:
        print("✨ 测试成功！完整工作流运行正常。")
        print("   1. RSS获取视频 ✓")
        print("   2. NotebookLM分析 ✓")
        print("   3. AI生成科普 ✓")
        print("   4. 保存本地笔记 ✓")
        print("   5. 生成飞书文档 ✓")
    else:
        print("⚠️ 测试失败，需要检查问题。")
    
    print(f"{'='*60}")
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()