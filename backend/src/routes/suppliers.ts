import { Router } from 'express';
import Supplier from '../models/Supplier';
import { authorize } from '../middleware/auth';

const router = Router();

router.post('/', authorize(['admin']), async (req, res) => {
  const sup = new Supplier(req.body);
  await sup.save();
  res.status(201).json(sup);
});

router.get('/', async (_req, res) => {
  const sups = await Supplier.find();
  res.json(sups);
});

router.put('/:id', authorize(['admin']), async (req, res) => {
  const sup = await Supplier.findByIdAndUpdate(req.params.id, req.body, { new: true });
  res.json(sup);
});

router.delete('/:id', authorize(['admin']), async (req, res) => {
  await Supplier.findByIdAndDelete(req.params.id);
  res.status(204).end();
});

export default router;
