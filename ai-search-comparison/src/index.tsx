import { Composition } from 'remotion';
import { ComparisonVideo } from './ComparisonVideo';

// 视频配置
export const VIDEO_WIDTH = 1080;
export const VIDEO_HEIGHT = 1920; // 竖屏 9:16
export const VIDEO_FPS = 30;
export const VIDEO_DURATION_IN_FRAMES = 900; // 30秒

export const RemotionRoot = () => {
  return (
    <Composition
      id="AI-Search-Comparison"
      component={ComparisonVideo}
      durationInFrames={VIDEO_DURATION_IN_FRAMES}
      fps={VIDEO_FPS}
      width={VIDEO_WIDTH}
      height={VIDEO_HEIGHT}
    />
  );
};

export default RemotionRoot;
