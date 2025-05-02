import { Request, Response } from "express";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export const getMessages = async (req: Request, res: Response) => {
    const { videoId } = req.params;
    try {
        const messages = await prisma.message.findMany({
            where: { videoId: parseInt(videoId) },
            include: { user: { select: { name: true, role: true } } },
            orderBy: { createdAt: "asc" },
        });
        res.json(messages);
    } catch (error) {
        res.status(500).json({ message: "Error fetching messages" });
    }
};