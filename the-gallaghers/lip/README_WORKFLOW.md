# Lip 智能学习助手 - 完整工作流

## 🚀 工作流程

```
RSS获取视频列表 → NotebookLM分析 → AI生成科普 → 同步飞书
```

## 📋 流程详解

### 1. RSS获取视频列表
- 使用YouTube RSS feed（无需cookies）
- 获取频道最新视频ID和标题
- 自动识别已处理视频

### 2. NotebookLM分析
- 将视频链接推送到NotebookLM
- NotebookLM自动抓取YouTube内容
- 生成结构化分析

### 3. AI生成科普
- 向NotebookLM查询视频摘要
- 基于摘要让AI提取专业名词
- 生成通俗易懂的科普解释

### 4. 同步飞书
- 生成包含视频链接、科普知识的文档
- 自动同步到飞书文档
- 支持多频道管理

## 🎯 核心优势

| 功能 | 说明 |
|------|------|
| **无IP限制** | 使用RSS + NotebookLM，绕过YouTube反爬 |
| **自动科普** | AI自动生成名词解释，学习更深入 |
| **多渠道管理** | 支持10个博主同时监控 |
| **定时任务** | 每天自动抓取，无需人工干预 |

## 🛠️ 使用方法

### 定时任务（已配置）
```bash
# 每天2:00 AM自动执行
crontab -l
# 0 2 * * * cd /home/admin/.openclaw/workspace/the-gallaghers/lip && python3 lip_workflow.py
```

### 手动执行
```bash
cd /home/admin/.openclaw/workspace/the-gallaghers/lip
python3 lip_workflow.py
```

### 飞书机器人命令
```
@Lip 添加博主 https://youtube.com/@channelname
@Lip 状态
@Lip 同步飞书 @channelname
```

## 📊 数据存储

- **本地**: `notebooks/<channel_name>/<video_id>_workflow.json`
- **NotebookLM**: 自动创建"学习笔记 - <channel_name>"
- **飞书**: 每个频道一个文档"学习笔记 - <channel_name>"

## 🔧 文件说明

| 文件 | 说明 |
|------|------|
| `lip_workflow.py` | 主工作流脚本 |
| `cron_job_v2.py` | 旧版定时任务（备用） |
| `web_api.py` | Web API服务 |
| `src/ai/analyzer.py` | AI分析模块 |
| `src/storage/feishu_sync.py` | 飞书同步模块 |

## ⚠️ 注意事项

1. **RSS限制**: YouTube RSS只返回最近15个视频
2. **NotebookLM**: 需要已登录状态（~/.notebooklm/storage_state.json）
3. **AI分析**: 基于NotebookLM摘要生成科普，准确性依赖摘要质量

## 📝 更新日志

- 2026-02-25: 完整工作流上线（RSS + NotebookLM + 科普 + 飞书）
