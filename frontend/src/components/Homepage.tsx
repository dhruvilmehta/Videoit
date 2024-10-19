import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export const Homepage = () => {
  const [videos, setVideos] = useState<any>([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios
      .get("http://localhost:3000/getVideos")
      .then((response) => setVideos(response.data))
      .catch((error) => {
        console.error("Error fetching videos:", error);
      });
  }, []);

  const handleClick = (id: string) => {
    // Navigate to /videoId when the div is clicked
    navigate(`/play/video${id}`);
  };

  return (
    <>
      {videos.map((video: any) => {
        return <div onClick={() => handleClick(video.id)}>{video.url}</div>;
      })}
    </>
  );
};
