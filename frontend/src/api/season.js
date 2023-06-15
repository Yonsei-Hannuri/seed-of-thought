import client from './client';

export const GET_CURRENT_SEASON_INFO = async () => {
  const { data } = await client.get('season/?current=True');
  return data[0];
};
