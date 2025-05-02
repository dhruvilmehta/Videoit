export interface User {
    id: number;
    email: string;
    name: string;
    role: string;
}

export interface Video {
    id: number;
    videoId: string;
    title: string;
    owner: { name: string; email: string };
    createdAt: string;
}

export interface Message {
    id: number; // Required, as backend includes it
    content: string;
    user: { name: string; role: string };
    createdAt: string;
}