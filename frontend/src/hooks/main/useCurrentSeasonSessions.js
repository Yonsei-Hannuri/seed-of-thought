import { useState } from 'react';
import useOnMountAsync from '../common/useOnMountAsync';
import { GET_CURRENT_SEASON_SESSIONS } from '../../api/session';

const useCurrentSeasonSessions = () => {
  const [sessions, setSessions] = useState([]);
  useOnMountAsync(async () => {
    const sessions = await GET_CURRENT_SEASON_SESSIONS();
    setSessions(sessions);
  });

  return sessions;
};

export default useCurrentSeasonSessions;
