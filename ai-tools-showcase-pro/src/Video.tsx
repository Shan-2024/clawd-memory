import {
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
  Easing,
  Sequence,
  AbsoluteFill,
} from 'remotion';
import React from 'react';

// ==================== 配置 ====================
const CONFIG = {
  fps: 30,
  width: 1920,
  height: 1080,
  durationInFrames: 5400,
};

// 苹果风格设计系统
const THEME = {
  colors: {
    background: '#FFFFFF',
    primary: '#1D1D1F',
    secondary: '#86868B',
    accent: '#0071E3',
    surface: '#F5F5F7',
    divider: '#D2D2D7',
  },
  fonts: {
    family: '"PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif',
    weights: {
      regular: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
  },
  spacing: {
    xs: 8,
    sm: 16,
    md: 24,
    lg: 32,
    xl: 48,
    xxl: 64,
  },
};

// ==================== 动画工具函数 ====================

const useFadeIn = (delay = 0, duration = 30) => {
  const frame = useCurrentFrame();
  return interpolate(frame - delay, [0, duration], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
};

const useSlideUp = (delay = 0, distance = 40) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({
    frame: frame - delay,
    fps,
    config: { damping: 25, stiffness: 120, mass: 0.8 },
  });
  return {
    opacity: progress,
    transform: `translateY(${(1 - progress) * distance}px)`,
  };
};

const useScaleIn = (delay = 0) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({
    frame: frame - delay,
    fps,
    config: { damping: 20, stiffness: 100, mass: 0.5 },
  });
  return {
    opacity: progress,
    transform: `scale(${0.8 + progress * 0.2})`,
  };
};

// ==================== 场景组件 ====================

const IntroScene: React.FC = () => {
  const { opacity: titleOpacity, transform: titleTransform } = useSlideUp(0);
  const { opacity: subtitleOpacity, transform: subtitleTransform } = useSlideUp(30);
  
  return (
    <AbsoluteFill
      style={{
        backgroundColor: THEME.colors.background,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: THEME.fonts.family,
      }}
    >
      <div style={{ opacity: titleOpacity, transform: titleTransform, textAlign: 'center' }}>
        <h1 style={{ fontSize: 120, fontWeight: THEME.fonts.weights.bold, color: THEME.colors.primary, letterSpacing: '-0.03em', margin: 0, lineHeight: 1.1 }}>
          AI 工具全景
        </h1>
      </div>
      <div style={{ opacity: subtitleOpacity, transform: subtitleTransform, marginTop: THEME.spacing.lg }}>
        <p style={{ fontSize: 48, fontWeight: THEME.fonts.weights.regular, color: THEME.colors.secondary, letterSpacing: '0.05em', margin: 0 }}>
          2026 年度精选
        </p>
      </div>
      <div style={{ width: 80, height: 4, backgroundColor: THEME.colors.accent, borderRadius: 2, marginTop: THEME.spacing.xxl, opacity: subtitleOpacity, transform: `scaleX(${subtitleOpacity})`, transformOrigin: 'center' }} />
    </AbsoluteFill>
  );
};

// AI 工具数据
const AI_TOOLS_DATA = [
  { category: '对话与写作', tools: [{ name: 'ChatGPT', company: 'OpenAI', desc: '全能型 AI 助手' }, { name: 'Claude', company: 'Anthropic', desc: '深度推理与代码' }, { name: 'Gemini', company: 'Google', desc: '多模态智能' }] },
  { category: '视频生成', tools: [{ name: 'Sora', company: 'OpenAI', desc: '高质量视频生成' }, { name: 'Veo', company: 'Google', desc: '4K 视频合成' }, { name: 'HeyGen', company: 'HeyGen', desc: '数字人视频' }] },
  { category: '图像与设计', tools: [{ name: 'Midjourney', company: 'Midjourney', desc: '艺术创作' }, { name: 'DALL-E 3', company: 'OpenAI', desc: '图像生成' }, { name: 'Firefly', company: 'Adobe', desc: '创意工具套件' }] },
  { category: '效率与开发', tools: [{ name: 'Cursor', company: 'Cursor', desc: 'AI 代码编辑器' }, { name: 'Notion AI', company: 'Notion', desc: '智能笔记' }, { name: 'Zapier AI', company: 'Zapier', desc: '工作流自动化' }] },
];

