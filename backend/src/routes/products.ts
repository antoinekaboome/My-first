import { Router } from 'express';
import { body, validationResult } from 'express-validator';
import Product from '../models/Product';
import { authorize } from '../middleware/auth';

const router = Router();

router.post(
  '/',
  authorize(['admin']),
  [body('name').isString(), body('quantity').isNumeric()],
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ errors: errors.array() });
    const product = new Product(req.body);
    await product.save();
    res.status(201).json(product);
  }
);

router.get('/', async (_req, res) => {
  const products = await Product.find().populate('category supplier');
  res.json(products);
});

router.put('/:id', authorize(['admin']), async (req, res) => {
  const product = await Product.findByIdAndUpdate(req.params.id, req.body, { new: true });
  res.json(product);
});

router.delete('/:id', authorize(['admin']), async (req, res) => {
  await Product.findByIdAndDelete(req.params.id);
  res.status(204).end();
});

export default router;
