import { Request, Response, NextFunction } from 'express';
import AuditLog from '../models/AuditLog';
import { AuthRequest } from './auth';

export const auditLogger = async (
  req: AuthRequest,
  res: Response,
  next: NextFunction
) => {
  res.on('finish', async () => {
    try {
      await AuditLog.create({
        user: req.user?._id,
        method: req.method,
        path: req.originalUrl,
        status: res.statusCode,
      });
    } catch (err) {
      console.error('Audit log error', err);
    }
  });
  next();
};
