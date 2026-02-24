import { Composition, registerRoot } from 'remotion';
import { AIToolsShowcasePro } from './Video';

export const RemotionRoot = () => {
  return (
    <Composition
      id="AI-Tools-Showcase-Pro"
      component={AIToolsShowcasePro}
      durationInFrames={5400}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{}}
    />
  );
};

registerRoot(RemotionRoot);