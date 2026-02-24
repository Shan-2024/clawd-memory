import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';

const TOOLS = [
  { name: 'Kimi', color: '#00BFFF' },
  { name: '秘塔', color: '#FF6B6B' },
  { name: '360AI', color: '#4ECDC4' },
  { name: '天工', color: '#FFE66D' },
];

interface Dimension {
  key: string;
  name: string;
  icon: string;
  description: string;
}

interface DimensionSceneProps {
  dimension: Dimension;
  scores: number[];
}

export const DimensionScene = ({ dimension, scores }: DimensionSceneProps) => {
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
        background: '#0a0a0a',
        padding: '40px',
      }}
    >
      {/* 维度标题 */}
      <div
        style={{
          textAlign: 'center',
          marginBottom: '60px',
          opacity: interpolate(frame, [0, 20], [0, 1]),
        }}
      >
        <div
          style={{
            fontSize: '80px',
            marginBottom: '20px',
          }}
        >
          {dimension.icon}
        </div>
        <h2
          style={{
            fontSize: '56px',
            color: '#ffffff',
            margin: '0 0 15px 0',
          }}
        >
          {dimension.name}
        </h2>
        <p
          style={{
            fontSize: '28px',
            color: '#888',
            margin: 0,
          }}
        >
          {dimension.description}
        </p>
      </div>

      {/* 评分条 */}
      <div
        style={{
          width: '100%',
          maxWidth: '800px',
          display: 'flex',
          flexDirection: 'column',
          gap: '25px',
        }}
      >
        {TOOLS.map((tool, index) => {
          const delay = 30 + index * 15;
          const opacity = interpolate(frame, [delay, delay + 20], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          const barWidth = interpolate(
            frame,
            [delay + 10, delay + 40],
            [0, (scores[index] / 5) * 100],
            {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            }
          );

          return (
            <div
              key={tool.name}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '20px',
                opacity,
              }}
            >
              <span
                style={{
                  fontSize: '28px',
                  color: tool.color,
                  width: '100px',
                  fontWeight: 'bold',
                }}
              >
                {tool.name}
              </span>
              <div
                style={{
                  flex: 1,
                  height: '40px',
                  background: '#222',
                  borderRadius: '20px',
                  overflow: 'hidden',
                }}
              >
                <div
                  style={{
                    width: `${barWidth}%`,
                    height: '100%',
                    background: `linear-gradient(90deg, ${tool.color}, ${tool.color}80)`,
                    borderRadius: '20px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'flex-end',
                    paddingRight: '15px',
                    transition: 'width 0.3s ease',
                  }}
                >
                  {barWidth > 15 && (
                    <span
                      style={{
                        fontSize: '22px',
                        fontWeight: 'bold',
                        color: '#000',
                      }}
                    >
                      {scores[index]}
                    </span>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
