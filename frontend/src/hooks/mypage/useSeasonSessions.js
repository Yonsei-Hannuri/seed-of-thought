import { useState } from 'react';
import useOnMountAsync from '../common/useOnMountAsync';
import client from '../../api/client';

const useSeasonSessions = () => {
  const [seasonSessions, setSeasonSessions] = useState([]);
  useOnMountAsync(async () => {
    const seasonInfo = await client({
      method: 'GET',
      url: process.env.REACT_APP_API_URL + 'season/',
      params: { current: true },
    });
    if (seasonInfo.data.length > 0) {
      setSeasonSessions(seasonInfo.data[0].session);
    }
  });
  return { seasonSessions };
};
export default useSeasonSessions;
