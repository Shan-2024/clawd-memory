import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

export const IntroScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 标题动画
  const titleOpacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const subtitleOpacity = interpolate(frame, [30, 60], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const scale = interpolate(frame, [0, 60], [0.8, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
      }}
    >
      {/* 发光效果 */}
      <div
        style={{
          position: 'absolute',
          width: '400px',
          height: '400px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(0,191,255,0.3) 0%, transparent 70%)',
          transform: `scale(${scale})`,
        }}
      />

      {/* 主标题 */}
      <h1
        style={{
          fontSize: '72px',
          fontWeight: 'bold',
          color: '#ffffff',
          textAlign: 'center',
          opacity: titleOpacity,
          transform: `scale(${scale})`,
          textShadow: '0 0 40px rgba(0,191,255,0.5)',
          marginBottom: '20px',
        }}
      >
        AI搜索工具横评
      </h1>

      {/* 副标题 */}
      <p
        style={{
          fontSize: '36px',
          color: '#00BFFF',
          opacity: subtitleOpacity,
          fontWeight: '500',
        }}
      >
        Kimi vs 秘塔 vs 360AI vs 天工
      </p>

      {/* 装饰线 */}
      <div
        style={{
          width: interpolate(frame, [45, 90], [0, 300], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
          height: '4px',
          background: 'linear-gradient(90deg, transparent, #00BFFF, transparent)',
          marginTop: '30px',
        }}
      />
    </div>
  );
};
