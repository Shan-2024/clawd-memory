# AI搜索工具横评 - Remotion视频项目

这个项目用 Remotion 制作了一个 30 秒的 AI 搜索工具测评视频，对比 Kimi、秘塔、360AI、天工四个工具。

## 📁 项目结构

```
ai-search-comparison/
├── src/
│   ├── index.tsx              # 入口文件，定义视频配置
│   ├── ComparisonVideo.tsx    # 主组件，组合所有场景
│   └── scenes/                # 场景组件
│       ├── IntroScene.tsx     # 片头 (0-3秒)
│       ├── ToolIntroScene.tsx # 工具介绍 (3-7秒)
│       ├── DimensionScene.tsx # 单个维度评分 (每维度5秒)
│       ├── ComparisonScene.tsx# 综合对比 (5秒)
│       └── OutroScene.tsx     # 片尾总结 (3秒)
├── package.json
├── tsconfig.json
└── README.md
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd ai-search-comparison
npm install
```

### 2. 启动预览

```bash
npm start
```

这会打开 Remotion Studio，你可以：
- 实时预览视频
- 拖动时间轴查看每一帧
- 调整参数后自动刷新

### 3. 导出视频

```bash
npm run build
```

视频会导出到 `out/video.mp4`

## 🎨 如何修改内容

### 修改测评分数

打开 `src/ComparisonVideo.tsx`，找到 `<DimensionScene>` 组件，修改 `scores` 数组：

```tsx
<DimensionScene 
  dimension={DIMENSIONS[0]} 
  scores={[4.5, 4, 3.5, 4]}  // ← 改这里的数字
/>
```

分数顺序对应：Kimi、秘塔、360AI、天工

### 修改测评维度

在 `src/ComparisonVideo.tsx` 中找到 `DIMENSIONS` 数组：

```tsx
export const DIMENSIONS = [
  { key: 'convenience', name: '体验便捷度', icon: '⚡', description: '打开即用，无需学习成本' },
  // 添加或修改这里
];
```

### 调整视频长度

在 `src/index.tsx` 中修改：

```tsx
export const VIDEO_DURATION_IN_FRAMES = 900; // 30秒 (30fps × 30s)
```

### 修改工具信息

在 `src/ComparisonVideo.tsx` 中修改 `TOOLS` 数组：

```tsx
export const TOOLS = [
  { name: 'Kimi', color: '#00BFFF', icon: 'K' },
  // 添加或修改
];
```

## 📊 默认测评维度

1. **体验便捷度** - 打开即用，无需学习成本
2. **答案准确度** - 信息准确，不胡说八道
3. **内容丰富度** - 答案全面，有深度有广度
4. **来源可靠性** - 引用清晰，可追溯验证
5. **响应速度** - 秒级响应，不卡顿
6. **生活关联度** - 购物/美食/出行等实用场景

## 🎯 视频流程

| 时间 | 场景 | 说明 |
|-----|------|-----|
| 0-3s | 片头 | 标题动画 |
| 3-7s | 工具介绍 | 四个工具卡片飞入 |
| 7-12s | 体验便捷度 | 进度条动画 |
| 12-17s | 答案准确度 | 进度条动画 |
| 17-22s | 内容丰富度 | 进度条动画 |
| 22-27s | 综合对比 | 评分表格 |
| 27-30s | 片尾总结 | 使用建议 |

## 💡 进阶技巧

### 添加更多维度

1. 在 `DIMENSIONS` 数组中添加新维度
2. 在 `ComparisonVideo.tsx` 中复制一个 `<Sequence>`
3. 调整 `from` 和 `durationInFrames` 避免重叠

### 修改配色

每个工具的颜色定义在 `TOOLS` 数组中，使用十六进制颜色码：
- `#00BFFF` - Kimi 蓝
- `#FF6B6B` - 秘塔红
- `#4ECDC4` - 360AI 青
- `#FFE66D` - 天工黄

### 添加动画

Remotion 提供了丰富的动画 API：
- `interpolate()` - 数值插值
- `useCurrentFrame()` - 获取当前帧
- `useVideoConfig()` - 获取视频配置

示例：让一个元素从下方飞入
```tsx
const translateY = interpolate(frame, [0, 30], [100, 0]);
return <div style={{ transform: `translateY(${translateY}px)` }} />;
```

## 📚 参考文档

- [Remotion 官方文档](https://www.remotion.dev/docs)
- [Remotion API 参考](https://www.remotion.dev/docs/api)

## 🐛 常见问题

**Q: npm install 报错？**  
A: 确保 Node.js 版本 >= 18

**Q: 预览窗口空白？**  
A: 检查浏览器控制台是否有报错，通常是组件语法错误

**Q: 导出视频失败？**  
A: 确保已安装 FFmpeg：`npm install @remotion/cli`

**Q: 想导出不同分辨率？**  
A: 修改 `src/index.tsx` 中的 `width` 和 `height`
- 竖屏 9:16: 1080 × 1920 (抖音/小红书)
- 横屏 16:9: 1920 × 1080 (B站/YouTube)
