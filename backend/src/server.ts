import express from 'express';
import mongoose from 'mongoose';
import dotenv from 'dotenv';
import helmet from 'helmet';
import cors from 'cors';
import rateLimit from 'express-rate-limit';
import authRoutes from './routes/auth';
import productRoutes from './routes/products';
import categoryRoutes from './routes/categories';
import supplierRoutes from './routes/suppliers';
import stockRoutes from './routes/stock';
import { authMiddleware } from './middleware/auth';
import { auditLogger } from './middleware/audit';

dotenv.config();

const app = express();

app.use(helmet());
app.use(cors({ origin: process.env.CORS_ORIGIN || 'http://localhost:3000' }));
app.use(express.json());
app.use(
  rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100,
  })
);

app.use('/api/auth', authRoutes);
app.use('/api/products', authMiddleware, auditLogger, productRoutes);
app.use('/api/categories', authMiddleware, auditLogger, categoryRoutes);
app.use('/api/suppliers', authMiddleware, auditLogger, supplierRoutes);
app.use('/api/stock', authMiddleware, auditLogger, stockRoutes);

const PORT = process.env.PORT || 5000;
const MONGO_URI = process.env.MONGO_URI || '';

mongoose
  .connect(MONGO_URI)
  .then(() => {
    console.log('Connected to MongoDB');
    if (process.env.NODE_ENV !== 'test') {
      app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
    }
  })
  .catch((err) => console.error(err));

export default app;
