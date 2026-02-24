import React from 'react';
import { Sequence } from 'remotion';
import { IntroScene } from './scenes/IntroScene';
import { ToolIntroScene } from './scenes/ToolIntroScene';
import { DimensionScene } from './scenes/DimensionScene';
import { ComparisonScene } from './scenes/ComparisonScene';
import { OutroScene } from './scenes/OutroScene';

// AI搜索工具数据
export const TOOLS = [
  { name: 'Kimi', color: '#00BFFF', icon: 'K' },
  { name: '秘塔', color: '#FF6B6B', icon: '秘' },
  { name: '360AI', color: '#4ECDC4', icon: '360' },
  { name: '天工', color: '#FFE66D', icon: '天' },
];

// 测评维度
export const DIMENSIONS = [
  { key: 'convenience', name: '体验便捷度', icon: '⚡', description: '打开即用，无需学习成本' },
  { key: 'accuracy', name: '答案准确度', icon: '🎯', description: '信息准确，不胡说八道' },
  { key: 'richness', name: '内容丰富度', icon: '📚', description: '答案全面，有深度有广度' },
  { key: 'source', name: '来源可靠性', icon: '🔗', description: '引用清晰，可追溯验证' },
  { key: 'speed', name: '响应速度', icon: '⏱️', description: '秒级响应，不卡顿' },
  { key: 'daily', name: '生活关联度', icon: '🛒', description: '购物/美食/出行等实用场景' },
];

export const ComparisonVideo = () => {
  return (
    <div style={{ backgroundColor: '#0a0a0a', width: '100%', height: '100%' }}>
      {/* 片头 - 0-3秒 */}
      <Sequence from={0} durationInFrames={90}>
        <IntroScene />
      </Sequence>

      {/* 工具介绍 - 3-7秒 */}
      <Sequence from={90} durationInFrames={120}>
        <ToolIntroScene />
      </Sequence>

      {/* 维度1：体验便捷度 - 7-12秒 */}
      <Sequence from={210} durationInFrames={150}>
        <DimensionScene dimension={DIMENSIONS[0]} scores={[4.5, 4, 3.5, 4]} />
      </Sequence>

      {/* 维度2：答案准确度 - 12-17秒 */}
      <Sequence from={360} durationInFrames={150}>
        <DimensionScene dimension={DIMENSIONS[1]} scores={[4, 4.5, 3, 4]} />
      </Sequence>

      {/* 维度3：内容丰富度 - 17-22秒 */}
      <Sequence from={510} durationInFrames={150}>
        <DimensionScene dimension={DIMENSIONS[2]} scores={[4.5, 4, 3.5, 4]} />
      </Sequence>

      {/* 综合对比 - 22-27秒 */}
      <Sequence from={660} durationInFrames={150}>
        <ComparisonScene />
      </Sequence>

      {/* 片尾 - 27-30秒 */}
      <Sequence from={810} durationInFrames={90}>
        <OutroScene />
      </Sequence>
    </div>
  );
};
