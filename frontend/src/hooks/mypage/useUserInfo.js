import { useState } from 'react';
import useOnMountAsync from '../common/useOnMountAsync';
import client from '../../api/client';

const useUserInfo = () => {
  const [userInfo, setUserInfo] = useState();

  const requestUserInfo = async (seasonId) => {
    const userInfo = await client({
      method: 'GET',
      url: process.env.REACT_APP_API_URL + 'mypageInfo',
      params: {
        seasonId: seasonId,
      },
    });
    setUserInfo(userInfo.data);
  };

  const deleteRequest = (e) => {
    const reply = window.confirm(
      '댓거리 삭제 시, 복구할 수 없습니다. 삭제하시겠습니까?',
    );
    if (reply) {
      client({
        method: 'DELETE',
        url:
          process.env.REACT_APP_API_URL +
          'detgori/' +
          e.currentTarget.getAttribute('val') +
          '/',
      }).then(() => {
        requestUserInfo();
        alert('댓거리가 삭제되었습니다.');
      });
    }
  };

  useOnMountAsync(requestUserInfo);

  return { userInfo, requestUserInfo, deleteRequest };
};
export default useUserInfo;
