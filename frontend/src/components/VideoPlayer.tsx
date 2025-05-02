import React, { useEffect, useRef } from "react";
import videojs from "video.js";
import "video.js/dist/video-js.css";
import Player from "video.js/dist/types/player";

interface VideoPlayerProps {
  m3u8Url: string;
  onError: (error: string) => void;
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ m3u8Url, onError }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const playerRef = useRef<Player | null>(null);

  useEffect(() => {
    if (!videoRef.current) return;

    playerRef.current = videojs(videoRef.current, {
      controls: true,
      autoplay: false,
      preload: "auto",
      fluid: true,
      sources: [
        {
          src: m3u8Url,
          type: "application/x-mpegURL",
        },
      ],
    });

  }, [m3u8Url, onError]);

  return (
    <div data-vjs-player style={{ width: "100%", maxWidth: "800px" }}>
      <video ref={videoRef} className="video-js vjs-default-skin" />
    </div>
  );
};

export default VideoPlayer;
