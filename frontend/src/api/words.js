import client from './client';

export const GET_SESSION_WORDS = async (sessionId) => {
  const res = await client.get(`wordList/session/${sessionId}`);
  return res.data.wordList;
};
