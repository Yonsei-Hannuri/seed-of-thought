import { useState } from 'react';
import useOnMountAsync from '../common/useOnMountAsync';
import client from '../../api/client';

const useUserWords = () => {
  const [userWords, setUserWords] = useState();

  const requestUserWords = async () => {
    const userWords = await client({
      method: 'GET',
      url: `${process.env.REACT_APP_API_URL}wordList/mypage/0`,
    });
    setUserWords(userWords.data.wordList);
  };

  useOnMountAsync(requestUserWords);

  return { userWords };
};
export default useUserWords;
