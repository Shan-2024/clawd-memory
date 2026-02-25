# YouTube Cookies 配置指南

## 问题
YouTube现在会检测自动化工具，要求登录验证（"Sign in to confirm you're not a bot"）。

## 解决方案
使用你的YouTube登录cookies，让yt-dlp以你的身份访问。

## 获取Cookies步骤

### 方法1：浏览器扩展（推荐）

1. **安装扩展**
   - Chrome/Edge: 安装 "Get cookies.txt LOCALLY"
   - Firefox: 安装 "cookies.txt"

2. **登录YouTube**
   - 在浏览器中访问 youtube.com
   - 确保你已登录Google账号

3. **导出Cookies**
   - 点击扩展图标
   - 点击 "Export" 或 "Copy"
   - 保存为 `youtube_cookies.txt`

4. **上传到服务器**
   ```bash
   # 在本机执行
   scp youtube_cookies.txt admin@43.98.247.48:/home/admin/.openclaw/workspace/the-gallaghers/lip/cookies/
   ```

### 方法2：开发者工具

1. 在YouTube页面按 F12 打开开发者工具
2. 切换到 Application/应用 标签
3. 左侧选择 Cookies → https://www.youtube.com
4. 复制所有cookie，格式化为Netscape格式

### 方法3：提供给我配置

直接在飞书中发送你的cookies内容（注意安全风险）：
```
.youtube.com	TRUE	/	TRUE	...	...
```

## Cookie文件格式

文件必须是Netscape格式：
```
# Netscape HTTP Cookie File
.youtube.com	TRUE	/	TRUE	...	...
.youtube.com	TRUE	/	TRUE	...	...
```

## 安全提示

⚠️ **Cookies包含你的登录信息**：
- 不要分享给不信任的人
- 定期更新密码
- 如发现异常，立即退出所有设备登录

## 测试

上传cookies后，测试是否有效：
```bash
cd /home/admin/.openclaw/workspace/the-gallaghers/lip
python -c "
from src.youtube.extractor import YouTubeExtractor
ext = YouTubeExtractor()
info = ext.get_video_info('https://www.youtube.com/watch?v=h69SwIn-bA4')
print('成功:', info['title'])
"
```