import express from "express";
import cors from "cors";
import { createServer } from "http";
import { Server } from "socket.io";
import dotenv from "dotenv";
import authRoutes from "./routes/auth";
import videoRoutes from "./routes/video";
import messageRoutes from "./routes/message";
import { setupSocket } from "./sockets/chat";
import { authMiddleware } from "./middleware/auth";

dotenv.config();

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
    cors: { origin: "http://localhost:5173" },
});

app.use(cors({ origin: "http://localhost:5173" }));
app.use(express.json());

app.use("/api/auth", authRoutes);
app.use("/api/videos", authMiddleware, videoRoutes);
app.use("/api/messages", authMiddleware, messageRoutes);

setupSocket(io);

const PORT = process.env.PORT || 5000;
httpServer.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});