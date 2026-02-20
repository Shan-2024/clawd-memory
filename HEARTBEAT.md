# HEARTBEAT.md

## 自动同步任务

每 10 分钟自动从 GitHub 拉取最新记忆：

```bash
cd /home/admin/clawd && git pull origin main
```

## 检查频率

- 云端服务器：每 10 分钟检查一次
- Mac 端：需要手动 push（或用 crontab 自动）

---

*配置时间: 2026-02-21*
