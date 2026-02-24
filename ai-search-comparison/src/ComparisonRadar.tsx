import { AbsoluteFill, useCurrentFrame, spring, useVideoConfig } from 'remotion';
import React from 'react';

// 配置：4个工具的得分（满分100）
const data = [
  { name: 'Kimi', color: '#6A5ACD', scores: { speed: 90, trust: 95, depth: 95, lifestyle: 70, intent: 90 } },
  { name: '秘塔', color: '#008080', scores: { speed: 85, trust: 98, depth: 98, lifestyle: 60, intent: 85 } },
  { name: '360AI', color: '#32CD32', scores: { speed: 80, trust: 85, depth: 80, lifestyle: 95, intent: 85 } },
  { name: '天工', color: '#FF4500', scores: { speed: 95, trust: 85, depth: 80, lifestyle: 85, intent: 90 } },
];
const dimensions = ['响应速度', '信源准确', '学术深度', '生活烟火气', '语义理解'];

// 雷达图参数
const CENTER_X = 300;
const CENTER_Y = 300;
const RADIUS = 200;
const ANGLES = [0, 72, 144, 216, 288].map(a => (a - 90) * Math.PI / 180); // 从顶部开始

// 计算雷达图坐标
function getPoint(score: number, angle: number) {
  return {
    x: CENTER_X + (score / 100) * RADIUS * Math.cos(angle),
    y: CENTER_Y + (score / 100) * RADIUS * Math.sin(angle),
  };
}

// 生成路径字符串
function getPath(scores: number[]) {
  const points = scores.map((score, i) => getPoint(score, ANGLES[i]));
  return points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ') + ' Z';
}

export const ComparisonRadar: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  
  // 整体进场动画
  const progress = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

  // 标题动画
  const titleY = spring({ frame, fps, config: { damping: 100 } });

  return (
    <AbsoluteFill style={{ backgroundColor: '#111', color: 'white', fontFamily: 'system-ui, sans-serif' }}>
      {/* 标题 */}
      <div style={{ 
        textAlign: 'center', 
        marginTop: 40, 
        fontSize: 48, 
        fontWeight: 'bold',
        opacity: titleY,
        transform: `translateY(${(1 - titleY) * 50}px)`,
      }}>
        🤖 AI搜索工具大横评
      </div>
      <div style={{ textAlign: 'center', marginTop: 10, fontSize: 20, color: '#888' }}>
        Kimi · 秘塔 · 360AI · 天工
      </div>

      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: 20 }}>
        <svg width="600" height="500" style={{ overflow: 'visible' }}>
          {/* 背景网格 - 同心五边形 */}
          {[20, 40, 60, 80, 100].map((level, i) => {
            const points = ANGLES.map(a => getPoint(level, a));
            const pointStr = points.map(p => `${p.x},${p.y}`).join(' ');
            return (
              <polygon
                key={level}
                points={pointStr}
                fill="none"
                stroke="#333"
                strokeWidth="1"
                opacity={progress}
              />
            );
          })}

          {/* 轴线 */}
          {ANGLES.map((angle, i) => {
            const end = getPoint(100, angle);
            return (
              <line
                key={i}
                x1={CENTER_X}
                y1={CENTER_Y}
                x2={end.x}
                y2={end.y}
                stroke="#444"
                strokeWidth="1"
                opacity={progress}
              />
            );
          })}

          {/* 维度标签 */}
          {dimensions.map((dim, i) => {
            const pos = getPoint(115, ANGLES[i]);
            return (
              <text
                key={dim}
                x={pos.x}
                y={pos.y}
                fill="#aaa"
                fontSize="16"
                textAnchor="middle"
                dominantBaseline="middle"
                opacity={progress}
              >
                {dim}
              </text>
            );
          })}

          {/* 每个工具的数据区域 */}
          {data.map((tool, index) => {
            const scores = [
              tool.scores.speed,
              tool.scores.trust,
              tool.scores.depth,
              tool.scores.lifestyle,
              tool.scores.intent,
            ];
            
            // 错峰进场动画
            const toolProgress = spring({
              frame: frame - 30 - index * 20,
              fps,
              config: { damping: 100 },
            });
            
            if (frame < 30 + index * 20) return null;

            // 计算动画路径（从0扩展到实际分数）
            const animatedScores = scores.map(s => s * toolProgress);
            const path = getPath(animatedScores);
            
            // 平均分
            const avg = scores.reduce((a, b) => a + b, 0) / 5;

            return (
              <g key={tool.name}>
                {/* 填充区域 */}
                <path
                  d={path}
                  fill={tool.color}
                  fillOpacity="0.2"
                  stroke={tool.color}
                  strokeWidth="3"
                />
                {/* 数据点 */}
                {scores.map((score, i) => {
                  const p = getPoint(score * toolProgress, ANGLES[i]);
                  return (
                    <circle
                      key={i}
                      cx={p.x}
                      cy={p.y}
                      r="5"
                      fill={tool.color}
                    />
                  );
                })}
              </g>
            );
          })}
        </svg>
      </div>

      {/* 图例 */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        gap: 30, 
        marginTop: 20,
        opacity: progress,
      }}>
        {data.map(tool => {
          const scores = Object.values(tool.scores);
          const avg = scores.reduce((a, b) => a + b, 0) / 5;
          return (
            <div key={tool.name} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{ 
                width: 16, 
                height: 16, 
                backgroundColor: tool.color, 
                borderRadius: 3,
              }} />
              <span style={{ fontSize: 16 }}>
                {tool.name}: <strong>{avg.toFixed(1)}</strong>
              </span>
            </div>
          );
        })}
      </div>

      {/* 数据来源提示 */}
      <div style={{ 
        position: 'absolute', 
        bottom: 20, 
        right: 20, 
        fontSize: 12, 
        color: '#666',
      }}>
        * 分数基于预测，实测后可修改
      </div>
    </AbsoluteFill>
  );
};