import { Router } from 'express';
import { body } from 'express-validator';
import { User } from '../models/User';
import { generateToken, verifyToken } from '../utils/jwt';

const userRouter = Router();

userRouter.post(
    '/signup',
    body('email').isEmail(),
    body('password').isLength({ min: 5 }),
    async (req, res) => {
        const { email, password } = req.body;
        const user = new User({ email, password });
        await user.save();
        const token = generateToken(user._id);
        res.send({ token });
    }
);

userRouter.post('/signin', async (req, res) => {
    const { email, password } = req.body;
    const user = await User.findOne({ email });
    if (!user || !(await user.comparePassword(password))) {
        return res.status(400).send('Invalid email or password');
    }
    const token = generateToken(user._id);
    res.send({ token });
});

userRouter.get('/me', async (req, res) => {
    const token = req.headers.authorization;
    if (!token) {
        return res.status(401).send('Unauthorized');
    }
    const payload = verifyToken(token);
    if (typeof payload === 'string' || !payload) {
        return res.status(401).send('Unauthorized');
    }
    const user = await User.findById(payload.id);
    res.send(user);
});

export { userRouter };
