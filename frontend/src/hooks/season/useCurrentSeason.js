import { useState } from 'react';
import useOnMountAsync from '../common/useOnMountAsync';
import { GET_CURRENT_SEASON_INFO } from '../../api/season';

const useCurrentSeason = () => {
  const [seasonTitle, setSeasonTitle] = useState('');
  const [seasonSessions, setSeasonSessions] = useState([]);
  useOnMountAsync(async () => {
    const season = await GET_CURRENT_SEASON_INFO();
    setSeasonTitle(season.title);
    setSeasonSessions(season.session);
  });

  return { seasonTitle, seasonSessions };
};

export default useCurrentSeason;
