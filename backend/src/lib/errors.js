export function sendError(res, status, code, message, extras = {}) {
  return res.status(status).json({
    error: {
      code,
      message,
      details: [],
      ...extras,
    },
  });
}
