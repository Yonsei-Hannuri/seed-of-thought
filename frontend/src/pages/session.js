import SessionReadfile from '../components/session/sessionReadfile';
import address from '../config/address.json';
import PDFViewer from '../components/session/PDFViewer';
import WordCloud from '../components/wordCloud/WordCloud';
import useSession from '../hooks/session/useSession';
import useOnMount from '../hooks/common/useOnMount';
import DurationLogger from '../modules/DurationLogger';
import { POST_DETGORI_READ_LOG } from '../api/log';
import ShowSelection from '../components/ShowSelection';
import ColorButton from '../components/session/ColorButton';
import getQueryParams from '../modules/getQueryParams';
import LocalstorageObject from '../modules/LocalstorageObject';

const durationThreshold = 0;
const durationLogger = new DurationLogger((id, duration) => {
  POST_DETGORI_READ_LOG(id, duration);
}, durationThreshold);

function Session() {
  const sessionId = getQueryParams().sessionID;
  const [session, detgoris] = useSession(sessionId);
  const readRecord = new LocalstorageObject(`session-${sessionId}-read-record`);
  useOnMount(() => {
    const unloadhandler = () => durationLogger.close();
    window.addEventListener('beforeunload', unloadhandler);
    return () => {
      window.removeEventListener('beforeunload', unloadhandler);
    };
  });

  if (session === null) return '';
  return (
    <div className="container pt-3">
      <h2>{session.title}</h2>
      <SessionReadfile
        urls={session.readfile}
        googleFolderId={session.googleFolderId}
      />
      <hr />
      {detgoris && (
        <ShowSelection
          title={'댓거리'}
          panel={(detgoriId) => (
            <PDFViewer
              key={detgoriId}
              src={`${address.back}uploads/detgori/${detgoriId}.pdf`}
            />
          )}
          options={(setDetgori) =>
            detgoris.map((detgori) => (
              <ColorButton
                key={detgori.id}
                color={detgori.authorColor}
                text={detgori.authorName}
                onClick={() => {
                  setDetgori(detgori.googleId);
                  durationLogger.changeTarget(detgori.id);
                  readRecord.setValue(detgori.id, true);
                }}
                clicked={readRecord.getValue(detgori.id)}
              />
            ))
          }
        />
      )}
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
