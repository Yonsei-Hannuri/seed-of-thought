import client from './client';

export const GET_SESSION = (sessionId) =>
  client.get('session/' + sessionId + '/');
