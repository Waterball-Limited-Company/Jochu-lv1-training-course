import { sendError } from '../lib/errors.js';

export function requireAuth(req, res, next) {
  if (!req.session?.user) {
    return sendError(res, 401, 'UNAUTHENTICATED', 'Authentication is required');
  }
  req.user = req.session.user;
  return next();
}
