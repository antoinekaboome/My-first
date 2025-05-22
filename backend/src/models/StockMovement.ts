import mongoose, { Schema } from 'mongoose';

const stockMovementSchema = new Schema({
  product: { type: Schema.Types.ObjectId, ref: 'Product' },
  quantity: Number,
  type: { type: String, enum: ['in', 'out'] },
  date: { type: Date, default: Date.now },
});

export default mongoose.model('StockMovement', stockMovementSchema);
