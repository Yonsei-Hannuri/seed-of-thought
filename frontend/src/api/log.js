import client from './client';

export const POST_DETGORI_READ_LOG = (detgori, duration) =>
  client.post('detgoriReadTime/', { detgori, duration });
