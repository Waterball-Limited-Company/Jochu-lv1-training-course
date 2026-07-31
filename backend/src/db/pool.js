import path from 'node:path';
import { fileURLToPath } from 'node:url';
import dotenv from 'dotenv';
import pg from 'pg';

const { Pool } = pg;

const backendRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
dotenv.config({ path: path.join(backendRoot, '.env'), quiet: true });

const isTest = process.env.NODE_ENV === 'test' || Boolean(process.env.NODE_TEST_CONTEXT);
const connectionString =
  (isTest ? process.env.TEST_DATABASE_URL : process.env.DATABASE_URL) ??
  'postgres://meeting:meeting@127.0.0.1:5432/meeting_room';

export const pool = new Pool({ connectionString, allowExitOnIdle: isTest });

export async function query(text, params) {
  return pool.query(text, params);
}
