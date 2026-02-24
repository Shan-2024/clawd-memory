import { useCurrentFrame, useVideoConfig, spring, interpolate, Easing } from 'remotion';
import React from 'react';

// 视频配置
const VIDEO_DURATION = 5400; // 3分钟 = 180秒 = 5400帧 @30fps
const FPS = 30;

// 苹果风格配色 - 极简黑白灰
const COLORS = {
  bg: '#FFFFFF',
  text: '#1D1D1F',
  textSecondary: '#86868B',
  accent: '#0071E3', // 苹果蓝
  divider: '#D2D2D7',
};

// 字体 - 苹方风格（系统非衬线字体）
const FONT_FAMILY = '"PingFang SC", "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';

// AI 工具数据 - 基于搜索结果
const AI_TOOLS = [
  {
    category: '对话与写作',
    tools: [
      { name: 'ChatGPT', desc: '全能型 AI 助手', company: 'OpenAI' },
      { name: 'Claude', desc: '深度推理与代码', company: 'Anthropic' },
      { name: 'Gemini', desc: '多模态智能', company: 'Google' },
    ]
  },
  {
    category: '视频生成',
    tools: [
      { name: 'Veo', desc: '高质量视频生成', company: 'Google' },
      { name: 'Sora', desc: 'OpenAI 视频模型', company: 'OpenAI' },
      { name: 'HeyGen', desc: '数字人视频', company: 'HeyGen' },
    ]
  },
  {
    category: '图像与设计',
    tools: [
      { name: 'Midjourney', desc: '艺术创作', company: 'Midjourney' },
      { name: 'DALL-E 3', desc: '图像生成', company: 'OpenAI' },
      { name: 'Gemini Imagen', desc: 'Google 图像模型', company: 'Google' },
    ]
  },
  {
    category: '效率与自动化',
    tools: [
      { name: 'Cursor', desc: 'AI 代码编辑器', company: 'Cursor' },
      { name: 'Notion AI', desc: '智能笔记', company: 'Notion' },
      { name: 'Zapier AI', desc: '工作流自动化', company: 'Zapier' },
    ]
  },
];

// 主视频组件
export const AIToolsShowcase: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        backgroundColor: COLORS.bg,
        fontFamily: FONT_FAMILY,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden',
      }}
    >
      {/* 开场 0-5s (0-150帧) */}
      {frame < 150 && <IntroScene frame={frame} />}
      
      {/* 四个类别展示，每个20秒 */}
      {frame >= 150 && frame < 750 && <CategoryScene frame={frame} categoryIndex={0} />} // 5-25s
      {frame >= 750 && frame < 1350 && <CategoryScene frame={frame} categoryIndex={1} />} // 25-45s
      {frame >= 1350 && frame < 1950 && <CategoryScene frame={frame} categoryIndex={2} />} // 45-65s
      {frame >= 1950 && frame < 2550 && <CategoryScene frame={frame} categoryIndex={3} />} // 65-85s
      
      {/* 数据洞察 85-100s */}
      {frame >= 2550 && frame < 3000 && <InsightsScene frame={frame} />}
      
      {/* 结尾 100-120s */}
      {frame >= 3000 && frame < 3600 && <OutroScene frame={frame} />}
      
      {/* 如果超过2分钟，循环展示更多内容 */}
      {frame >= 3600 && frame < 5400 && <ExtendedContent frame={frame} />}
    </div>
  );
};

