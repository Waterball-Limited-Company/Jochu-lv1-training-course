import express from 'express';
import session from 'express-session';
import connectPgSimple from 'connect-pg-simple';
import { pool } from './db/pool.js';
import authRoutes from './routes/auth.js';
import roomsRoutes from './routes/rooms.js';
import bookingsRoutes from './routes/bookings.js';
import maintenanceRoutes from './routes/maintenance.js';
import overviewRoutes from './routes/overview.js';

export function createApp() {
  const app = express();
  app.use(express.json());
  const PgStore = connectPgSimple(session);
  app.use(
    session({
      store: new PgStore({
        pool,
        tableName: 'session',
        createTableIfMissing: true,
      }),
      name: 'meeting.sid',
      secret: process.env.SESSION_SECRET ?? 'local-training-session-secret',
      resave: false,
      saveUninitialized: false,
      cookie: {
        httpOnly: true,
        sameSite: 'lax',
        secure: false,
      },
    }),
  );

  app.get('/api/health', (_req, res) => {
    res.status(200).json({ ok: true });
  });

  app.use('/api/auth', authRoutes);
  app.use('/api/rooms', roomsRoutes);
  app.use('/api/bookings', bookingsRoutes);
  app.use('/api/maintenance', maintenanceRoutes);
  app.use('/api/overview', overviewRoutes);

  return app;
}

const app = createApp();
export default app;
