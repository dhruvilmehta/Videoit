import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import { Video } from "../types";

const Dashboard: React.FC = () => {
  const [videos, setVideos] = useState<Video[]>([]);
  const [title, setTitle] = useState("");
  const [videoId, setVideoId] = useState("");
  const auth = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchVideos = async () => {
      const res = await axios.get("http://localhost:5000/api/videos", {
        headers: { Authorization: `Bearer ${auth?.token}` },
      });
      setVideos(res.data);
    };
    fetchVideos();
  }, [auth?.token]);

  const handleInitialize = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post(
        "http://localhost:5000/api/videos/initialize",
        { videoId, title },
        { headers: { Authorization: `Bearer ${auth?.token}` } },
      );
      setTitle("");
      setVideoId("");
      const res = await axios.get("http://localhost:5000/api/videos", {
        headers: { Authorization: `Bearer ${auth?.token}` },
      });
      setVideos(res.data);
    } catch (error) {
      alert(`Failed to initialize video ${error}`);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
        padding: "40px 20px",
        display: "flex",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          background: "#fff",
          padding: "40px",
          borderRadius: "12px",
          boxShadow: "0 4px 20px rgba(0, 0, 0, 0.1)",
          width: "100%",
          maxWidth: "800px",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "30px",
          }}
        >
          <h2
            style={{
              fontSize: "2rem",
              color: "#333",
              fontWeight: "600",
              margin: 0,
            }}
          >
            Dashboard
          </h2>
          <button
            onClick={() => auth?.logout()}
            style={{
              padding: "10px 20px",
              fontSize: "1rem",
              background: "#dc3545",
              color: "#fff",
              border: "none",
              borderRadius: "6px",
              cursor: "pointer",
              transition: "background 0.3s",
            }}
            onMouseOver={(e) => (e.currentTarget.style.background = "#b02a37")}
            onMouseOut={(e) => (e.currentTarget.style.background = "#dc3545")}
          >
            Logout
          </button>
        </div>

        {auth?.user?.role === "owner" && (
          <div style={{ marginBottom: "40px" }}>
            <h3
              style={{
                fontSize: "1.5rem",
                color: "#333",
                marginBottom: "20px",
                fontWeight: "500",
              }}
            >
              Initialize Video
            </h3>
            <form onSubmit={handleInitialize}>
              <div style={{ marginBottom: "20px" }}>
                <label
                  style={{
                    display: "block",
                    marginBottom: "8px",
                    fontSize: "1rem",
                    color: "#555",
                    fontWeight: "500",
                  }}
                >
                  Video ID:
                </label>
                <input
                  type="text"
                  value={videoId}
                  onChange={(e) => setVideoId(e.target.value)}
                  required
                  style={{
                    width: "100%",
                    padding: "12px",
                    fontSize: "1rem",
                    border: "1px solid #ccc",
                    borderRadius: "6px",
                    outline: "none",
                    transition: "border-color 0.3s",
                  }}
                  onFocus={(e) => (e.target.style.borderColor = "#007bff")}
                  onBlur={(e) => (e.target.style.borderColor = "#ccc")}
                />
              </div>
              <div style={{ marginBottom: "20px" }}>
                <label
                  style={{
                    display: "block",
                    marginBottom: "8px",
                    fontSize: "1rem",
                    color: "#555",
                    fontWeight: "500",
                  }}
                >
                  Title:
                </label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                  style={{
                    width: "100%",
                    padding: "12px",
                    fontSize: "1rem",
                    border: "1px solid #ccc",
                    borderRadius: "6px",
                    outline: "none",
                    transition: "border-color 0.3s",
                  }}
                  onFocus={(e) => (e.target.style.borderColor = "#007bff")}
                  onBlur={(e) => (e.target.style.borderColor = "#ccc")}
                />
              </div>
              <button
                type="submit"
                style={{
                  width: "100%",
                  padding: "12px",
                  fontSize: "1rem",
                  background: "#007bff",
                  color: "#fff",
                  border: "none",
                  borderRadius: "6px",
                  cursor: "pointer",
                  transition: "background 0.3s",
                }}
                onMouseOver={(e) =>
                  (e.currentTarget.style.background = "#0056b3")
                }
                onMouseOut={(e) =>
                  (e.currentTarget.style.background = "#007bff")
                }
              >
                Initialize
              </button>
            </form>
          </div>
        )}

        <h3
          style={{
            fontSize: "1.5rem",
            color: "#333",
            marginBottom: "20px",
            fontWeight: "500",
          }}
        >
          Videos
        </h3>
        <ul
          style={{
            listStyle: "none",
            padding: 0,
          }}
        >
          {videos.map((video) => (
            <li
              key={video.id}
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "15px",
                marginBottom: "10px",
                background: "#f8f9fa",
                borderRadius: "6px",
                border: "1px solid #e9ecef",
              }}
            >
              <span
                style={{
                  fontSize: "1rem",
                  color: "#333",
                }}
              >
                {video.title} (Owner: {video.owner.name})
              </span>
              <button
                onClick={() => navigate(`/video/${video.videoId}`)}
                style={{
                  padding: "8px 16px",
                  fontSize: "0.9rem",
                  background: "#28a745",
                  color: "#fff",
                  border: "none",
                  borderRadius: "6px",
                  cursor: "pointer",
                  transition: "background 0.3s",
                }}
                onMouseOver={(e) =>
                  (e.currentTarget.style.background = "#218838")
                }
                onMouseOut={(e) =>
                  (e.currentTarget.style.background = "#28a745")
                }
              >
                View & Chat
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;
