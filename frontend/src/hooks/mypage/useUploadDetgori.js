import { useState, useRef } from 'react';
import { UPLOAD_DETGORI } from '../../api/detgori';

const useUploadDetgori = () => {
  const [pending, setPending] = useState(false);
  const [error, setError] = useState(false);
  const uploadDetgori = useRef(async (e) => {
    setPending(true);
    try {
      await UPLOAD_DETGORI(e.target);
    } catch {
      setError(true);
      setPending(false);
      throw new Error('업로드에 실패하였습니다.');
    }
    setPending(false);
  }).current;

  return {
    pending,
    uploadDetgori: uploadDetgori,
    error,
  };
};

export default useUploadDetgori;
