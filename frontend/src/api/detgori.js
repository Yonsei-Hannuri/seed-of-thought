import client from './client';

export const UPLOAD_DETGORI = (file) =>
  client.post('detgori/', new FormData(file));
