import SessionOption from '../components/mypage/detgoriUpload/sessionOption';
import Loading from '../components/design/Loading';
import useOpenOrClose from '../hooks/mypage/useOpenOrClose';
import useUploadDetgori from '../hooks/mypage/useUploadDetgori';

function DetgoriUpload({ session, onUpload }) {
  const { pending, uploadDetgori, error } = useUploadDetgori();
  const { isOpen, toggle: toggleOpen } = useOpenOrClose(false);

  if (pending) {
    return <Loading />;
  }

  if (isOpen) {
    const sessionOptions = session
      .slice()
      .reverse()
      .map((sessionInfo, idx) => (
        <SessionOption info={sessionInfo} key={idx} />
      ));
    return (
      <div className="border rounded mb-3">
        <div className="m-3 row " width="100%">
          <form
            id="detgoriForm"
            onSubmit={async (e) => {
              await uploadDetgori(e);
              onUpload();
              toggleOpen();
            }}
          >
            <select
              className="form-select form-select-md mb-3"
              name="parentSession"
            >
              {sessionOptions}
            </select>
            <p>
              <input
                className="form-control"
                name="title"
                type="text"
                placeholder="제목을 입력해주세요"
              />
            </p>
            <p>
              <input className="form-control" name="pdf" type="file" />
            </p>
            {error ? (
              <p className="text-danger">
                업로드 과정에서 오류가 생겼습니다. (PDF파일만 업로드
                가능합니다.)
              </p>
            ) : (
              ''
            )}
            <button className="btn btn-light border float-end">
              {' '}
              등록하기{' '}
            </button>
            <span
              className="btn float-end mx-2 btn-light border"
              onClick={toggleOpen}
            >
              업로드 취소
            </span>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="row m-0">
      <div className="col-sm-9"></div>
      <button
        onClick={toggleOpen}
        className="col-sm-3 btn btn-outline-secondary mb-3"
      >
        댓거리 업로드
      </button>
    </div>
  );
}

export default DetgoriUpload;
