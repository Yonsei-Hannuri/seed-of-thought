import { useEffect } from 'react';

const useOnMount = (effect) => {
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(effect, []);
};

export default useOnMount;
