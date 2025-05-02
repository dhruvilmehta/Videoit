export interface User {
    id: number;
    email: string;
    name: string;
    role: string;
}

export interface JwtPayload {
    userId: number;
    role: string;
}