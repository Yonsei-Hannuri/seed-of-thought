import client from './client';

export const GET_SESSION = (sessionId) =>
  client.get('session/' + sessionId + '/');

export const GET_CURRENT_SEASON_SESSIONS = async () => {
  const res = await client.get('season/?current=True');
  return res.data[0].session;
};
