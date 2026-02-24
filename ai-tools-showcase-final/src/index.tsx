import { Composition, registerRoot } from 'remotion';
import { AIToolsShowcaseFinal } from './Video';

export const RemotionRoot = () => {
  return (
    <Composition
      id="AI-Tools-Showcase-Final"
      component={AIToolsShowcaseFinal}
      durationInFrames={5400}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};

registerRoot(RemotionRoot);