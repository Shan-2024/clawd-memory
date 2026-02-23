# HEARTBEAT.md

## 自动同步任务

每次有新内容时同步到 GitHub：

```bash
cd /home/admin/.openclaw/workspace && git add -A && git commit -m "sync" && git push origin main
```

从 GitHub 拉取：

```bash
cd /home/admin/.openclaw/workspace && git pull origin main
```

## 说明

- 工作目录：`/home/admin/.openclaw/workspace`
- 仓库：https://github.com/Shan-2024/clawd-memory
- 服务器：新加坡（43.98.247.48）

*迁移时间: 2026-02-23*
