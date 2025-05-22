import mongoose, { Schema } from 'mongoose';

const productSchema = new Schema({
  name: { type: String, required: true },
  category: { type: Schema.Types.ObjectId, ref: 'Category' },
  supplier: { type: Schema.Types.ObjectId, ref: 'Supplier' },
  quantity: { type: Number, default: 0 },
  threshold: { type: Number, default: 0 },
});

export default mongoose.model('Product', productSchema);
