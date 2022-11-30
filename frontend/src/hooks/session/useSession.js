import { useEffect, useState } from 'react';
import { GET_SESSION } from '../../api/session';

const useSession = (sessionId) => {
  const [session, setSession] = useState(null);
  useEffect(() => {
    (async () => {
      const res = await GET_SESSION(sessionId);
      if (res.status === 200) {
        setSession(res.data);
      }
    })();
  }, []);

  return session;
};

export default useSession;
