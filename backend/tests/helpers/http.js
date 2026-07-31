import http from 'node:http';
import { createApp } from '../../src/app.js';

/**
 * Start the Express app on an ephemeral port.
 * Returns { baseUrl, close, jar } where jar tracks Set-Cookie for session tests.
 */
export async function startTestServer() {
  const app = createApp();
  const server = http.createServer(app);
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const { port } = server.address();
  const baseUrl = `http://127.0.0.1:${port}`;
  const jar = new Map();

  async function request(method, path, { headers = {}, body } = {}) {
    const cookieHeader = [...jar.entries()]
      .map(([k, v]) => `${k}=${v}`)
      .join('; ');
    const res = await fetch(`${baseUrl}${path}`, {
      method,
      headers: {
        ...(body !== undefined ? { 'content-type': 'application/json' } : {}),
        ...(cookieHeader ? { cookie: cookieHeader } : {}),
        ...headers,
      },
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
    const rawSetCookie = res.headers.getSetCookie?.() ?? [];
    for (const line of rawSetCookie) {
      const [pair] = line.split(';');
      const eq = pair.indexOf('=');
      if (eq > 0) {
        jar.set(pair.slice(0, eq), pair.slice(eq + 1));
      }
    }
    const text = await res.text();
    let json = null;
    try {
      json = text ? JSON.parse(text) : null;
    } catch {
      json = text;
    }
    return { status: res.status, headers: res.headers, body: json, text };
  }

  return {
    baseUrl,
    jar,
    request,
    async close() {
      await new Promise((resolve, reject) => {
        server.close((err) => (err ? reject(err) : resolve()));
      });
    },
  };
}
