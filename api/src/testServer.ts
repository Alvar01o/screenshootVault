import request from 'supertest';
import dotenv from 'dotenv';
import express from 'express';
import mongoose from 'mongoose';
import { userRouter } from './routes/userRoutes';
import { fileRouter } from './routes/fileRoutes';
import cors from 'cors';


const app = express();
const port = 3005;
dotenv.config();
if (!process.env.MONGO_URI) {
  throw new Error('MONGO_URI must be defined in the .env file');
}
// Conexión a MongoDB
mongoose.connect(process.env.MONGO_URI as string)
    .then()
    .catch((error) => console.log(error));

// Add middleware and routes to the app
app.use(express.json());
app.use(cors({
  origin: process.env.FRONT_END_URL
}));
// Rutas
app.use('/api/users', userRouter);
app.use('/api/files', fileRouter);
// Export a function that starts the server and returns a supertest agent
export const startTestServer = () => {
  const server = app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
  });
  const agent = request.agent(server);

  return agent;
};

