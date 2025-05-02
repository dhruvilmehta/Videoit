import express from "express";
import { getMessages } from "../controllers/message";
import { authMiddleware } from "../middleware/auth";

const router = express.Router();

router.get("/:videoId", authMiddleware, getMessages);

export default router;