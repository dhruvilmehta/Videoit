import express from "express";
import { signup, login, verifyToken } from "../controllers/auth";

const router = express.Router();

router.post("/signup", signup);
router.post("/login", login);
router.get("/verify", verifyToken);

export default router;