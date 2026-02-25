#!/usr/bin/env python3
"""
生成详细的视频分析 - 直接使用OpenClaw环境
"""
import subprocess
import json
import os
from datetime import datetime

def call_openclaw_model(prompt: str, model: str = "kimi/kimi-k2.5") -> str:
    """
    调用OpenClaw模型
    """
    try:
        # 使用OpenClaw命令行工具 - Python 3.6兼容版本
        cmd = ["openclaw", "chat", "--model", model, "--system", "你是一个专业的视频内容分析专家", prompt]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=120)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"命令执行失败: {result.stderr}")
            return None
    except FileNotFoundError:
        print("openclaw命令未找到")
        return None
    except subprocess.TimeoutExpired:
        print("请求超时")
        return None
    except Exception as e:
        print(f"调用失败: {e}")
        return None

def generate_detailed_analysis():
    """生成详细分析"""
    
    # 视频信息
    video_info = {
        "title": "The Sermon on the Mount | Lecture One",
        "duration": "64分钟",
        "speaker": "Jordan B Peterson",
        "speaker_title": "临床心理学家、前多伦多大学教授",
        "series": "Peterson Academy圣经解读系列",
        "url": "https://www.youtube.com/watch?v=Wv7lEyck2mg",
        "description": "Jordan Peterson从心理学、历史和哲学角度深度解读《圣经·马太福音》第5-7章的'登山宝训'，探讨其与现代心理学、个人责任和社会秩序的关联。"
    }
    
    # 构建详细的提示词
    prompt = f"""# 视频详细分析任务

## 视频信息
- **标题**: {video_info['title']}
- **时长**: {video_info['duration']}
- **讲师**: {video_info['speaker']} ({video_info['speaker_title']})
- **系列**: {video_info['series']}
- **描述**: {video_info['description']}

## 分析要求
请为这个64分钟的讲座视频生成一份极其详细的学习笔记，要求如下：

### 1. 视频概述 (200-300字)
- 核心主题和讲师背景
- 视频的结构和主要内容
- 观看这个视频的价值

### 2. 时间线详细分析 (按10分钟分段，每个分段100-150字)
- 0-10分钟：开场和引言
- 10-20分钟：第一部分内容
- 20-30分钟：第二部分内容
- 30-40分钟：第三部分内容
- 40-50分钟：第四部分内容
- 50-60分钟：第五部分内容
- 60-64分钟：总结和结论

### 3. 关键概念深度解析 (每个概念100-150字)
- 登山宝训 (Sermon on the Mount)
- 八福 (Beatitudes)
- 荣格心理学 (Jungian Psychology)
- 认知考古学 (Cognitive Archaeology)
- 道德发展理论 (Moral Development Theory)
- 意义心理学 (Psychology of Meaning)
- 叙事心理学 (Narrative Psychology)

### 4. 心理学理论应用 (每个理论100-150字)
- 荣格的集体无意识理论如何应用于圣经解读
- 科尔伯格的道德发展阶段理论在八福中的体现
- 维克多·弗兰克的意义疗法与登山宝训的关联
- 积极心理学视角下的八福分析

### 5. 学习收获与应用 (每个收获80-100字)
- 对个人成长的启示
- 对道德发展的理解
- 对意义追求的指导
- 对冲突解决的启发
- 对社会责任的思考

### 6. 批判性分析与不同视角 (每个视角100-150字)
- 心理学解读的局限性
- 女性主义视角的缺失
- 跨文化视角的不足
- 历史批判方法的对比
- 解放神学的不同解读

### 7. 延伸学习资源
- 推荐书籍（每本简要介绍）
- 推荐视频/讲座
- 学术论文/研究
- 实践练习建议

### 8. 学习计划建议
- 初次观看的学习重点
- 二次观看的深度思考
- 日常实践的具体方法
- 长期学习的规划

## 输出要求
1. 使用中文，专业但易懂
2. 总字数不少于3000字
3. 结构清晰，层次分明
4. 包含具体的时间标记和例子
5. 既有深度又有实用性

请开始生成详细的学习笔记："""

    print("正在生成详细分析...")
    print(f"视频标题: {video_info['title']}")
    print(f"视频时长: {video_info['duration']}")
    print("=" * 60)
    
    # 调用模型
    response = call_openclaw_model(prompt)
    
    if response:
        # 保存结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"detailed_analysis_{timestamp}.md"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# {video_info['title']} - 详细分析\n\n")
            f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**视频信息**:\n")
            f.write(f"- 标题: {video_info['title']}\n")
            f.write(f"- 时长: {video_info['duration']}\n")
            f.write(f"- 讲师: {video_info['speaker']}\n")
            f.write(f"- 系列: {video_info['series']}\n")
            f.write(f"- URL: {video_info['url']}\n\n")
            f.write("=" * 60 + "\n\n")
            f.write(response)
        
        print(f"分析完成！已保存到: {output_file}")
        
        # 统计字数
        word_count = len(response)
        print(f"总字数: {word_count}字")
        
        # 显示部分内容预览
        print("\n部分内容预览:")
        print("=" * 60)
        lines = response.split('\n')
        for i, line in enumerate(lines[:20]):
            print(line)
        print("...")
        
        return output_file
    else:
        print("分析生成失败")
        return None

def create_feishu_document(analysis_file: str):
    """创建飞书文档"""
    if not os.path.exists(analysis_file):
        print(f"文件不存在: {analysis_file}")
        return
    
    # 读取分析内容
    with open(analysis_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 截取前5000字符（飞书文档限制）
    if len(content) > 5000:
        content = content[:5000] + "\n\n...（内容过长，完整版请查看本地文件）"
    
    print(f"准备创建飞书文档，内容长度: {len(content)}字符")
    
    # 这里可以添加飞书API调用代码
    # 由于我们已经有了飞书文档创建功能，可以直接使用
    
    return content

if __name__ == "__main__":
    print("开始生成Jordan Peterson视频的详细分析...")
    print("=" * 60)
    
    # 生成详细分析
    analysis_file = generate_detailed_analysis()
    
    if analysis_file:
        print(f"\n分析文件: {analysis_file}")
        print("\n下一步：")
        print("1. 查看完整分析文件")
        print("2. 将分析同步到飞书文档")
        print("3. 分享给其他学习者")
    else:
        print("分析生成失败")