// 开场场景
const IntroScene: React.FC<{ frame: number }> = ({ frame }) => {
  const opacity = interpolate(frame, [0, 60], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  
  const scale = interpolate(frame, [0, 60], [0.9, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const subtitleOpacity = interpolate(frame, [60, 120], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        opacity,
        transform: `scale(${scale})`,
      }}
    >
      <h1
        style={{
          fontSize: 72,
          fontWeight: 600,
          color: COLORS.text,
          letterSpacing: '-0.02em',
          margin: 0,
          marginBottom: 24,
        }}
      >
        AI 工具全景
      </h1>
      <p
        style={{
          fontSize: 28,
          fontWeight: 400,
          color: COLORS.textSecondary,
          letterSpacing: '0.02em',
          opacity: subtitleOpacity,
          margin: 0,
        }}
      >
        2026 年度精选
      </p>
    </div>
  );
};

// 类别展示场景
const CategoryScene: React.FC<{ frame: number; categoryIndex: number }> = ({ frame, categoryIndex }) => {
  const category = AI_TOOLS[categoryIndex];
  const sectionStartFrame = 150 + categoryIndex * 600;
  const relativeFrame = frame - sectionStartFrame;
  
  // 标题进场动画
  const titleY = interpolate(relativeFrame, [0, 40], [40, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const titleOpacity = interpolate(relativeFrame, [0, 40], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        width: '100%',
        height: '100%',
      }}
    >
      {/* 类别标题 */}
      <div
        style={{
          transform: `translateY(${titleY}px)`,
          opacity: titleOpacity,
          marginBottom: 80,
        }}
      >
        <p
          style={{
            fontSize: 18,
            fontWeight: 500,
            color: COLORS.textSecondary,
            letterSpacing: '0.1em',
            textTransform: 'uppercase',
            margin: 0,
            marginBottom: 16,
          }}
        >
          类别 {categoryIndex + 1} / {AI_TOOLS.length}
        </p>
        <h2
          style={{
            fontSize: 56,
            fontWeight: 600,
            color: COLORS.text,
            letterSpacing: '-0.02em',
            margin: 0,
          }}
        >
          {category.category}
        </h2>
      </div>

      {/* 工具卡片 */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 32,
        }}
      >
        {category.tools.map((tool, index) => {
          const toolDelay = 60 + index * 40;
          const toolOpacity = interpolate(relativeFrame, [toolDelay, toolDelay + 40], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          const toolX = interpolate(relativeFrame, [toolDelay, toolDelay + 40], [30, 0], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

          return (
            <div
              key={tool.name}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 24,
                opacity: toolOpacity,
                transform: `translateX(${toolX}px)`,
                padding: '24px 48px',
                borderRadius: 16,
                backgroundColor: '#F5F5F7',
                minWidth: 480,
              }}
            >
              <div>
                <p
                  style={{
                    fontSize: 14,
                    fontWeight: 500,
                    color: COLORS.textSecondary,
                    margin: 0,
                    marginBottom: 4,
                  }}
                >
                  {tool.company}
                </p>
                <h3
                  style={{
                    fontSize: 32,
                    fontWeight: 600,
                    color: COLORS.text,
                    margin: 0,
                    letterSpacing: '-0.01em',
                  }}
                >
                  {tool.name}
                </h3>
              </div>
              <div
                style={{
                  width: 1,
                  height: 40,
                  backgroundColor: COLORS.divider,
                  margin: '0 16px',
                }}
              />
              <p
                style={{
                  fontSize: 18,
                  fontWeight: 400,
                  color: COLORS.textSecondary,
                  margin: 0,
                  flex: 1,
                }}
              >
                {tool.desc}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// 数据洞察场景
const InsightsScene: React.FC<{ frame: number }> = ({ frame }) => {
  const relativeFrame = frame - 2550;
  
  const opacity = interpolate(relativeFrame, [0, 40], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const stats = [
    { label: '对话 AI', value: '3', unit: '款' },
    { label: '视频生成', value: '3', unit: '款' },
    { label: '图像设计', value: '3', unit: '款' },
    { label: '效率工具', value: '3', unit: '款' },
  ];

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        opacity,
      }}
    >
      <h2
        style={{
          fontSize: 48,
          fontWeight: 600,
          color: COLORS.text,
          margin: 0,
          marginBottom: 80,
          letterSpacing: '-0.02em',
        }}
      >
        全景概览
      </h2>

      <div
        style={{
          display: 'flex',
          gap: 60,
        }}
      >
        {stats.map((stat, index) => {
          const statDelay = 40 + index * 30;
          const statOpacity = interpolate(relativeFrame, [statDelay, statDelay + 30], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          const statY = interpolate(relativeFrame, [statDelay, statDelay + 30], [20, 0], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

          return (
            <div
              key={stat.label}
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                opacity: statOpacity,
                transform: `translateY(${statY}px)`,
              }}
            >
              <span
                style={{
                  fontSize: 64,
                  fontWeight: 300,
                  color: COLORS.text,
                  letterSpacing: '-0.03em',
                }}
              >
                {stat.value}
                <span style={{ fontSize: 24, fontWeight: 400, color: COLORS.textSecondary }}>
                  {stat.unit}
                </span>
              </span>
              <span
                style={{
                  fontSize: 16,
                  fontWeight: 500,
                  color: COLORS.textSecondary,
                  marginTop: 8,
                  letterSpacing: '0.05em',
                }}
              >
                {stat.label}
              </span>
            </div>
          );
        })}
      </div>

      <div
        style={{
          marginTop: 80,
          padding: '32px 64px',
          borderTop: `1px solid ${COLORS.divider}`,
          opacity: interpolate(relativeFrame, [200, 240], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        <p
          style={{
            fontSize: 20,
            fontWeight: 400,
            color: COLORS.textSecondary,
            textAlign: 'center',
            margin: 0,
            lineHeight: 1.6,
          }}
        >
          工具选择应基于具体场景，<br />
          而非盲目追求最新技术
        </p>
      </div>
    </div>
  );
};

// 结尾场景
const OutroScene: React.FC<{ frame: number }> = ({ frame }) => {
  const relativeFrame = frame - 3000;
  
  const opacity = interpolate(relativeFrame, [0, 60], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  
  const scale = interpolate(relativeFrame, [0, 60], [0.95, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        opacity,
        transform: `scale(${scale})`,
      }}
    >
      <p
        style={{
          fontSize: 24,
          fontWeight: 500,
          color: COLORS.textSecondary,
          letterSpacing: '0.1em',
          margin: 0,
          marginBottom: 32,
        }}
      >
        感谢观看
      </p>
      <h2
        style={{
          fontSize: 64,
          fontWeight: 600,
          color: COLORS.text,
          letterSpacing: '-0.02em',
          margin: 0,
          marginBottom: 48,
        }}
      >
        持续探索，明智选择
      </h2>
      <div
        style={{
          width: 60,
          height: 4,
          backgroundColor: COLORS.accent,
          borderRadius: 2,
        }}
      />
    </div>
  );
};

// 扩展内容（如果视频超过2分钟）
const ExtendedContent: React.FC<{ frame: number }> = ({ frame }) => {
  const relativeFrame = frame - 3600;
  const cycle = Math.floor(relativeFrame / 600) % 3; // 每20秒循环一次
  
  // 循环展示不同的内容页面
  if (cycle === 0) {
    return <TrendsScene frame={relativeFrame % 600} />;
  } else if (cycle === 1) {
    return <ComparisonScene frame={relativeFrame % 600} />;
  } else {
    return <TipsScene frame={relativeFrame % 600} />;
  }
};

// 趋势场景
const TrendsScene: React.FC<{ frame: number }> = ({ frame }) => {
  const opacity = interpolate(frame, [0, 40], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const trends = [
    '多模态融合成为标配',
    '推理能力持续增强',
    '个性化程度不断提升',
    '本地化部署需求增长',
  ];

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        opacity,
      }}
    >
      <h2
        style={{
          fontSize: 48,
          fontWeight: 600,
          color: COLORS.text,
          margin: 0,
          marginBottom: 64,
          letterSpacing: '-0.02em',
        }}
      >
        2026 趋势观察
      </h2>

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: 24,
        }}
      >
        {trends.map((trend, index) => {
          const trendDelay = 40 + index * 30;
          const trendOpacity = interpolate(frame, [trendDelay, trendDelay + 30], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

          return (
            <div
              key={trend}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 20,
                opacity: trendOpacity,
              }}
            >
              <div
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: '50%',
                  backgroundColor: COLORS.accent,
                }}
              />
              <p
                style={{
                  fontSize: 24,
                  fontWeight: 400,
                  color: COLORS.text,
                  margin: 0,
                }}
              >
                {trend}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// 对比场景
const ComparisonScene: React.FC<{ frame: number }> = ({ frame }) => {
  const opacity = interpolate(frame, [0, 40], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        opacity,
      }}
    >
      <h2
        style={{
          fontSize: 48,
          fontWeight: 600,
          color: COLORS.text,
          margin: 0,
          marginBottom: 64,
          letterSpacing: '-0.02em',
        }}
      >
        选型建议
      </h2>

      <div
        style={{
          display: 'flex',
          gap: 48,
        }}
      >
        {[
          { type: '入门用户', tool: 'ChatGPT', reason: '生态完善，易于上手' },
          { type: '专业开发', tool: 'Claude', reason: '代码能力强，推理深入' },
          { type: '创意工作', tool: 'Midjourney', reason: '图像质量行业领先' },
        ].map((item, index) => {
          const itemDelay = 40 + index * 40;
          const itemOpacity = interpolate(frame, [itemDelay, itemDelay + 40], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

          return (
            <div
              key={item.type}
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                padding: '40px 48px',
                backgroundColor: '#F5F5F7',
                borderRadius: 20,
                opacity: itemOpacity,
                minWidth: 200,
              }}
            >
              <p
                style={{
                  fontSize: 14,
                  fontWeight: 500,
                  color: COLORS.textSecondary,
                  margin: 0,
                  marginBottom: 12,
                  letterSpacing: '0.05em',
                }}
              >
                {item.type}
              </p>
              <h3
                style={{
                  fontSize: 28,
                  fontWeight: 600,
                  color: COLORS.text,
                  margin: 0,
                  marginBottom: 8,
                }}
              >
                {item.tool}
              </h3>
              <p
                style={{
                  fontSize: 14,
                  fontWeight: 400,
                  color: COLORS.textSecondary,
                  margin: 0,
                  textAlign: 'center',
                }}
              >
                {item.reason}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// 提示场景
const TipsScene: React.FC<{ frame: number }> = ({ frame }) => {
  const opacity = interpolate(frame, [0, 40], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const tips = [
    '定期评估工具适用性',
    '关注隐私与数据安全',
    '培养批判性思维能力',
    '保持学习与更新',
  ];

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        opacity,
      }}
    >
      <h2
        style={{
          fontSize: 48,
          fontWeight: 600,
          color: COLORS.text,
          margin: 0,
          marginBottom: 64,
          letterSpacing: '-0.02em',
        }}
      >
        使用建议
      </h2>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '32px 64px',
        }}
      >
        {tips.map((tip, index) => {
          const tipDelay = 40 + index * 25;
          const tipOpacity = interpolate(frame, [tipDelay, tipDelay + 25], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

          return (
            <div
              key={tip}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 16,
                opacity: tipOpacity,
              }}
            >
              <span
                style={{
                  fontSize: 20,
                  fontWeight: 600,
                  color: COLORS.accent,
                }}
              >
                0{index + 1}
              </span>
              <p
                style={{
                  fontSize: 22,
                  fontWeight: 400,
                  color: COLORS.text,
                  margin: 0,
                }}
              >
                {tip}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};