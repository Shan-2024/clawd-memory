# Lip 智能学习助手 — 实施计划

**基于设计方案**: [2026-02-25-lip-learning-assistant-design.md](./2026-02-25-lip-learning-assistant-design.md)

---

## 实施阶段

### Phase 1: 基础架构搭建 (Day 1)

#### 1.1 项目结构创建
```
the-gallaghers/lip/
├── src/
│   ├── config/
│   │   └── manager.py      # 配置管理
│   ├── youtube/
│   │   ├── extractor.py    # YouTube提取
│   │   └── parser.py       # 链接解析
│   ├── ai/
│   │   └── analyzer.py     # AI分析模块
│   ├── storage/
│   │   ├── local.py        # 本地存储
│   │   └── feishu_sync.py  # 飞书同步
│   └── feishu/
│       └── bot.py          # 飞书交互
├── notebooks/              # 笔记存储目录
├── config.json             # 配置文件
├── requirements.txt        # Python依赖
└── cron_job.py            # 定时任务入口
```

#### 1.2 核心文件创建
- [ ] `config.json` 模板
- [ ] `requirements.txt` (yt-dlp, requests, etc.)
- [ ] `.gitignore` (忽略notebooks/内容)

#### 1.3 Gallagher集成
- [ ] 在 `index.html` 中添加 Lip 角色
- [ ] 创建基础Web面板框架

---

### Phase 2: YouTube提取模块 (Day 1-2)

#### 2.1 功能实现
- [ ] `extractor.py`: 频道视频列表获取
- [ ] `extractor.py`: 单视频字幕提取
- [ ] `parser.py`: 链接类型识别（频道/播放列表/单视频）

#### 2.2 技术细节
- 使用 `yt-dlp` 提取字幕
- 代理配置（避免IP被封）
- 错误处理和重试机制

#### 2.3 测试验证
- [ ] 测试频道视频列表获取
- [ ] 测试字幕提取
- [ ] 测试无字幕视频处理

---

### Phase 3: AI分析模块 (Day 2)

#### 3.1 Prompt设计
- [ ] 摘要生成 Prompt
- [ ] 标签生成 Prompt
- [ ] 名词识别与科普 Prompt

#### 3.2 API集成
- [ ] `analyzer.py`: Kimi API调用封装
- [ ] Token限制处理（截断长文本）
- [ ] 错误重试机制

#### 3.3 输出格式化
- [ ] Markdown生成
- [ ] JSON元数据生成

---

### Phase 4: 飞书交互 (Day 2-3)

#### 4.1 命令解析
- [ ] `@Lip 添加博主 <URL>`
- [ ] `@Lip 状态`
- [ ] `@Lip 删除博主 <博主名>`
- [ ] `@Lip 同步 <博主名> 到NotebookLM`

#### 4.2 消息模板
- [ ] 添加成功通知
- [ ] 每日分析报告
- [ ] 错误告警

#### 4.3 OpenClaw集成
- [ ] 在OpenClaw配置中添加Lip命令处理器

---

### Phase 5: 定时任务 (Day 3)

#### 5.1 核心逻辑
- [ ] `cron_job.py`: 每日扫描逻辑
- [ ] 视频去重（避免重复分析）
- [ ] 进度更新

#### 5.2 OpenClaw Cron配置
```yaml
# 添加到OpenClaw配置
cron:
  lip_daily_analysis:
    schedule: "0 2 * * *"  # 每天凌晨2点
    command: "python /home/admin/.openclaw/workspace/the-gallaghers/lip/cron_job.py"
```

#### 5.3 日志记录
- [ ] 分析日志
- [ ] 错误日志

---

### Phase 6: Web面板 (Day 3-4)

#### 6.1 页面开发
- [ ] 仪表板（博主卡片、进度条）
- [ ] 笔记列表（搜索、筛选）
- [ ] 科普词典（名词索引）

#### 6.2 API接口
- [ ] 获取博主列表
- [ ] 获取笔记列表
- [ ] 获取科普词典

---

### Phase 7: NotebookLM同步 (Day 4)

#### 7.1 功能实现
- [ ] 调用 `notebooklm` CLI创建笔记本
- [ ] 批量添加视频链接
- [ ] 同步状态跟踪

#### 7.2 飞书命令
- [ ] `@Lip 同步 <博主名> 到NotebookLM`

---

### Phase 8: 测试与优化 (Day 4-5)

#### 8.1 功能测试
- [ ] 端到端测试（添加博主 → 分析 → 查看笔记）
- [ ] 边界测试（无字幕、长视频、特殊字符）

#### 8.2 性能优化
- [ ] YouTube提取优化
- [ ] AI调用并发控制

#### 8.3 文档完善
- [ ] README.md
- [ ] 使用说明

---

## 依赖清单

### Python包
```
yt-dlp
requests
python-dateutil
```

### 外部工具
- `yt-dlp`: YouTube视频/字幕提取
- `notebooklm`: NotebookLM CLI（已安装）

### API密钥/配置
- Kimi API Key（使用OpenClaw内置）
- YouTube代理配置（如需）

---

## 风险与应对

| 风险 | 可能性 | 影响 | 应对措施 |
|------|--------|------|----------|
| YouTube IP被封 | 中 | 高 | 使用代理池，降低请求频率 |
| AI API限流 | 中 | 中 | 添加重试和退避机制 |
| 视频无字幕 | 高 | 低 | 跳过并标记，发送通知 |
| 存储空间不足 | 低 | 中 | 定期清理旧笔记，添加压缩 |

---

## 验收检查表

- [ ] 能成功添加YouTube博主
- [ ] 24小时内自动生成第一条笔记
- [ ] 每条笔记包含：摘要、字幕、科普、标签
- [ ] 飞书状态命令显示准确进度
- [ ] 科普板块识别至少3个名词
- [ ] 能同步到NotebookLM
- [ ] Web面板可正常浏览笔记
- [ ] 系统稳定运行7天

---

## 开始实施

**下一步动作**: 创建项目目录结构和基础文件