const ToolCard: React.FC<{ tool: { name: string; company: string; desc: string }; index: number; isActive: boolean }> = ({ tool, index, isActive }) => {
  const delay = index * 10;
  const { opacity, transform } = useSlideUp(isActive ? delay : -100);
  
  return (
    <div style={{ opacity, transform, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: THEME.spacing.sm, padding: `${THEME.spacing.xl}px`, backgroundColor: THEME.colors.surface, borderRadius: 20, minWidth: 280, maxWidth: 320, textAlign: 'center' }}>
      <p style={{ fontSize: 16, fontWeight: THEME.fonts.weights.medium, color: THEME.colors.secondary, margin: 0, letterSpacing: '0.02em' }}>{tool.company}</p>
      <h3 style={{ fontSize: 40, fontWeight: THEME.fonts.weights.semibold, color: THEME.colors.primary, margin: 0, letterSpacing: '-0.01em' }}>{tool.name}</h3>
      <div style={{ width: 40, height: 2, backgroundColor: THEME.colors.divider, margin: `${THEME.spacing.sm}px 0` }} />
      <p style={{ fontSize: 20, fontWeight: THEME.fonts.weights.regular, color: THEME.colors.secondary, margin: 0 }}>{tool.desc}</p>
    </div>
  );
};

const CategoryScene: React.FC<{ categoryIndex: number }> = ({ categoryIndex }) => {
  const data = AI_TOOLS_DATA[categoryIndex];
  const { opacity: headerOpacity, transform: headerTransform } = useSlideUp(0);
  
  return (
    <AbsoluteFill style={{ backgroundColor: THEME.colors.background, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: THEME.fonts.family }}>
      <div style={{ opacity: headerOpacity, transform: headerTransform, textAlign: 'center', marginBottom: THEME.spacing.xxl }}>
        <p style={{ fontSize: 20, fontWeight: THEME.fonts.weights.medium, color: THEME.colors.secondary, letterSpacing: '0.15em', textTransform: 'uppercase', margin: 0, marginBottom: THEME.spacing.sm }}>类别 {categoryIndex + 1} / {AI_TOOLS_DATA.length}</p>
        <h2 style={{ fontSize: 72, fontWeight: THEME.fonts.weights.bold, color: THEME.colors.primary, letterSpacing: '-0.02em', margin: 0 }}>{data.category}</h2>
      </div>
      <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems: 'center', gap: THEME.spacing.xl }}>
        {data.tools.map((tool, index) => <ToolCard key={tool.name} tool={tool} index={index} isActive={true} />)}
      </div>
    </AbsoluteFill>
  );
};

