import { Composition, registerRoot } from 'remotion';
import { AIToolsShowcase } from './Video';

export const RemotionRoot = () => {
  return (
    <Composition
      id="AI-Tools-Showcase"
      component={AIToolsShowcase}
      durationInFrames={5400}  // 3分钟 = 180秒 @30fps
      fps={30}
      width={1080}
      height={1920}  // 竖屏 9:16
      defaultProps={{}}
    />
  );
};

registerRoot(RemotionRoot);