import address from '../config/address.json';
import client from './client';

export const GET_SESSION = (sessionId) =>
  client.get(address.back + 'session/' + sessionId + '/');
