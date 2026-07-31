import { Router } from 'express';
import bcrypt from 'bcrypt';
import { userModel } from '../models/user.js';
import { sendError } from '../lib/errors.js';
import { regenerateSession, saveSession, toPublicUser } from '../lib/session.js';
import { requireAuth } from '../middleware/auth.js';

const router = Router();

router.post('/login', async (req, res, next) => {
  try {
    const { username, password } = req.body ?? {};
    if (typeof username !== 'string' || !username.trim() || typeof password !== 'string') {
      return sendError(res, 400, 'VALIDATION_ERROR', 'username and password are required');
    }

    const user = await userModel.findByUsername(username);
    if (!user || !(await bcrypt.compare(password, user.password_hash))) {
      return sendError(res, 401, 'INVALID_CREDENTIALS', 'Invalid username or password');
    }

    const publicUser = toPublicUser(user);
    await regenerateSession(req);
    req.session.user = publicUser;
    await saveSession(req);
    return res.status(200).json({ authenticated: true, user: publicUser });
  } catch (error) {
    return next(error);
  }
});

router.post('/logout', requireAuth, async (req, res, next) => {
  try {
    await new Promise((resolve, reject) => {
      req.session.destroy((error) => (error ? reject(error) : resolve()));
    });
    res.clearCookie('meeting.sid');
    return res.status(200).json({ authenticated: false });
  } catch (error) {
    return next(error);
  }
});

router.get('/me', requireAuth, (req, res) => {
  return res.status(200).json({ authenticated: true, user: req.user });
});

export default router;
