import React, { useState, useEffect, useContext, useRef } from "react";
import { useParams } from "react-router-dom";
import io, { Socket } from "socket.io-client";
import axios from "axios";
import { AuthContext } from "../context/AuthContext";
import { Message } from "../types";
import "video.js/dist/video-js.css";
import VideoPlayer from "../components/VideoPlayer";

const VideoChat: React.FC = () => {
  const { videoId } = useParams<{ videoId: string }>();
  const [messages, setMessages] = useState<Message[]>([]);
  const [message, setMessage] = useState("");
  const auth = useContext(AuthContext);
  const [socket, setSocket] = useState<Socket | null>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const m3u8Url = `https://videoversioncontrol.s3-us-west-2.amazonaws.com/${videoId}/hls/playlist.m3u8`;

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const res = await axios.get(
          `http://localhost:5000/api/messages/${videoId}`,
          {
            headers: { Authorization: `Bearer ${auth?.token}` },
          },
        );
        setMessages(res.data);
      } catch (error) {
        console.error("Error fetching messages:", error);
        alert("Failed to load chat history");
      }
    };
    if (auth?.token) {
      fetchMessages();
    }
  }, [videoId, auth?.token]);

  useEffect(() => {
    if (!auth?.token) return;

    const newSocket = io("http://localhost:5000", {
      auth: { token: auth.token },
    });
    setSocket(newSocket);
    newSocket.emit("joinRoom", videoId);

    newSocket.on("message", (msg: Message) => {
      setMessages((prev) => {
        if (prev.some((m) => m.id === msg.id)) return prev; // Prevent duplicates
        return [...prev, msg];
      });
    });

    return () => {
      newSocket.disconnect();
    };
  }, [videoId, auth?.token]);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (message && socket) {
      socket.emit("chatMessage", { videoId, content: message });
      setMessage("");
    }
  };

  if (auth?.isLoading) {
    return (
      <div
        style={{
          textAlign: "center",
          color: "#333",
          height: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        Loading...
      </div>
    );
  }

  return (
    <div
      style={{
        height: "100vh",
        width: "100%",
        background: "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        boxSizing: "border-box",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          background: "#fff",
          borderRadius: "12px",
          boxShadow: "0 4px 20px rgba(0, 0, 0, 0.1)",
          width: "100%",
          maxWidth: "1200px",
          height: "100%",
          boxSizing: "border-box",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <h2
          style={{
            fontSize: "1.8rem",
            color: "#333",
            fontWeight: "600",
            textAlign: "center",
            padding: "10px 0",
          }}
        >
          Video Collaboration (ID: {videoId})
        </h2>
        <div
          style={{
            display: "flex",
            width: "100%",
            height: "calc(100% - 50px)", // Adjust for header
            boxSizing: "border-box",
          }}
        >
          <div
            style={{
              flex: "0 0 50%",
              boxSizing: "border-box",
              height: "100%",
            }}
          >
            <VideoPlayer
              m3u8Url={m3u8Url}
              onError={(error) => console.error(error)}
            />
          </div>
          <div
            style={{
              flex: "0 0 50%",
              boxSizing: "border-box",
              height: "100%",
              marginLeft: "20px",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <h3
              style={{
                fontSize: "1.3rem",
                color: "#333",
                fontWeight: "500",
                padding: "10px 0",
              }}
            >
              Chat
            </h3>
            <div
              ref={chatContainerRef}
              style={{
                border: "1px solid #e9ecef",
                flex: "1",
                overflowY: "scroll",
                background: "#f8f9fa",
                padding: "10px",
                borderRadius: "6px",
                boxSizing: "border-box",
              }}
            >
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  style={{
                    fontSize: "0.95rem",
                    color: "#333",
                  }}
                >
                  <strong
                    style={{
                      color: "#007bff",
                      fontWeight: "600",
                    }}
                  >
                    {msg.user.name} ({msg.user.role}):
                  </strong>{" "}
                  {msg.content}{" "}
                  <small style={{ color: "#777", fontSize: "0.8rem" }}>
                    {new Date(msg.createdAt).toLocaleTimeString()}
                  </small>
                </div>
              ))}
            </div>
            <form
              onSubmit={sendMessage}
              style={{
                padding: "10px 0",
              }}
            >
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type your message..."
                style={{
                  width: "100%",
                  padding: "10px",
                  fontSize: "1rem",
                  border: "1px solid #ccc",
                  borderRadius: "6px",
                  outline: "none",
                  boxSizing: "border-box",
                  transition: "border-color 0.3s",
                }}
                onFocus={(e) => (e.target.style.borderColor = "#007bff")}
                onBlur={(e) => (e.target.style.borderColor = "#ccc")}
              />
              <button
                type="submit"
                style={{
                  width: "100%",
                  padding: "10px",
                  fontSize: "1rem",
                  background: "#007bff",
                  color: "#fff",
                  border: "none",
                  borderRadius: "6px",
                  cursor: "pointer",
                  boxSizing: "border-box",
                  transition: "background 0.3s",
                }}
                onMouseOver={(e) =>
                  (e.currentTarget.style.background = "#0056b3")
                }
                onMouseOut={(e) =>
                  (e.currentTarget.style.background = "#007bff")
                }
              >
                Send
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VideoChat;
