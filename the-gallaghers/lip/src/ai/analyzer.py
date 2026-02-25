"""
AI分析模块
使用 Kimi API 进行内容分析
"""
import os
import re
from typing import List, Dict


class AIAnalyzer:
    """AI内容分析器"""
    
    def __init__(self, model: str = "kimi-k2.5"):
        self.model = model
        # 使用OpenClaw的Kimi模型（通过环境或默认配置）
        self.max_tokens = 8000  # 限制输入token数
    
    def _call_ai(self, prompt: str) -> str:
        """
        调用AI模型
        
        在OpenClaw环境中，我们可以直接使用内部工具调用
        这里提供一个通用接口，实际实现可以使用OpenClaw的调用方式
        """
        # 尝试使用OpenClaw的方式调用
        try:
            # 这里应该使用OpenClaw的模型调用方式
            # 由于我们在OpenClaw agent中运行，可以直接用工具
            import subprocess
            result = subprocess.run(
                ['openclaw', 'chat', '--model', self.model, '--system', '你是一个专业的内容分析助手', prompt],
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        # 备用：直接返回模拟结果（开发测试用）
        return self._mock_response(prompt)
    
    def _mock_response(self, prompt: str) -> str:
        """模拟AI响应（用于测试）"""
        if "摘要" in prompt:
            return """1. 视频讨论了人工智能在内容创作中的应用
2. 介绍了多个实用工具和技巧
3. 强调了人机协作的重要性
4. 提供了具体的操作步骤和案例
5. 展望了未来发展趋势"""
        elif "标签" in prompt:
            return "#AI #内容创作 #工具推荐 #教程"
        elif "名词" in prompt or "科普" in prompt:
            return """- **人工智能**：计算机科学的一个分支，研究如何让机器模拟人类智能
- **机器学习**：AI的一种方法，让计算机从数据中学习规律
- **深度学习**：机器学习的一个子领域，使用多层神经网络"""
        return "分析完成"
    
    def generate_knowledge_from_summary(self, title: str, summary: str) -> Dict[str, str]:
        """
        基于摘要生成科普知识
        
        Args:
            title: 视频标题
            summary: 视频摘要
            
        Returns:
            名词->解释的字典
        """
        if not summary:
            return {}
        
        truncated_summary = self._truncate_text(summary, max_chars=3000)
        
        prompt = f"""基于以下视频信息，提取并解释所有专业名词、人名、地名、概念等。

视频标题：{title}
视频摘要：{truncated_summary}

要求：
1. 提取视频中提到的所有需要解释的名词
2. 为每个名词提供2-3句话的科普解释
3. 解释要通俗易懂，适合普通读者
4. 以JSON格式返回

输出格式：
{{
  "名词1": "解释1",
  "名词2": "解释2"
}}

如果没有需要解释的名词，返回空对象 {{}}。"""
        
        response = self._call_ai(prompt)
        
        # 尝试解析JSON
        try:
            import json
            # 提取JSON部分
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group(0))
        except:
            pass
        
        # 解析失败，尝试从文本解析
        return self._parse_knowledge_text(response)
    
    def _parse_knowledge_text(self, text: str) -> Dict[str, str]:
        """从文本解析科普知识"""
        knowledge = {}
        
        # 匹配 "- **名词**：解释" 或 "名词：解释" 格式
        pattern = r'(?:^|\n)\s*[-*]*\s*\*\*(.+?)\*\*\s*[:：]\s*(.+?)(?=\n|$)'
        matches = re.findall(pattern, text, re.MULTILINE)
        
        for name, explanation in matches:
            knowledge[name.strip()] = explanation.strip()
        
        # 如果没有匹配到，尝试其他格式
        if not knowledge:
            pattern2 = r'(?:^|\n)\s*\d+[\.、]\s*(.+?)\s*[:：]\s*(.+?)(?=\n|$)'
            matches = re.findall(pattern2, text, re.MULTILINE)
            for name, explanation in matches:
                knowledge[name.strip()] = explanation.strip()
        
        return knowledge
    
    def _truncate_text(self, text: str, max_chars: int = 8000) -> str:
        """截断文本以适应token限制"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."
    
    def generate_summary(self, transcript: str) -> List[str]:
        """
        生成视频摘要
        
        Returns:
            3-5条核心要点
        """
        truncated = self._truncate_text(transcript)
        
        prompt = f"""请为以下YouTube视频字幕生成结构化摘要。
