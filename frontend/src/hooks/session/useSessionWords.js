import { useState } from 'react';
import useOnMountAsync from '../common/useOnMountAsync';
import { GET_SESSION_WORDS } from '../../api/words';

const useSessionWords = (sessionId) => {
  const [sessionWordList, setSessionWordList] = useState([]);
  useOnMountAsync(async () => {
    setSessionWordList(await GET_SESSION_WORDS(sessionId));
  });
  return {
    sessionWordList,
  };
};

export default useSessionWords;
