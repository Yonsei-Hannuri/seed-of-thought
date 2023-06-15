import SessionBanner from '../components/main/sessionBanner';
import FolderUI from '../components/main/folderUI/folderUI';
import { useHistory } from 'react-router';
import useCurrentSeason from '../hooks/season/useCurrentSeason';

function MainPage() {
  const { seasonTitle, seasonSessions: sessions } = useCurrentSeason();
  const history = useHistory();
  return (
    <div>
      <div>{seasonTitle}</div>
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
