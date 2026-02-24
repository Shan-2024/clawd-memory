import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';

const TOOLS = [
  { name: 'Kimi', color: '#00BFFF', scores: [4.5, 4, 4.5, 4, 4.5, 4] },
  { name: '秘塔', color: '#FF6B6B', scores: [4, 4.5, 4, 5, 4, 3.5] },
  { name: '360AI', color: '#4ECDC4', scores: [3.5, 3, 3.5, 3.5, 3.5, 4.5] },
  { name: '天工', color: '#FFE66D', scores: [4, 4, 4, 4, 4, 4] },
];

const DIMENSIONS = ['便捷度', '准确度', '丰富度', '来源', '速度', '生活'];

export const ComparisonScene = () => {
  const frame = useCurrentFrame();

  // 计算总分
  const totalScores = TOOLS.map(tool =>
    tool.scores.reduce((a, b) => a + b, 0).toFixed(1)
  );

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        background: '#0a0a0a',
        padding: '40px',
      }}
    >
      <h2
        style={{
          fontSize: '48px',
          color: '#ffffff',
          marginBottom: '40px',
          opacity: interpolate(frame, [0, 20], [0, 1]),
        }}
      >
        综合评分
      </h2>

      {/* 雷达图/表格 */}
      <div
        style={{
          width: '100%',
          maxWidth: '950px',
          background: '#111',
          borderRadius: '20px',
          padding: '30px',
          opacity: interpolate(frame, [20, 40], [0, 1]),
        }}
      >
        {/* 表头 */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '100px repeat(6, 1fr) 80px',
            gap: '10px',
            marginBottom: '20px',
            borderBottom: '2px solid #333',
            paddingBottom: '15px',
          }}
        >
          <span style={{ color: '#888', fontSize: '22px' }}>工具</span>
          {DIMENSIONS.map(dim => (
            <span
              key={dim}
              style={{ color: '#888', fontSize: '20px', textAlign: 'center' }}
            >
              {dim}
            </span>
          ))}
          <span style={{ color: '#00BFFF', fontSize: '22px', textAlign: 'center' }}>
            总分
          </span>
        </div>

        {/* 数据行 */}
        {TOOLS.map((tool, index) => {
          const delay = 40 + index * 15;
          const opacity = interpolate(frame, [delay, delay + 20], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

          return (
            <div
              key={tool.name}
              style={{
                display: 'grid',
                gridTemplateColumns: '100px repeat(6, 1fr) 80px',
                gap: '10px',
                marginBottom: '15px',
                opacity,
              }}
            >
              <span
                style={{ color: tool.color, fontSize: '24px', fontWeight: 'bold' }}
              >
                {tool.name}
              </span>
              {tool.scores.map((score, i) => (
                <span
                  key={i}
                  style={{
                    color: score >= 4 ? '#4ade80' : score >= 3.5 ? '#fbbf24' : '#f87171',
                    fontSize: '22px',
                    textAlign: 'center',
                    fontWeight: 'bold',
                  }}
                >
                  {score}
                </span>
              ))}
              <span
                style={{
                  color: '#fff',
                  fontSize: '26px',
                  textAlign: 'center',
                  fontWeight: 'bold',
                  background: `${tool.color}30`,
                  borderRadius: '8px',
                }}
              >
                {totalScores[index]}
              </span>
            </div>
          );
        })}
      </div>

      {/* 结论 */}
      <div
        style={{
          marginTop: '40px',
          padding: '20px 40px',
          background: 'linear-gradient(90deg, #00BFFF20, #4ECDC420)',
          borderRadius: '15px',
          opacity: interpolate(frame, [100, 120], [0, 1]),
        }}
      >
        <p style={{ fontSize: '28px', color: '#fff', margin: 0 }}>
          🏆 <span style={{ color: '#00BFFF' }}>Kimi</span> 综合体验最佳 ·
          <span style={{ color: '#FF6B6B' }}>秘塔</span> 学术最强 ·
          <span style={{ color: '#4ECDC4' }}>360AI</span> 生活场景出色
        </p>
      </div>
    </div>
  );
};
