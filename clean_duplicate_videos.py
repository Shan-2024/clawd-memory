#!/usr/bin/env python3
"""
清理NotebookLM中的重复视频
"""
import subprocess
import json
import re
from collections import defaultdict

def run_command(cmd):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def get_notebook_sources(notebook_id):
    """获取笔记本的所有sources"""
    print(f"📚 获取笔记本 {notebook_id} 的sources...")
    
    cmd = f'~/.local/bin/notebooklm use {notebook_id} && ~/.local/bin/notebooklm source list'
    stdout, stderr, code = run_command(cmd)
    
    if code != 0:
        print(f"❌ 获取失败: {stderr[:200]}")
        return []
    
    # 解析sources
    sources = []
    lines = stdout.split('\n')
    
    # 找到sources表格的开始
    start_idx = -1
    for i, line in enumerate(lines):
        if "Sources in" in line:
            start_idx = i + 2  # 跳过表头
            break
    
    if start_idx == -1:
        print("❌ 找不到sources表格")
        return []
    
    # 解析每一行
    for i in range(start_idx, len(lines)):
        line = lines[i].strip()
        if not line or line.startswith('└') or line.startswith('┏'):
            continue
            
        # 解析source信息
        parts = line.split('│')
        if len(parts) >= 5:
            source_id = parts[0].strip()
            title = parts[1].strip()
            source_type = parts[2].strip()
            created = parts[3].strip()
            status = parts[4].strip()
            
            # 提取YouTube视频ID
            video_id = extract_video_id(title)
            
            sources.append({
                'id': source_id,
                'title': title,
                'type': source_type,
                'created': created,
                'status': status,
                'video_id': video_id
            })
    
    print(f"✅ 找到 {len(sources)} 个sources")
    return sources

def extract_video_id(title):
    """从标题中提取视频ID（简化版）"""
    # 尝试从标题中提取视频ID
    # 实际应该从URL中提取，但这里只有标题
    # 使用标题作为唯一标识
    return title[:50]  # 取前50个字符作为标识

def find_duplicates(sources):
    """查找重复的视频"""
    print("🔍 查找重复视频...")
    
    # 按视频ID分组
    groups = defaultdict(list)
    for source in sources:
        if source['video_id']:
            groups[source['video_id']].append(source)
    
    # 找出重复的组
    duplicates = []
    for video_id, sources_list in groups.items():
        if len(sources_list) > 1:
            duplicates.append({
                'video_id': video_id,
                'count': len(sources_list),
                'sources': sources_list
            })
    
    print(f"📊 找到 {len(duplicates)} 个重复视频")
    return duplicates

def delete_source(notebook_id, source_id):
    """删除一个source"""
    print(f"  🗑️  删除source: {source_id[:12]}...")
    
    # NotebookLM CLI目前没有删除source的命令
    # 需要手动在Web界面删除
    # 这里只输出信息
    print(f"  ⚠️  需要手动删除: https://notebooklm.google.com/notebook/{notebook_id}")
    return False

def clean_notebook(notebook_id, notebook_name):
    """清理一个笔记本的重复视频"""
    print(f"\n{'='*60}")
    print(f"🧹 清理笔记本: {notebook_name}")
    print(f"{'='*60}")
    
    # 1. 获取所有sources
    sources = get_notebook_sources(notebook_id)
    if not sources:
        return
    
    # 2. 查找重复
    duplicates = find_duplicates(sources)
    
    if not duplicates:
        print("✅ 没有重复视频")
        return
    
    # 3. 分析重复情况
    total_duplicates = sum(d['count'] - 1 for d in duplicates)
    print(f"\n📊 重复统计:")
    print(f"  重复视频数: {len(duplicates)}")
    print(f"  需要删除的重复项: {total_duplicates}")
    
    # 4. 显示重复详情
    print(f"\n📋 重复详情:")
    for i, dup in enumerate(duplicates[:10], 1):  # 只显示前10个
        print(f"  {i}. {dup['video_id'][:40]}...")
        print(f"     重复次数: {dup['count']}")
        for source in dup['sources'][:2]:  # 显示前2个重复
            print(f"     - {source['id'][:12]} ({source['created']})")
    
    if len(duplicates) > 10:
        print(f"  ... 还有 {len(duplicates) - 10} 个重复视频")
    
    # 5. 建议
    print(f"\n💡 建议:")
    print(f"  1. 访问 https://notebooklm.google.com/notebook/{notebook_id}")
    print(f"  2. 手动删除重复的sources")
    print(f"  3. 保留每个视频的最新版本")
    print(f"  4. 删除后重新运行此脚本验证")
    
    # 6. 保存分析结果
    result = {
        'notebook_id': notebook_id,
        'notebook_name': notebook_name,
        'total_sources': len(sources),
        'duplicate_groups': len(duplicates),
        'duplicate_items': total_duplicates,
        'duplicates': duplicates[:20]  # 只保存前20个
    }
    
    with open(f'duplicate_analysis_{notebook_name}.json', 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 分析结果已保存到: duplicate_analysis_{notebook_name}.json")

def main():
    """主函数"""
    print("🧹 NotebookLM重复视频清理工具")
    print("=" * 60)
    
    # 需要清理的笔记本
    notebooks = [
        {
            'id': '0d369fcb-2f0a-40d6-a423-25928ad3375c',
            'name': 'lexfridman'
        },
        {
            'id': 'c9195c1b-02a5-4a7d-b4ca-5157a3068866',
            'name': 'joerogan'
        },
        {
            'id': 'a160580f-fa3d-4277-bc91-cd7dd6f3c09d',
            'name': 'unknown_channel'
        }
    ]
    
    for notebook in notebooks:
        clean_notebook(notebook['id'], notebook['name'])
    
    print(f"\n{'='*60}")
    print("🎯 清理建议总结:")
    print(f"{'='*60}")
    print("\n由于NotebookLM CLI没有删除source的命令，需要:")
    print("1. 📱 访问每个笔记本的Web界面")
    print("2. 🗑️  手动删除重复的sources")
    print("3. 🔄 删除后重新运行此脚本验证")
    print("\n笔记本链接:")
    for notebook in notebooks:
        print(f"  • {notebook['name']}: https://notebooklm.google.com/notebook/{notebook['id']}")
    
    print(f"\n💡 预防措施:")
    print("  1. 修复Lip系统的重复检测逻辑")
    print("  2. 在添加前检查是否已存在相同视频")
    print("  3. 使用唯一的视频ID作为标识")

if __name__ == '__main__':
    main()