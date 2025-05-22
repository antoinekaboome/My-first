import mongoose, { Schema } from 'mongoose';

const auditLogSchema = new Schema({
  user: { type: Schema.Types.ObjectId, ref: 'User' },
  method: String,
  path: String,
  status: Number,
  timestamp: { type: Date, default: Date.now },
});

export default mongoose.model('AuditLog', auditLogSchema);
