import { Request, Response } from "express";
import { PrismaClient } from "@prisma/client";
import fs from "fs";
import path from "path";

const prisma = new PrismaClient();

export const listVideos = async (req: Request, res: Response) => {
    const videos = await prisma.video.findMany({
        where: req.user?.role === "owner" ? { ownerId: req.user.userId } : {},
        include: { owner: { select: { name: true, email: true } } },
    });
    res.json(videos);
};

// Placeholder for CLI integration
export const initializeVideo = async (req: Request, res: Response) => {
    const { videoId, title } = req.body;
    // Assume video-processor CLI has run and created a directory with videoId
    const videoDir = path.join(__dirname, "../../../cli/newest", videoId);
    if (!fs.existsSync(videoDir)) {
        return res.status(400).json({ message: "Video directory not found. Run video-processor first." });
    }
    try {
        const video = await prisma.video.create({
            data: {
                videoId,
                title,
                ownerId: req.user!.userId,
            },
        });
        // TODO: Implement S3 upload here
        res.json(video);
    } catch (error) {
        res.status(400).json({ message: "Error initializing video" });
    }
};