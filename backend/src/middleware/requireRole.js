import { sendError } from '../lib/errors.js';

export function requireRole(role) {
  return function roleGate(req, res, next) {
    if (req.user?.role !== role) {
      return sendError(
        res,
        403,
        'FORBIDDEN',
        'Facility administrator role is required',
      );
    }
    return next();
  };
}
