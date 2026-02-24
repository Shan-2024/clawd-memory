import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';

export const OutroScene = () => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        background: 'linear-gradient(135deg, #0f3460 0%, #16213e 50%, #1a1a2e 100%)',
      }}
    >
      <h2
        style={{
          fontSize: '56px',
          color: '#ffffff',
          marginBottom: '30px',
          opacity: interpolate(frame, [0, 20], [0, 1]),
          transform: `translateY(${interpolate(frame, [0, 20], [30, 0])}px)`,
        }}
      >
        总结
      </h2>

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '20px',
          alignItems: 'center',
          opacity: interpolate(frame, [20, 40], [0, 1]),
        }}
      >
        <p
          style={{
            fontSize: '32px',
            color: '#fff',
            background: '#00BFFF20',
            padding: '15px 30px',
            borderRadius: '12px',
            border: '2px solid #00BFFF',
          }}
        >
          🔍 日常搜索 → Kimi
        </p>
        <p
          style={{
            fontSize: '32px',
            color: '#fff',
            background: '#FF6B6B20',
            padding: '15px 30px',
            borderRadius: '12px',
            border: '2px solid #FF6B6B',
          }}
        >
          📚 学术研究 → 秘塔
        </p>
        <p
          style={{
            fontSize: '32px',
            color: '#fff',
            background: '#4ECDC420',
            padding: '15px 30px',
            borderRadius: '12px',
            border: '2px solid #4ECDC4',
          }}
        >
          🛍️ 生活消费 → 360AI
        </p>
      </div>

      <p
        style={{
          marginTop: '60px',
          fontSize: '28px',
          color: '#888',
          opacity: interpolate(frame, [50, 70], [0, 1]),
        }}
      >
        👆 点赞关注，获取更多AI工具测评
      </p>
    </div>
  );
};
