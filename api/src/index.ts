import dotenv from 'dotenv';
import express from 'express';
import mongoose from 'mongoose';
import { userRouter } from './routes/userRoutes';


const app = express();
const port = process.env.PORT || 3000;
dotenv.config();
if (!process.env.MONGO_URI) {
    throw new Error('MONGO_URI must be defined in the .env file');
}
// Conexión a MongoDB
mongoose.connect(process.env.MONGO_URI as string)
    .then(() => console.log('Connected to MongoDB'))
    .catch((error) => console.log(error));

app.use(express.json());

// Rutas
app.use('/api/users', userRouter);

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});