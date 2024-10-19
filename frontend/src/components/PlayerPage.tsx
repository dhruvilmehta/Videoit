import { useParams } from "react-router-dom";
import Player from "./Player";

export const PlayerPage = () => {
  const videoId = useParams();

  const videoJsOptions = {
    autoplay: true,
    controls: true,
    responsive: true,
    fluid: true,
    sources: [
      {
        src: `https://videohlsstreams.s3.amazonaws.com/${videoId.videoId}/playlist.m3u8`,
        type: "application/x-mpegURL",
      },
    ],
  };

  return (
    <>
      <Player options={videoJsOptions} />
    </>
  );
};
