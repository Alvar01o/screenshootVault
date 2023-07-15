import { Router } from 'express';
import { check, validationResult } from 'express-validator';
import { User, IUser } from '../models/User';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { Request, Response } from 'express-serve-static-core';

const router = Router();

// middleware para verificar el token
const verifyToken = (token: string): string | jwt.JwtPayload => {
    return jwt.verify(token, process.env.JWT_SECRET as string);
};

// Ruta de registro
router.post(
    '/register',
    [
        check('email', 'Please include a valid email').isEmail(),
        check(
            'password',
            'Please enter a password with 6 or more characters'
        ).isLength({ min: 6 })
    ],
    async (req: Request, res: Response) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        const { name, email, password } = req.body;

        try {
            let user = await User.findOne({ email });

            if (user) {
                return res
                    .status(400)
                    .json({ errors: [{ msg: 'User already exists' }] });
            }

            user = new User({
                name,
                email,
                password
            });

            const salt = await bcrypt.genSalt(10);

            user.password = await bcrypt.hash(password, salt);

            await user.save();

            const payload = {
                user: {
                    id: user.id
                }
            };

            jwt.sign(
                payload,
                process.env.JWT_SECRET as string,
                { expiresIn: 360000 },
                (err, token) => {
                    if (err) throw err;
                    res.json({ token, email:user?.email, name:user?.name });
                }
            );
        } catch (err) {
            if (err instanceof Error) {
                console.error(err.message);
            } else {
                console.error(err);
            }
            res.status(500).send('Server error');
        }
    }
);

// Ruta de login
router.post(
    '/login',
    [
        check('email', 'Please include a valid email').isEmail(),
        check('password', 'Password is required').exists()
    ],
    async (req: Request, res: Response) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        const { email, password } = req.body;

        try {
            let user = await User.findOne({ email });

            if (!user) {
                return res
                    .status(400)
                    .json({ errors: [{ msg: 'Invalid Credentials' }] });
            }

            const isMatch = await bcrypt.compare(password, user.password);

            if (!isMatch) {
                return res
                    .status(400)
                    .json({ errors: [{ msg: 'Invalid Credentials' }] });
            }

            const payload = {
                user: {
                    id: user.id
                }
            };

            jwt.sign(
                payload,
                process.env.JWT_SECRET as string,
                { expiresIn: 360000 },
                (err, token) => {
                    if (err) throw err;
                    res.json({ token });
                }
            );
        } catch (err) {
            if (err instanceof Error) {
                console.error(err.message);
            } else {
                console.error(err);
            }
            res.status(500).send('Server error');
        }
    }
);

// Ruta para obtener los datos del usuario autenticado
router.get('/data', async (req: Request, res: Response) => {
    // Extraer el token de la cabecera de autorización
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
        return res.sendStatus(401); // Si no hay token, retornar un error 401 (No autorizado)
    }
    
    try {
        const payload = verifyToken(token); // Verificar el token
        if (typeof payload === 'string' || payload === null) {
            return res.sendStatus(403); // Si el payload es una string o null, retornar un error 403 (Prohibido)
        }

        const user: IUser | null = await User.findById(payload.user.id); // Buscar al usuario en la base de datos utilizando el id del payload

        if (!user) {
            return res.sendStatus(404); // Si no se encuentra al usuario, retornar un error 404 (No encontrado)
        }

        // Retornar los datos del usuario (excepto la contraseña)
        return res.json({
            email: user.email,
            // Otras propiedades del usuario que quieras retornar...
        });
    } catch (err: any) {
        console.error(err.message);
        return res.sendStatus(403); // Si algo falla (p.ej. el token es inválido), retornar un error 403 (Prohibido)
    }
});

export { router as userRouter };
