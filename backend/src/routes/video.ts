import express from "express";
import { listVideos, initializeVideo } from "../controllers/video";

const router = express.Router();

router.get("/", listVideos);
router.post("/initialize", initializeVideo);

export default router;