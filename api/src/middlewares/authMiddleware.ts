import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { User, IUser, currentuser } from '../models/User';

const currentUser: currentuser = {
  id: '',
  email: '',
  name: ''
}
const signToken = (payload: any) => {
  return jwt.sign(payload, process.env.JWT_SECRET as string, {
    expiresIn: '12h'
  });
};

// middleware para verificar el token
const verifyToken = (token: string): string | jwt.JwtPayload => {
  return jwt.verify(token, process.env.JWT_SECRET as string);
};

const authMiddleware = async (req: Request, res: Response, next: NextFunction) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.sendStatus(401).json({
      error: 'Unauthorized'
    }); // Si no hay token, retornar un error 401 (No autorizado)
  }

  try {
    const payload = verifyToken(token); // Verificar el token
    if (typeof payload === 'string' || payload === null) {
      return res.sendStatus(403).json({error: 'weird error'}); // Si el payload es una string o null, retornar un error 403 (Prohibido)
    }
    const user: IUser | null = await User.findById(payload.user.id); // Buscar al usuario en la base de datos utilizando el id del payload
    if (!user) {
      return res.sendStatus(404).json({
        error: 'User not found'
      }); // Si no se encuentra al usuario, retornar un error 404 (No encontrado)
    }
    currentUser.id = user?._id as string;
    currentUser.email = user?.email as string;
    currentUser.name = user?.name as string;
    // Aquí podrías verificar el token y hacer otras validaciones
    next();
  } catch (err: any) {
    return res.sendStatus(403).json({error:'Invalid Token'}); // Si algo falla (p.ej. el token es inválido), retornar un error 403 (Prohibido)
  }
};

export { authMiddleware, verifyToken, signToken, currentUser };