import { Route, Routes } from "react-router-dom";
import "./App.css";
import { Homepage } from "./components/Homepage";
import { PlayerPage } from "./components/PlayerPage";

function App() {
  const videoJsOptions = {
    autoplay: true,
    controls: true,
    responsive: true,
    fluid: true,
    sources: [
      {
        src: "/path/to/video.mp4",
        type: "video/mp4",
      },
    ],
  };

  return (
    <>
    <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/play/:videoId" element={<PlayerPage />} />
    </Routes>
    </>
  );
}

export default App;