const InsightsScene: React.FC = () => {
  const { opacity, transform } = useSlideUp(0);
  const stats = [{ value: '12', label: '款精选工具', delay: 20 }, { value: '4', label: '大核心类别', delay: 35 }, { value: '8', label: '家领先公司', delay: 50 }, { value: '3', label: '分钟概览', delay: 65 }];
  
  return (
    <AbsoluteFill style={{ backgroundColor: THEME.colors.background, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: THEME.fonts.family }}>
      <div style={{ opacity, transform, textAlign: 'center' }}>
        <h2 style={{ fontSize: 64, fontWeight: THEME.fonts.weights.bold, color: THEME.colors.primary, margin: 0, marginBottom: THEME.spacing.xxl * 2, letterSpacing: '-0.02em' }}>全景概览</h2>
      </div>
      <div style={{ display: 'flex', gap: THEME.spacing.xxl * 3, marginBottom: THEME.spacing.xxl * 2 }}>
        {stats.map((stat, index) => {
          const { opacity: statOpacity, transform: statTransform } = useSlideUp(stat.delay);
          return (
            <div key={stat.label} style={{ opacity: statOpacity, transform: statTransform, textAlign: 'center' }}>
              <span style={{ fontSize: 96, fontWeight: THEME.fonts.weights.light, color: THEME.colors.primary, letterSpacing: '-0.03em' }}>{stat.value}</span>
              <span style={{ fontSize: 32, fontWeight: THEME.fonts.weights.regular, color: THEME.colors.secondary }}> {stat.label.replace(/\d+/, '')}</span>
              <p style={{ fontSize: 20, fontWeight: THEME.fonts.weights.medium, color: THEME.colors.secondary, margin: 0, marginTop: THEME.spacing.sm, letterSpacing: '0.05em' }}>{stat.label}</p>
            </div>
          );
        })}
      </div>
      <div style={{ opacity: useFadeIn(80), padding: `0 ${THEME.spacing.xxl}px`, textAlign: 'center' }}>
        <p style={{ fontSize: 28, fontWeight: THEME.fonts.weights.regular, color: THEME.colors.secondary, lineHeight: 1.6, margin: 0 }}>工具选择应基于具体场景，<br />而非盲目追求最新技术</p>
      </div>
    </AbsoluteFill>
  );
};

const OutroScene: React.FC = () => {
  const { opacity: titleOpacity, transform: titleTransform } = useScaleIn(0);
  const { opacity: subtitleOpacity, transform: subtitleTransform } = useSlideUp(30);
  const lineOpacity = useFadeIn(60);
  
  return (
    <AbsoluteFill style={{ backgroundColor: THEME.colors.background, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: THEME.fonts.family }}>
      <div style={{ opacity: subtitleOpacity, transform: subtitleTransform, marginBottom: THEME.spacing.lg }}>
        <p style={{ fontSize: 32, fontWeight: THEME.fonts.weights.medium, color: THEME.colors.secondary, letterSpacing: '0.1em', margin: 0 }}>感谢观看</p>
      </div>
      <div style={{ opacity: titleOpacity, transform: titleTransform, textAlign: 'center' }}>
        <h2 style={{ fontSize: 80, fontWeight: THEME.fonts.weights.bold, color: THEME.colors.primary, letterSpacing: '-0.02em', margin: 0, lineHeight: 1.2 }}>持续探索  明智选择</h2>
      </div>
      <div style={{ width: 80, height: 4, backgroundColor: THEME.colors.accent, borderRadius: 2, marginTop: THEME.spacing.xxl * 2, opacity: lineOpacity, transform: `scaleX(${lineOpacity})`, transformOrigin: 'center' }} />
    </AbsoluteFill>
  );
};

// ==================== 主组件 ====================

export const AIToolsShowcasePro: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: THEME.colors.background }}>
      <Sequence from={0} durationInFrames={150}><IntroScene /></Sequence>
      <Sequence from={150} durationInFrames={600}><CategoryScene categoryIndex={0} /></Sequence>
      <Sequence from={750} durationInFrames={600}><CategoryScene categoryIndex={1} /></Sequence>
      <Sequence from={1350} durationInFrames={600}><CategoryScene categoryIndex={2} /></Sequence>
      <Sequence from={1950} durationInFrames={600}><CategoryScene categoryIndex={3} /></Sequence>
      <Sequence from={2550} durationInFrames={450}><InsightsScene /></Sequence>
      <Sequence from={3000} durationInFrames={600}><OutroScene /></Sequence>
      <Sequence from={3600} durationInFrames={1800}><AbsoluteFill style={{ backgroundColor: THEME.colors.background }} /></Sequence>
    </AbsoluteFill>
  );
};

export default AIToolsShowcasePro;