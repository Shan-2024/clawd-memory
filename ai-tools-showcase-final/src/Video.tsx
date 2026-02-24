import { useCurrentFrame, useVideoConfig, spring, interpolate, Easing, Sequence, AbsoluteFill, staticFile } from 'remotion';
import React from 'react';

// 加载本地字体
const fontStyle = `
  @font-face {
    font-family: 'Noto Sans SC';
    src: url('${staticFile('fonts/NotoSansSC-Regular.ttf')}') format('opentype');
    font-weight: 400;
    font-display: swap;
  }
`;

const THEME = {
  colors: { 
    background: '#FFFFFF', 
    primary: '#1D1D1F', 
    secondary: '#86868B', 
    accent: '#0071E3', 
    surface: '#F5F5F7',
    muted: '#E8E8ED'
  },
  fonts: { family: '"Noto Sans SC", sans-serif' },
};

// 动画工具
const useSpringFade = (delay = 0) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({ frame: frame - delay, fps, config: { damping: 25, stiffness: 100 } });
  return { opacity: progress, transform: `translateY(${(1 - progress) * 40}px)` };
};

const useFade = (delay = 0, duration = 25) => {
  const frame = useCurrentFrame();
  return interpolate(frame - delay, [0, duration], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
};

// 工具数据 - 带颜色配置
const TOOLS = [
  { name: 'ChatGPT', company: 'OpenAI', desc: '全能型 AI 助手', features: ['自然对话', '代码生成', '创意写作'], color: '#10A37F', bgGradient: 'linear-gradient(135deg, #10A37F20, #10A37F08)' },
  { name: 'Claude', company: 'Anthropic', desc: '深度推理专家', features: ['超长上下文', '逻辑分析', '安全可靠'], color: '#D97757', bgGradient: 'linear-gradient(135deg, #D9775720, #D9775708)' },
  { name: 'Gemini', company: 'Google', desc: '多模态智能平台', features: ['原生多模态', '实时搜索', '深度集成'], color: '#4285F4', bgGradient: 'linear-gradient(135deg, #4285F420, #4285F408)' },
  { name: 'Sora', company: 'OpenAI', desc: '革命性视频生成', features: ['文本生视频', '物理模拟', '电影级画质'], color: '#000000', bgGradient: 'linear-gradient(135deg, #00000015, #00000005)' },
  { name: 'Midjourney', company: 'Midjourney', desc: '艺术创作先锋', features: ['精美图像', '风格多样', '社区活跃'], color: '#1F2937', bgGradient: 'linear-gradient(135deg, #1F293720, #1F293708)' },
  { name: 'Cursor', company: 'Cursor', desc: 'AI 原生代码编辑器', features: ['智能补全', '代码重构', '自然语言编程'], color: '#6366F1', bgGradient: 'linear-gradient(135deg, #6366F120, #6366F108)' },
];

// 场景1: 开场
const SceneIntro: React.FC = () => {
  const titleAnim = useSpringFade(0);
  const subtitleAnim = useSpringFade(20);
  const lineAnim = useFade(40, 30);
  
  return (
    <AbsoluteFill style={{ background: THEME.colors.background, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: THEME.fonts.family }}>
      <div style={{ ...titleAnim, textAlign: 'center' }}>
        <h1 style={{ fontSize: 96, fontWeight: 700, color: THEME.colors.primary, margin: 0, letterSpacing: '-0.02em' }}>AI 工具全景 2026</h1>
      </div>
      <div style={{ ...subtitleAnim, textAlign: 'center', marginTop: 32 }}>
        <p style={{ fontSize: 32, color: THEME.colors.secondary, margin: 0 }}>六大精选工具 · 深度解析</p>
      </div>
      <div style={{ 
        width: 80, height: 4, background: THEME.colors.accent, borderRadius: 2, marginTop: 48,
        opacity: lineAnim, transform: `scaleX(${lineAnim})`, transformOrigin: 'center'
      }} />
    </AbsoluteFill>
  );
};

// 场景2-7: 详细工具展示 - 改进设计
const SceneToolDetail: React.FC<{ tool: typeof TOOLS[0]; index: number }> = ({ tool, index }) => {
  const frame = useCurrentFrame();
  const delay = index * 3;
  
  const bgOpacity = interpolate(frame - delay, [0, 30], [0, 1], { extrapolateLeft: 'clamp' });
  const contentY = interpolate(frame - delay - 10, [0, 25], [30, 0], { extrapolateLeft: 'clamp' });
  const contentOpacity = interpolate(frame - delay - 10, [0, 25], [0, 1], { extrapolateLeft: 'clamp' });
  
  return (
    <AbsoluteFill style={{ background: THEME.colors.background, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: THEME.fonts.family, padding: 80 }}>
      {/* 顶部公司名 */}
      <div style={{ textAlign: 'center', marginBottom: 40 }}>
        <span style={{ 
          fontSize: 18, color: THEME.colors.secondary, letterSpacing: '0.2em',
          opacity: interpolate(frame - delay, [0, 20], [0, 1], { extrapolateLeft: 'clamp' })
        }}>{tool.company}</span>
      </div>
      
      {/* 主内容区 */}
      <div style={{ 
        background: tool.bgGradient,
        borderRadius: 24,
        padding: '60px 100px',
        textAlign: 'center',
        minWidth: 700,
        opacity: bgOpacity
      }}>
        {/* 工具名 */}
        <h2 style={{ 
          fontSize: 80, fontWeight: 700, color: tool.color, margin: '0 0 16px 0',
          opacity: contentOpacity, transform: `translateY(${contentY}px)`
        }}>{tool.name}</h2>
        
        {/* 描述 */}
        <p style={{ 
          fontSize: 28, color: THEME.colors.secondary, margin: '0 0 40px 0',
          opacity: interpolate(frame - delay - 20, [0, 20], [0, 1], { extrapolateLeft: 'clamp' })
        }}>{tool.desc}</p>
        
        {/* 特性标签 */}
        <div style={{ display: 'flex', justifyContent: 'center', gap: 16 }}>
          {tool.features.map((feature, i) => (
            <span key={feature} style={{ 
              padding: '12px 24px', background: 'rgba(255,255,255,0.8)', borderRadius: 8,
              fontSize: 18, color: THEME.colors.primary, fontWeight: 500,
              opacity: interpolate(frame - delay - 30 - i * 8, [0, 15], [0, 1], { extrapolateLeft: 'clamp' }),
              transform: `translateY(${interpolate(frame - delay - 30 - i * 8, [0, 15], [10, 0], { extrapolateLeft: 'clamp' })}px)`
            }}>{feature}</span>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景8: 快速对比
const SceneComparison: React.FC = () => {
  const frame = useCurrentFrame();
  const titleAnim = useSpringFade(0);
  
  return (
    <AbsoluteFill style={{ background: THEME.colors.background, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: THEME.fonts.family, padding: 60 }}>
      <div style={{ ...titleAnim, marginBottom: 60 }}>
        <h2 style={{ fontSize: 56, fontWeight: 700, color: THEME.colors.primary, margin: 0 }}>快速对比</h2>
      </div>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 24, maxWidth: 1400 }}>
        {TOOLS.slice(0, 3).map((tool, i) => (
          <div key={tool.name} style={{
            background: THEME.colors.surface,
            borderRadius: 16,
            padding: 32,
            textAlign: 'center',
            opacity: interpolate(frame - 20 - i * 15, [0, 20], [0, 1], { extrapolateLeft: 'clamp' }),
            transform: `translateY(${interpolate(frame - 20 - i * 15, [0, 20], [20, 0], { extrapolateLeft: 'clamp' })}px)`
          }}>
            <div style={{ fontSize: 14, color: THEME.colors.secondary, marginBottom: 8 }}>{tool.company}</div>
            <div style={{ fontSize: 32, fontWeight: 700, color: tool.color, marginBottom: 12 }}>{tool.name}</div>
            <div style={{ fontSize: 16, color: THEME.colors.secondary }}>{tool.desc}</div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// 场景9: 选型建议
const SceneRecommendations: React.FC = () => {
  const frame = useCurrentFrame();
  const titleAnim = useSpringFade(0);
  
  const recs = [
    { title: '日常对话', tool: 'ChatGPT', reason: '综合能力最强' },
    { title: '深度研究', tool: 'Claude', reason: '长文本处理优秀' },
    { title: '创意工作', tool: 'Midjourney', reason: '图像质量顶尖' },
    { title: '编程开发', tool: 'Cursor', reason: '代码理解精准' },
  ];
  
  return (
    <AbsoluteFill style={{ background: THEME.colors.background, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: THEME.fonts.family }}>
      <div style={{ ...titleAnim, marginBottom: 60 }}>
        <h2 style={{ fontSize: 56, fontWeight: 700, color: THEME.colors.primary, margin: 0 }}>选型建议</h2>
      </div>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32, maxWidth: 1000 }}>
        {recs.map((rec, i) => {
          const tool = TOOLS.find(t => t.name === rec.tool);
          return (
            <div key={rec.title} style={{
              display: 'flex', alignItems: 'center', gap: 20,
              padding: 28, background: THEME.colors.surface, borderRadius: 12,
              opacity: interpolate(frame - 20 - i * 12, [0, 20], [0, 1], { extrapolateLeft: 'clamp' })
            }}>
              <div style={{
                width: 50, height: 50, borderRadius: 12,
                background: tool?.color || THEME.colors.accent,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                color: '#fff', fontSize: 20, fontWeight: 700
              }}>{rec.tool[0]}</div>
              <div>
                <div style={{ fontSize: 14, color: THEME.colors.secondary, marginBottom: 4 }}>{rec.title}</div>
                <div style={{ fontSize: 22, fontWeight: 600, color: THEME.colors.primary }}>{rec.tool}</div>
                <div style={{ fontSize: 14, color: THEME.colors.secondary, marginTop: 4 }}>{rec.reason}</div>
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// 场景10: 2026趋势
const SceneTrends: React.FC = () => {
  const frame = useCurrentFrame();
  const titleAnim = useSpringFade(0);
  
  const trends = [
    { title: '多模态融合', desc: '文本、图像、视频、音频统一处理', icon: '🔄' },
    { title: '端侧 AI', desc: '本地运行，保护隐私，降低延迟', icon: '📱' },
    { title: 'Agent 自主', desc: '从回答问题到自主完成任务', icon: '🤖' },
    { title: '垂直深化', desc: '医疗、法律、教育等专业领域', icon: '🎯' },
  ];
  
  return (
    <AbsoluteFill style={{ background: THEME.colors.background, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: THEME.fonts.family }}>
      <div style={{ ...titleAnim, marginBottom: 60 }}>
        <h2 style={{ fontSize: 56, fontWeight: 700, color: THEME.colors.primary, margin: 0 }}>2026 AI 趋势</h2>
      </div>
      
      <div style={{ display: 'flex', gap: 24 }}>
        {trends.map((trend, i) => (
          <div key={trend.title} style={{
            width: 220, padding: 32,
            background: THEME.colors.surface, borderRadius: 16,
            textAlign: 'center',
            opacity: interpolate(frame - 20 - i * 15, [0, 20], [0, 1], { extrapolateLeft: 'clamp' }),
            transform: `scale(${interpolate(frame - 20 - i * 15, [0, 20], [0.9, 1], { extrapolateLeft: 'clamp' })})`
          }}>
            <div style={{ fontSize: 40, marginBottom: 16 }}>{trend.icon}</div>
            <div style={{ fontSize: 20, fontWeight: 600, color: THEME.colors.primary, marginBottom: 8 }}>{trend.title}</div>
            <div style={{ fontSize: 14, color: THEME.colors.secondary, lineHeight: 1.5 }}>{trend.desc}</div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// 场景11: 结尾
const SceneOutro: React.FC = () => {
  const titleAnim = useSpringFade(0);
  const subtitleAnim = useSpringFade(25);
  const lineAnim = useFade(50, 30);
  
  return (
    <AbsoluteFill style={{ background: THEME.colors.background, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: THEME.fonts.family }}>
      <div style={{ ...subtitleAnim, marginBottom: 16 }}>
        <p style={{ fontSize: 28, color: THEME.colors.secondary, margin: 0 }}>感谢观看</p>
      </div>
      <div style={{ ...titleAnim, textAlign: 'center' }}>
        <h2 style={{ fontSize: 72, fontWeight: 700, color: THEME.colors.primary, margin: 0 }}>持续探索 · 明智选择</h2>
      </div>
      <div style={{ 
        width: 80, height: 4, background: THEME.colors.accent, borderRadius: 2, marginTop: 48,
        opacity: lineAnim, transform: `scaleX(${lineAnim})`, transformOrigin: 'center'
      }} />
    </AbsoluteFill>
  );
};

// 主组件
export const AIToolsShowcaseFinal: React.FC = () => {
  return (
    <>
      <style>{fontStyle}</style>
      <AbsoluteFill style={{ background: THEME.colors.background }}>
        <Sequence from={0} durationInFrames={90}><SceneIntro /></Sequence>
        {TOOLS.map((tool, i) => (
          <Sequence key={tool.name} from={90 + i * 280} durationInFrames={280}>
            <SceneToolDetail tool={tool} index={i} />
          </Sequence>
        ))}
        <Sequence from={90 + TOOLS.length * 280} durationInFrames={200}><SceneComparison /></Sequence>
        <Sequence from={90 + TOOLS.length * 280 + 200} durationInFrames={220}><SceneRecommendations /></Sequence>
        <Sequence from={90 + TOOLS.length * 280 + 420} durationInFrames={220}><SceneTrends /></Sequence>
        <Sequence from={90 + TOOLS.length * 280 + 640} durationInFrames={150}><SceneOutro /></Sequence>
        <Sequence from={90 + TOOLS.length * 280 + 790} durationInFrames={110}><AbsoluteFill style={{ background: THEME.colors.background }} /></Sequence>
      </AbsoluteFill>
    </>
  );
};

export default AIToolsShowcaseFinal;