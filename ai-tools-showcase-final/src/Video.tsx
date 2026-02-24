import { useCurrentFrame, useVideoConfig, spring, interpolate, Easing, Sequence, AbsoluteFill } from 'remotion';
import React from 'react';

const THEME = {
  colors: { background: '#FFFFFF', primary: '#1D1D1F', secondary: '#86868B', accent: '#0071E3', surface: '#F5F5F7' },
  fonts: { family: '"PingFang SC", "Microsoft YaHei", sans-serif' },
};

// 动画工具
const useAnim = (delay = 0) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({ frame: frame - delay, fps, config: { damping: 20, stiffness: 100 } });
  return { opacity: progress, transform: `translateY(${(1 - progress) * 30}px)` };
};

const useFade = (delay = 0) => {
  const frame = useCurrentFrame();
  return interpolate(frame - delay, [0, 20], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
};

// 工具数据
const TOOLS = [
  { name: 'ChatGPT', company: 'OpenAI', desc: '全能型 AI 助手', tags: ['对话', '写作', '编程'], color: '#10A37F' },
  { name: 'Claude', company: 'Anthropic', desc: '深度推理与代码', tags: ['分析', '安全', '长文本'], color: '#D97757' },
  { name: 'Gemini', company: 'Google', desc: '多模态智能', tags: ['搜索', '图像', '视频'], color: '#4285F4' },
  { name: 'Sora', company: 'OpenAI', desc: '视频生成', tags: ['AI视频', '创意'], color: '#000000' },
  { name: 'Midjourney', company: 'Midjourney', desc: '艺术创作', tags: ['图像', '设计'], color: '#1F2937' },
  { name: 'Cursor', company: 'Cursor', desc: 'AI代码编辑器', tags: ['开发', '效率'], color: '#6366F1' },
];

// 场景1: 开场
const SceneIntro: React.FC = () => {
  const { opacity, transform } = useAnim(0);
  const subOpacity = useFade(30);
  return (
    <AbsoluteFill style={{ background: THEME.colors.background, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: THEME.fonts.family }}>
      <div style={{ opacity, transform, textAlign: 'center' }}>
        <h1 style={{ fontSize: 100, fontWeight: 700, color: THEME.colors.primary, margin: 0, letterSpacing: '-0.02em' }}>AI 工具全景 2026</h1>
        <p style={{ fontSize: 36, color: THEME.colors.secondary, marginTop: 24, opacity: subOpacity }}>12 款精选工具 · 4 大核心类别 · 深度测评</p>
      </div>
    </AbsoluteFill>
  );
};

// 场景2-7: 详细工具展示 (每款10秒)
const SceneToolDetail: React.FC<{ tool: typeof TOOLS[0]; index: number }> = ({ tool, index }) => {
  const frame = useCurrentFrame();
  const showDelay = index * 5;
  
  return (
    <AbsoluteFill style={{ background: THEME.colors.background, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: THEME.colors.fonts?.family || THEME.fonts.family, gap: 80 }}>
      {/* 左侧大图标 */}
      <div style={{ 
        width: 300, height: 300, borderRadius: 40, 
        background: tool.color, display: 'flex', alignItems: 'center', justifyContent: 'center',
        opacity: interpolate(frame - showDelay, [0, 20], [0, 1], { extrapolateLeft: 'clamp' }),
        transform: `scale(${interpolate(frame - showDelay, [0, 30], [0.8, 1], { extrapolateLeft: 'clamp' })})`
      }}>
        <span style={{ fontSize: 72, fontWeight: 700, color: '#FFF' }}>{tool.name[0]}</span>
      </div>
      
      {/* 右侧信息 */}
      <div style={{ maxWidth: 600 }}>
        <p style={{ fontSize: 20, color: THEME.colors.secondary, margin: 0, letterSpacing: '0.1em' }}>{tool.company}</p>
        <h2 style={{ 
          fontSize: 72, fontWeight: 700, color: THEME.colors.primary, margin: '8px 0', 
          opacity: interpolate(frame - showDelay - 10, [0, 20], [0, 1], { extrapolateLeft: 'clamp' })
        }}>{tool.name}</h2>
        <p style={{ 
          fontSize: 28, color: THEME.colors.secondary, margin: '16px 0',
          opacity: interpolate(frame - showDelay - 20, [0, 20], [0, 1], { extrapolateLeft: 'clamp' })
        }}>{tool.desc}</p>
        <div style={{ display: 'flex', gap: 12, marginTop: 24 }}>
          {tool.tags.map((tag, i) => (
            <span key={tag} style={{ 
              padding: '8px 16px', background: THEME.colors.surface, borderRadius: 20,
              fontSize: 16, color: THEME.colors.secondary,
              opacity: interpolate(frame - showDelay - 30 - i * 5, [0, 15], [0, 1], { extrapolateLeft: 'clamp' })
            }}>{tag}</span>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景8: 对比表格
const SceneComparison: React.FC = () => {
  const { opacity } = useAnim(0);
  const headers = ['工具', '公司', '核心优势', '适用场景'];
  const data = TOOLS.slice(0, 4).map(t => [t.name, t.company, t.desc, t.tags[0]]);
  
  return (
    <AbsoluteFill style={{ background: THEME.colors.background, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: THEME.fonts.family, padding: 60 }}>
      <h2 style={{ fontSize: 48, fontWeight: 700, color: THEME.colors.primary, marginBottom: 40 }}>工具对比一览</h2>
      <div style={{ opacity, width: '100%', maxWidth: 1400 }}>
        {/* 表头 */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 2fr 1fr', gap: 20, padding: '20px 0', borderBottom: '2px solid ' + THEME.colors.primary }}>
          {headers.map(h => <span key={h} style={{ fontSize: 20, fontWeight: 600, color: THEME.colors.primary }}>{h}</span>)}
        </div>
        {/* 数据行 */}
        {data.map((row, i) => (
          <div key={i} style={{ 
            display: 'grid', gridTemplateColumns: '1fr 1fr 2fr 1fr', gap: 20, 
            padding: '24px 0', borderBottom: '1px solid #E5E5E5',
            opacity: interpolate(useCurrentFrame() - i * 10, [0, 20], [0, 1], { extrapolateLeft: 'clamp' })
          }}>
            {row.map((cell, j) => <span key={j} style={{ fontSize: 18, color: j === 0 ? THEME.colors.primary : THEME.colors.secondary, fontWeight: j === 0 ? 600 : 400 }}>{cell}</span>)}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// 场景9: 使用建议
const SceneRecommendations: React.FC = () => {
  const frame = useCurrentFrame();
  const tips = [
    { icon: '🎯', title: '明确需求', desc: '先确定要解决什么问题' },
    { icon: '⚡', title: '快速尝试', desc: '利用免费额度多测试几款' },
    { icon: '🔒', title: '注意隐私', desc: '敏感数据选择本地化方案' },
    { icon: '📈', title: '持续学习', desc: 'AI 能力在快速进化' },
  ];
  
  return (
    <AbsoluteFill style={{ background: THEME.colors.background, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: THEME.fonts.family }}>
      <h2 style={{ fontSize: 56, fontWeight: 700, color: THEME.colors.primary, marginBottom: 60 }}>选型建议</h2>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 40 }}>
        {tips.map((tip, i) => (
          <div key={tip.title} style={{ 
            display: 'flex', alignItems: 'flex-start', gap: 20,
            padding: 32, background: THEME.colors.surface, borderRadius: 16,
            opacity: interpolate(frame - i * 15, [0, 25], [0, 1], { extrapolateLeft: 'clamp' }),
            transform: `translateY(${interpolate(frame - i * 15, [0, 25], [20, 0], { extrapolateLeft: 'clamp' })}px)`
          }}>
            <span style={{ fontSize: 40 }}>{tip.icon}</span>
            <div>
              <h3 style={{ fontSize: 24, fontWeight: 600, color: THEME.colors.primary, margin: 0 }}>{tip.title}</h3>
              <p style={{ fontSize: 18, color: THEME.colors.secondary, margin: '8px 0 0 0' }}>{tip.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// 场景10: 结尾
const SceneOutro: React.FC = () => {
  const { opacity, transform } = useAnim(0);
  return (
    <AbsoluteFill style={{ background: THEME.colors.background, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: THEME.fonts.family }}>
      <div style={{ opacity, transform, textAlign: 'center' }}>
        <p style={{ fontSize: 32, color: THEME.colors.secondary, marginBottom: 24 }}>感谢观看</p>
        <h2 style={{ fontSize: 80, fontWeight: 700, color: THEME.colors.primary, margin: 0 }}>持续探索 · 明智选择</h2>
        <div style={{ width: 80, height: 4, background: THEME.colors.accent, borderRadius: 2, margin: '40px auto 0' }} />
      </div>
    </AbsoluteFill>
  );
};

// 场景11: 趋势展望 (填充剩余时间)
const SceneTrends: React.FC = () => {
  const frame = useCurrentFrame();
  const trends = ['多模态融合加速', '端侧 AI 普及', 'Agent 自动化', '垂直领域深化'];
  
  return (
    <AbsoluteFill style={{ background: THEME.colors.background, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: THEME.fonts.family }}>
      <h2 style={{ fontSize: 56, fontWeight: 700, color: THEME.colors.primary, marginBottom: 60 }}>2026 AI 趋势</h2>
      <div style={{ display: 'flex', gap: 30 }}>
        {trends.map((trend, i) => (
          <div key={trend} style={{
            padding: '40px 30px', background: THEME.colors.surface, borderRadius: 20,
            textAlign: 'center', minWidth: 200,
            opacity: interpolate(frame - i * 20, [0, 25], [0, 1], { extrapolateLeft: 'clamp' }),
            transform: `scale(${interpolate(frame - i * 20, [0, 25], [0.9, 1], { extrapolateLeft: 'clamp' })})`
          }}>
            <div style={{ fontSize: 48, marginBottom: 16 }}>{['🔄', '📱', '🤖', '🎯'][i]}</div>
            <p style={{ fontSize: 20, fontWeight: 600, color: THEME.colors.primary, margin: 0 }}>{trend}</p>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// 主组件
export const AIToolsShowcaseFinal: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: THEME.colors.background }}>
      <Sequence from={0} durationInFrames={90}><SceneIntro /></Sequence>
      {TOOLS.map((tool, i) => (
        <Sequence key={tool.name} from={90 + i * 300} durationInFrames={300}>
          <SceneToolDetail tool={tool} index={i} />
        </Sequence>
      ))}
      <Sequence from={90 + TOOLS.length * 300} durationInFrames={240}><SceneComparison /></Sequence>
      <Sequence from={90 + TOOLS.length * 300 + 240} durationInFrames={240}><SceneRecommendations /></Sequence>
      <Sequence from={90 + TOOLS.length * 300 + 480} durationInFrames={240}><SceneTrends /></Sequence>
      <Sequence from={90 + TOOLS.length * 300 + 720} durationInFrames={150}><SceneOutro /></Sequence>
    </AbsoluteFill>
  );
};

export default AIToolsShowcaseFinal;