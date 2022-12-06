import { useState } from 'react';
import { GET_SESSION } from '../../api/session';
import useOnMount from '../common/useOnMount';

const useSession = (sessionId) => {
  const [session, setSession] = useState(null);
  const [detgoris, setDetgoris] = useState(null);
  useOnMount(() => {
    (async () => {
      const res = await GET_SESSION(sessionId);
      if (res.status === 200) {
        const detgoris = res.data.detgori;
        delete res.data.detgori;
        setSession(res.data);
        setDetgoris(detgoris);
      }
    })();
  });

  return [session, detgoris];
};

export default useSession;
