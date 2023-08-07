import jwt from 'jsonwebtoken';

export const generateToken = (userId: string) => {
    return jwt.sign({ id: userId }, 'mysecretkey', { expiresIn: '1d' });
}

export const verifyToken = (token: string) => {
    try {
        return jwt.verify(token, 'mysecretkey');
    } catch (e) {
        console.log(e);
        return null;
    }
}
