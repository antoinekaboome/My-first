import { Router } from 'express';
import Category from '../models/Category';
import { authorize } from '../middleware/auth';

const router = Router();

router.post('/', authorize(['admin']), async (req, res) => {
  const cat = new Category(req.body);
  await cat.save();
  res.status(201).json(cat);
});

router.get('/', async (_req, res) => {
  const cats = await Category.find();
  res.json(cats);
});

router.put('/:id', authorize(['admin']), async (req, res) => {
  const cat = await Category.findByIdAndUpdate(req.params.id, req.body, { new: true });
  res.json(cat);
});

router.delete('/:id', authorize(['admin']), async (req, res) => {
  await Category.findByIdAndDelete(req.params.id);
  res.status(204).end();
});

export default router;
