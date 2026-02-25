# Lip 智能学习助手

**Lip** 是 Gallagher 家族中的智能学习助手，能够自动分析 YouTube 博主内容，生成结构化学习笔记。

## 🎯 功能特点

- **自动分析**: 每天自动分析每个博主的最新5条视频
- **智能摘要**: AI生成3-5条核心要点
- **标签分类**: 自动提取内容标签
- **科普板块**: 自动识别名词并提供解释
- **飞书交互**: 直接在飞书对话中操作
- **Web面板**: 可视化查看进度和笔记
- **本地存储**: 所有笔记保存为Markdown文件
- **NotebookLM同步**: 可选同步到NotebookLM

## 📁 项目结构

```
lip/
├── src/
│   ├── config/manager.py      # 配置管理
│   ├── youtube/
│   │   ├── extractor.py       # YouTube提取
│   │   └── parser.py          # 链接解析
│   ├── ai/analyzer.py         # AI分析模块
│   ├── storage/
│   │   ├── local.py           # 本地存储
│   │   └── feishu_sync.py     # 飞书同步（待实现）
│   └── feishu/bot.py          # 飞书交互
├── notebooks/                  # 笔记存储目录
├── config.json                # 配置文件
├── cron_job.py               # 定时任务入口
├── web_api.py                # Web API服务器
├── test_system.py            # 系统测试
└── requirements.txt          # Python依赖
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 确保已安装 yt-dlp
which yt-dlp

# 如果没有，安装到用户目录
pip3 install --user yt-dlp requests python-dateutil
```

### 2. 测试系统

```bash
cd /home/admin/.openclaw/workspace/the-gallaghers/lip
python test_system.py
```

### 3. 在飞书中使用

**添加博主**
```
@Lip 添加博主 https://youtube.com/@channelname
```

**查看进度**
```
@Lip 状态
```

**删除博主**
```
@Lip 删除博主 @channelname
```

**同步到NotebookLM**
```
@Lip 同步 @channelname 到NotebookLM
```

**查看科普词典**
```
@Lip 科普词典
```

### 4. Web面板

#### 启动API服务器

```bash
cd /home/admin/.openclaw/workspace/the-gallaghers/lip
python web_api.py

# 或使用其他端口
python web_api.py 8889
```

#### 访问Web面板

打开 Gallagher 系统，选择 **Lip** 角色，点击 **智能学习助手** 进入Web面板。

**Web面板功能：**
- 添加/删除YouTube博主
- 实时查看分析进度
- 浏览所有学习笔记
- 搜索笔记内容
- 查看科普词典
- 一键立即分析

#### API端点

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/status` | 系统状态统计 |
| GET | `/api/channels` | 频道列表 |
| POST | `/api/channels` | 添加频道 |
| POST | `/api/channels/delete` | 删除频道 |
| GET | `/api/notes` | 笔记列表（支持搜索） |
| GET | `/api/knowledge` | 科普词典 |
| POST | `/api/analyze` | 立即分析 |
| POST | `/api/sync/notebooklm` | 同步到NotebookLM |

## ⚙️ 配置OpenClaw定时任务

在OpenClaw配置中添加定时任务：

```yaml
# 添加到OpenClaw配置
cron:
  lip_daily_analysis:
    schedule: "0 2 * * *"  # 每天凌晨2点
    command: "python /home/admin/.openclaw/workspace/the-gallaghers/lip/cron_job.py"
```

## 📊 数据存储

### 本地笔记
所有笔记保存在 `notebooks/` 目录下，按博主分文件夹：

```
notebooks/
├── @channel1/
│   ├── 2025-01-15-视频标题.md
│   ├── 2025-01-16-另一个视频.md
│   └── summary.json
└── @channel2/
    └── ...
```

### 配置文件
`config.json` 存储博主列表和系统设置：

```json
{
  "version": "1.0",
  "max_channels": 10,
  "daily_limit_per_channel": 5,
  "channels": [
    {
      "id": "ch_20260225090000",
      "url": "https://youtube.com/@channelname",
      "name": "@channelname",
      "display_name": "博主名称",
      "added_at": "2026-02-25T09:00:00Z",
      "status": "active",
      "stats": {
        "total_videos": 127,
        "analyzed_count": 25,
        "last_analyzed_at": "2026-02-24T22:00:00Z"
      }
    }
  ]
}
```

## 🔧 开发说明

### 模块说明

1. **config/manager.py** - 配置管理
   - 添加/删除博主
   - 更新统计信息
   - 保存/加载配置

2. **youtube/extractor.py** - YouTube提取
   - 获取频道视频列表
   - 提取视频字幕
   - 获取视频信息

3. **ai/analyzer.py** - AI分析
   - 生成摘要
   - 提取标签
   - 识别名词并解释

4. **storage/local.py** - 本地存储
   - 保存笔记为Markdown
   - 管理笔记索引
   - 生成科普词典

5. **feishu/bot.py** - 飞书交互
   - 解析用户命令
   - 返回格式化回复
   - 处理各种操作

### 扩展开发

**添加新功能**:
1. 在 `src/` 下创建新模块
2. 在 `feishu/bot.py` 中添加命令处理
3. 在Web面板中添加对应界面

**修改AI分析**:
编辑 `ai/analyzer.py` 中的Prompt模板

**修改存储格式**:
编辑 `storage/local.py` 中的 `_generate_markdown()` 方法

## 🐛 故障排除

### 常见问题

1. **无法提取字幕**
   - 检查视频是否有字幕
   - 检查网络连接
   - 可能需要代理

2. **AI分析失败**
   - 检查OpenClaw的Kimi API配置
   - 检查网络连接

3. **飞书命令不响应**
   - 检查OpenClaw的飞书配置
   - 确保消息格式正确

4. **Web面板无法加载数据**
   - 检查API服务器是否运行：`curl http://localhost:8888/api/test`
   - 检查端口是否被占用
   - 查看API日志：`tail -f /tmp/web_api.log`

5. **CORS错误**
   - 确保Web面板和API在同一域名/端口，或修改`ALLOWED_ORIGINS`

### 日志查看

定时任务日志：
```bash
# 查看OpenClaw日志
openclaw logs
```

API服务器日志：
```bash
tail -f /tmp/web_api.log
```

## 📈 未来规划

- [x] **基础功能**: 飞书交互、定时任务、Web面板
- [x] **Web API**: 完整的RESTful API
- [ ] 飞书文档自动同步
- [ ] NotebookLM深度集成
- [ ] 多语言支持
- [ ] 视频类型自动分类
- [ ] 学习进度统计图表
- [ ] 移动端适配

## 📄 许可证

MIT License

---

**Lip** - 让学习自动化，让知识结构化 🎓