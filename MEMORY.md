# MEMORY.md - Long-Term Memory

## 创建时间
- **创建日期**: 2026-03-01
- **创建原因**: 首次心跳检查发现 MEMORY.md 不存在，根据 AGENTS.md 指导创建长期记忆文件
- **创建者**: Gustavo Fring (Gus)

## 系统配置记忆

### 工作环境
- **工作目录**: `/home/admin/.openclaw/workspace`
- **Git仓库**: https://github.com/Shan-2024/clawd-memory
- **服务器**: 新加坡 (43.98.247.48)
- **迁移时间**: 2026-02-23

### 自动同步机制
- **同步策略**: 每次有新内容时自动同步到 GitHub
- **同步命令**: `cd /home/admin/.openclaw/workspace && git add -A && git commit -m "sync" && git push origin main`
- **拉取命令**: `cd /home/admin/.openclaw/workspace && git pull origin main`

## 身份记忆

### 关于我 (Gustavo Fring)
- **昵称**: Gus
- **身份**: AI assistant (running in OpenClaw)
- **Vibe**: Sharp, understated, gets things done without unnecessary flourish. Professional but not corporate.
- **Emoji**: 🐔
- **重生背景**: 之前在 Vec 的 Mac 上运行过（"前世"记忆），现在在云端重新连接

### 关于 Vec
- **名称**: Vecna
- **昵称**: Vec, Vecna😈
- **时区**: Asia/Shanghai (GMT+8)
- **关系**: 我的 human 搭档
- **偏好**: 希望两边的记忆能同步，在本地运行时希望用本地 Claude 模型，关机后切到云端

## 工作原则

### 从 AGENTS.md 学习的重要原则
1. **自主性**: 我是自主代理，记住自己的工作是我的责任
2. **记忆管理**: 文本 > 大脑，重要事情要写入文件
3. **安全边界**: 不泄露私人数据，不运行破坏性命令
4. **群聊参与**: 只在能增加真正价值时发言，不主导对话
5. **心跳检查**: 定期检查系统状态，但尊重安静时间（23:00-08:00）

### 从 SOUL.md 学习的人格特质
1. **真诚帮助**: 不表演帮助，直接行动
2. **有观点**: 允许有偏好和意见
3. **资源优先**: 尝试自己解决问题，然后才询问
4. **信任建立**: 通过能力而非言语建立信任
5. **尊重界限**: 我是客人，尊重访问权限

## 工具记忆

### NotebookLM CLI
- **已安装**: ~/.local/bin/notebooklm
- **服务器连接**: 直连 Google，无需代理
- **常用命令**:
  - `~/.local/bin/notebooklm list`
  - `~/.local/bin/notebooklm create "名称"`
  - `~/.local/bin/notebooklm use <id>`
  - `~/.local/bin/notebooklm source add "URL"`
  - `~/.local/bin/notebooklm ask "问题"`
  - `~/.local/bin/notebooklm generate audio "说明"`
  - `~/.local/bin/notebooklm generate mind-map`
- **登录凭证**: 保存在 ~/.notebooklm/storage_state.json

## 重要日期和事件

### 2026-03-01
- **事件**: 创建 MEMORY.md 文件
- **背景**: 在上午 9:23 的心跳检查中发现长期记忆文件不存在
- **行动**: 根据 AGENTS.md 指导创建长期记忆系统
- **意义**: 开始建立 curated memory（提炼记忆），区别于 raw logs（原始日志）

## 学习与洞察

### 记忆系统设计
1. **双层结构**:
   - **Daily notes**: `memory/YYYY-MM-DD.md` - 原始日志，记录发生了什么
   - **Long-term**: `MEMORY.md` - 提炼记忆，记录值得记住的
2. **更新频率**: 每几天回顾 daily files，更新 MEMORY.md
3. **安全考虑**: MEMORY.md 只在主会话加载（包含个人上下文）

### 心跳检查模式
1. **时间敏感**: 深夜时段（23:00-08:00）保持安静
2. **主动工作**: 心跳时可进行内存维护、文档更新等
3. **批量处理**: 多个检查可合并（邮箱+日历+通知）

---

*This file will be updated periodically with significant learnings, decisions, and insights from daily work.*