import { Router } from 'express';
import StockMovement from '../models/StockMovement';
import Product from '../models/Product';
import { authorize } from '../middleware/auth';

const router = Router();

router.post('/', authorize(['admin', 'employee']), async (req, res) => {
  const move = new StockMovement(req.body);
  await move.save();
  const product = await Product.findById(move.product);
  if (product) {
    product.quantity += move.type === 'in' ? move.quantity : -move.quantity;
    await product.save();
  }
  res.status(201).json(move);
});

router.get('/', authorize(['admin', 'employee']), async (_req, res) => {
  const moves = await StockMovement.find().populate('product');
  res.json(moves);
});

export default router;
