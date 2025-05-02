import { Server, Socket } from "socket.io";
import { PrismaClient } from "@prisma/client";
import jwt from "jsonwebtoken";
import { JwtPayload } from "../types";

const prisma = new PrismaClient();

export const setupSocket = (io: Server) => {
    io.use((socket: Socket, next) => {
        const token = socket.handshake.auth.token;
        if (!token) {
            return next(new Error("Authentication error"));
        }
        try {
            const decoded = jwt.verify(token, process.env.JWT_SECRET!) as JwtPayload;
            socket.data.user = decoded;
            next();
        } catch (error) {
            next(new Error("Invalid token"));
        }
    });

    io.on("connection", (socket: Socket) => {
        console.log(`User ${socket.data.user.userId} connected`);

        socket.on("joinRoom", (videoId: string) => {
            socket.join(videoId);
            console.log(`User ${socket.data.user.userId} joined room ${videoId}`);
        });

        socket.on("chatMessage", async ({ videoId, content }: { videoId: string; content: string }) => {
            const message = await prisma.message.create({
                data: {
                    content,
                    userId: socket.data.user.userId,
                    videoId: parseInt(videoId),
                },
                include: { user: { select: { name: true, role: true } } },
            });
            io.to(videoId).emit("message", {
                content: message.content,
                user: message.user,
                createdAt: message.createdAt,
            });
        });

        socket.on("disconnect", () => {
            console.log(`User ${socket.data.user.userId} disconnected`);
        });
    });
};