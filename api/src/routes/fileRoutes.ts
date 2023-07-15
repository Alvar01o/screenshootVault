import { Router, Request, Response } from 'express';
import mongoose from 'mongoose';
import Grid from 'gridfs-stream';

// Crear la conexión a GridFS
const conn = mongoose.createConnection(process.env.MONGO_URI as string);
let gfs: Grid.Grid;

conn.once('open', () => {
  // Iniciar stream
  gfs = Grid(conn.db, mongoose.mongo);
  gfs.collection('uploads');
});

const router = Router();

// Endpoint para listar los archivos
router.get('/files', (req: Request, res: Response) => {
  gfs.files.find().toArray((err:any, files:any) => {
    if (!files || files.length === 0) {
      return res.status(404).json({
        err: 'No files exist'
      });
    }

    // Si existen archivos, retornarlos
    return res.json(files);
  });
});

// Endpoint para obtener un archivo específico
router.get('/files/:filename', (req: Request, res: Response) => {
  gfs.files.findOne({ filename: req.params.filename }, (err:any, file:any) => {
    if (!file || file.length === 0) {
      return res.status(404).json({
        err: 'No file exists'
      });
    }

    // Si el archivo existe, retornarlo
    const readstream = gfs.createReadStream(file.filename);
    readstream.pipe(res);
  });
});

export { router as fileRouter };
