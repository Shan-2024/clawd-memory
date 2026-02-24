import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

const TOOLS = [
  { name: 'Kimi', color: '#00BFFF', description: '月之暗面出品' },
  { name: '秘塔', color: '#FF6B6B', description: '学术搜索专家' },
  { name: '360AI', color: '#4ECDC4', description: '安全大厂出品' },
  { name: '天工', color: '#FFE66D', description: '昆仑万维打造' },
];

export const ToolIntroScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

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
          marginBottom: '60px',
          opacity: interpolate(frame, [0, 20], [0, 1]),
        }}
      >
        参赛选手
      </h2>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '30px',
          width: '100%',
          maxWidth: '900px',
        }}
      >
        {TOOLS.map((tool, index) => {
          const delay = index * 15;
          const opacity = interpolate(frame, [delay, delay + 20], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          const translateY = interpolate(frame, [delay, delay + 20], [50, 0], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

          return (
            <div
              key={tool.name}
              style={{
                background: `linear-gradient(135deg, ${tool.color}20, ${tool.color}05)`,
                border: `2px solid ${tool.color}`,
                borderRadius: '20px',
                padding: '30px',
                opacity,
                transform: `translateY(${translateY}px)`,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
              }}
            >
              <div
                style={{
                  width: '80px',
                  height: '80px',
                  borderRadius: '50%',
                  background: tool.color,
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  fontSize: '32px',
                  fontWeight: 'bold',
                  color: '#000',
                  marginBottom: '15px',
                }}
              >
                {tool.name[0]}
              </div>
              <h3 style={{ fontSize: '36px', color: '#fff', margin: '0 0 10px 0' }}>
                {tool.name}
              </h3>
              <p style={{ fontSize: '24px', color: '#aaa', margin: 0 }}>
                {tool.description}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
