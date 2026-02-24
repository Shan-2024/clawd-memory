import { Composition, registerRoot } from 'remotion';
import { ComparisonVideo } from './ComparisonVideo';
import { ComparisonRadar } from './ComparisonRadar';

// 视频配置
export const VIDEO_WIDTH = 1080;
export const VIDEO_HEIGHT = 1920; // 竖屏 9:16
export const VIDEO_FPS = 30;
export const VIDEO_DURATION_IN_FRAMES = 900; // 30秒

// 雷达图配置
export const RADAR_DURATION = 180; // 6秒

export const RemotionRoot = () => {
  return (
    <>
      {/* 主视频 */}
      <Composition
        id="AI-Search-Comparison"
        component={ComparisonVideo}
        durationInFrames={VIDEO_DURATION_IN_FRAMES}
        fps={VIDEO_FPS}
        width={VIDEO_WIDTH}
        height={VIDEO_HEIGHT}
      />
      
      {/* 雷达图版本 */}
      <Composition
        id="Radar-Chart"
        component={ComparisonRadar}
        durationInFrames={RADAR_DURATION}
        fps={VIDEO_FPS}
        width={VIDEO_WIDTH}
        height={VIDEO_HEIGHT}
        defaultProps={{}}
      />
    </>
  );
};

export default RemotionRoot;

registerRoot(RemotionRoot);