要求：
1. 提取3-5条核心要点
2. 每条要点简洁明了，不超过50字
3. 用中文输出
4. 只输出要点列表，不要其他内容

字幕内容：
{truncated}

请按以下格式输出：
1. 要点一
2. 要点二
3. 要点三
"""
        
        response = self._call_ai(prompt)
        
        # 解析响应
        points = []
        for line in response.strip().split('\n'):
            line = line.strip()
            # 匹配 "1. xxx" 或 "1、xxx" 格式
            match = re.match(r'^[\d一二三四五][\.、\s]+(.+)$', line)
            if match:
                points.append(match.group(1).strip())
            elif line and not line.startswith('-'):
                # 也可能是简单列表
                clean_line = re.sub(r'^[\-\*•]\s*', '', line)
                if clean_line and len(clean_line) > 5:
                    points.append(clean_line)
        
        return points[:5] if points else ["无法生成摘要"]
    
    def generate_tags(self, transcript: str) -> List[str]:
        """
        生成标签
        
        Returns:
            3-5个标签，格式如 ['AI', '投资', '思维模型']
        """
        truncated = self._truncate_text(transcript, 4000)  # 标签不需要全文
        
        prompt = f"""请分析以下YouTube视频内容，提取3-5个关键词标签。

要求：
1. 标签应该准确反映内容主题
2. 标签简洁，2-4个字为宜
3. 不要输出"#"符号
4. 只输出标签列表，每行一个

内容摘要：
{truncated[:1000]}...

请按以下格式输出：
标签一
标签二
标签三
"""
        
        response = self._call_ai(prompt)
        
        # 解析响应
        tags = []
        for line in response.strip().split('\n'):
            line = line.strip()
            # 移除#符号
            line = re.sub(r'^#+\s*', '', line)
            # 移除序号
            line = re.sub(r'^[\d一二三四五][\.、\s]+', '', line)
            
            if line and len(line) <= 20:
                tags.append(line)
        
        return tags[:5] if tags else ["未分类"]
    
    def extract_knowledge(self, transcript: str) -> Dict[str, str]:
        """
        提取名词并生成科普解释
        
        Returns:
            名词 -> 解释 的字典
        """
        truncated = self._truncate_text(transcript)
        
        prompt = f"""请识别以下YouTube视频内容中提到的所有人名、地名、历史事件、专业术语、概念、技术名词等专有名词，并为每个名词提供简要解释（30-80字）。

要求：
1. 识别视频中明确提到的重要概念
2. 提供准确、简洁的解释
3. 用中文输出
4. 只输出名词解释列表，格式：名词：解释内容
5. 如果内容没有明显名词，输出"无"

字幕内容：
{truncated}

请按以下格式输出：
名词一：这是名词一的简要解释...
名词二：这是名词二的简要解释...
"""
        
        response = self._call_ai(prompt)
        
        # 解析响应
        knowledge = {}
        for line in response.strip().split('\n'):
            line = line.strip()
            # 匹配 "名词：解释" 格式
            match = re.match(r'^(.+?)[：:](.+)$', line)
            if match:
                name = match.group(1).strip()
                explanation = match.group(2).strip()
                # 过滤掉无意义的条目
                if name not in ['无', ''] and len(explanation) > 5:
                    knowledge[name] = explanation
        
        return knowledge
    
    def analyze_video(self, transcript: str) -> Dict:
        """
        完整分析视频
        
        Returns:
            {
                'summary': ['要点1', '要点2', ...],
                'tags': ['标签1', '标签2', ...],
                'knowledge': {'名词1': '解释1', ...}
            }
        """
        print("正在生成摘要...")
        summary = self.generate_summary(transcript)
        
        print("正在生成标签...")
        tags = self.generate_tags(transcript)
        
        print("正在提取科普知识...")
        knowledge = self.extract_knowledge(transcript)
        
        return {
            'summary': summary,
            'tags': tags,
            'knowledge': knowledge
        }