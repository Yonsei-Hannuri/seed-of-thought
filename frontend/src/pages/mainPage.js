import SessionBanner from '../components/main/sessionBanner';
import FolderUI from '../components/main/folderUI/folderUI';
import { useHistory } from 'react-router';
import useCurrentSeasonSessions from '../hooks/main/useCurrentSeasonSessions';

function MainPage() {
  const sessions = useCurrentSeasonSessions();
  const history = useHistory();
  return (
    <div>
      <SessionBanner recentSession={sessions[sessions.length - 1]}>
        <button
          type="button"
          className="btn btn-light border btn-lg px-4 gap-3"
          onClick={() => {
            history.push({
              pathname:
                '/session/?sessionID=' + sessions[sessions.length - 1].id,
            });
          }}
        >
          세션 입장하기
        </button>
      </SessionBanner>
      <FolderUI seasonSessionInfos={sessions} />
    </div>
  );
}

export default MainPage;
