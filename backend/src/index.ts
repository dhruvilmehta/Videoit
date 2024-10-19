import express, { Request, Response } from 'express';
import prisma from './prisma';
import dotenv from 'dotenv'
import cors from 'cors'

dotenv.config()

const app = express();
app.use(cors())

app.get("/", (req: Request, res: Response) => {
    res.send("Server running");
});

app.get("/getS3Url", async (req: Request, res: Response) => {
    const videoId = req.params.videoId;

    const response = await prisma.video.findFirst({
        where: {
            id: videoId
        },
        select: {
            url: true
        }
    })

    res.status(200).json({ "url": response?.url })
})

app.get("/getVideos", async (req: Request, res: Response) => {
    const response = await prisma.video.findMany();

    res.status(200).json(response)
})

app.listen(3000, () => {
    console.log("Listening on port 3000");
});
