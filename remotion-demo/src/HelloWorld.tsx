import {useCurrentFrame, useVideoConfig, interpolate} from 'remotion';

export const HelloWorld = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  
  // 透明度从 0 到 1（前 30 帧）
  const opacity = interpolate(frame, [0, 30], [0, 1]);
  
  // 缩放从 0.8 到 1（前 30 帧）
  const scale = interpolate(frame, [0, 30], [0.8, 1]);
  
  // 位置从左到右移动（整个视频）
  const x = interpolate(frame, [0, durationInFrames], [-200, 1920]);
  
  return (
    <div 
      style={{
        flex: 1,
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <h1
        style={{
          fontSize: 120,
          color: 'white',
          fontFamily: 'system-ui, sans-serif',
          fontWeight: 'bold',
          opacity,
          transform: `scale(${scale})`,
          textAlign: 'center',
        }}
      >
        Hello, Remotion!
        <br />
        <span style={{fontSize: 40, fontWeight: 'normal'}}>
          Frame: {frame}
        </span>
      </h1>
      
      {/* 移动的球 */}
      <div
        style={{
          position: 'absolute',
          bottom: 100,
          left: x,
          width: 100,
          height: 100,
          borderRadius: '50%',
          background: '#ff6b6b',
        }}
      />
    </div>
  );
};