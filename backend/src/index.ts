import express, { Request, Response } from 'express';

const app = express();

app.get("/", (req: Request, res: Response) => {
    res.send("Server running");
});

app.listen(3000, () => {
    console.log("Listening on port 3000");
});
