import { useState } from 'react';
import SessionReadfile from '../components/session/sessionReadfile';
import address from '../config/address.json';
import NameCard from '../components/session/nameCard';
import PDFViewer from '../components/session/PDFViewer';
import WordCloud from '../components/wordCloud/WordCloud';
import useSession from '../hooks/session/useSession';
import useOnMount from '../hooks/common/useOnMount';
import DurationLogger from '../modules/DurationLogger';
import { POST_DETGORI_READ_LOG } from '../api/log';

const durationThreshold = 0;
const durationLogger = new DurationLogger((id, duration) => {
  POST_DETGORI_READ_LOG(id, duration);
}, durationThreshold);

function Session() {
  const urlSearchParams = new URLSearchParams(window.location.search);
  const params = Object.fromEntries(urlSearchParams.entries());
  const session = useSession(params.sessionID);
  const [currentDetgoriId, setCurrentDetgoriId] = useState(null);

  const onNameClick = (googleId, detgoriId) => {
    durationLogger.changeTarget(detgoriId);
    document.body.scrollTop = document.documentElement.scrollTop = 0;
    setTimeout(() => {
      setCurrentDetgoriId(googleId);
    }, 500);
  };

  useOnMount(() => {
    const unloadhandler = () => durationLogger.close();
    window.addEventListener('beforeunload', unloadhandler);
    return () => {
      window.removeEventListener('beforeunload', unloadhandler);
    };
  });

  // const onClickCloseDetgori = () => {
  //   document.body.scrollTop = document.documentElement.scrollTop = 0;
  //   durationLogger.close();
  //   setTimeout(() => {
  //     setCurrentDetgoriId(null);
  //   }, 500);
  // };

  if (session === null) return '';

  const name_list = session.detgori.map((detgoriInfo) => (
    <NameCard
      clickhandler={onNameClick}
      info={detgoriInfo}
      key={detgoriInfo.id}
    />
  ));

  return (
    <div className="container pt-3">
      <h2>{session.title}</h2>
      <SessionReadfile
        urls={session.readfile}
        googleFolderId={session.googleFolderId}
      />
      <hr />
      <div className="row">
        <span className="fw-bolder fs-4 py-1"> 댓거리</span>
        {currentDetgoriId !== null && (
          <PDFViewer
            key={currentDetgoriId}
            src={`${address.back}uploads/detgori/${currentDetgoriId}.pdf`}
          />
        )}
        <div>
          <ul className="d-flex p-0 clear-fix overflow-auto justify-content-start flex-wrap">
            {name_list}
          </ul>
        </div>
      </div>
      <hr />
      {session && (
        <WordCloud src={`${address.back}wordList/session/${session.id}`} />
      )}
      <hr />
      <div className="text-end m-3">
        <a href="/">
          <button className="btn btn-light border">나가기</button>
        </a>
      </div>
    </div>
  );
}

export default Session;
