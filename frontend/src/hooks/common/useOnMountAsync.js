import { useEffect } from 'react';

const useOnMountAsync = (effect, detachHandler) => {
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    effect();
    return detachHandler;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
};

export default useOnMountAsync;
