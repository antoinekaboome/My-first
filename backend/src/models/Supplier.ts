import mongoose, { Schema } from 'mongoose';

const supplierSchema = new Schema({
  name: { type: String, required: true },
});

export default mongoose.model('Supplier', supplierSchema);
