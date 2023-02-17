import React from 'react';
import DetgoriUpload from '../components/mypage/detgoriUpload/detgoriUpload';
import ProfileColor from '../components/mypage/profileColor';
import Detgori from '../components/mypage/detgori';
import WordChart from '../components/wordChart/WordChart';
import useUserInfo from '../hooks/mypage/useUserInfo';
import useSeasonSessions from '../hooks/mypage/useSeasonSessions';
import useUserWords from '../hooks/mypage/useUserWords';

function Mypage() {
  const { userInfo, requestUserInfo, deleteRequest } = useUserInfo();
  const { seasonSessions } = useSeasonSessions();
  const { userWords } = useUserWords();
  const seasonOptions =
    userInfo &&
    userInfo.seasons.map((season, idx) => (
      <option value={season.id} key={season.id}>
        {season.year} - {season.semester}
      </option>
    ));
  const detgoriList =
    userInfo &&
    userInfo.seasonDetgoris
      .slice(1)
      .map((detgori) => (
        <Detgori
          key={detgori.detgoriId}
          detgori={detgori}
          deleteRequest={deleteRequest}
        />
      ));
  if (!(userInfo && seasonSessions && userWords)) return '';
  return (
    <div>
      <div className="d-flex m-3" id="profile_box">
        <div className="text-center">
          <ProfileColor userInfo={userInfo} onChange={requestUserInfo} />
        </div>
        <div className="m-3">
          <h3>&nbsp;&nbsp;&nbsp; {userInfo.name} 학회원님</h3>
          <h5>&nbsp;&nbsp;&nbsp;&nbsp; {userInfo.generation}기</h5>
          {userInfo.is_staff ? (
            <a href={`${process.env.REACT_APP_API_URL}admin`}>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 임원진 페이지
            </a>
          ) : (
            <span></span>
          )}
        </div>
      </div>
      <ul className="list-group">
        <div>
          <span className="d-inline fw-bolder fs-4 mt-3">
            &nbsp;&nbsp;댓거리
          </span>
          {userInfo.seasons.length === 0 ? (
            ''
          ) : (
            <select
              className="d-inline form-select small-dropdown"
              onChange={(e) => requestUserInfo(e.target.value)}
              name="학기"
            >
              {seasonOptions}
            </select>
          )}
        </div>
        <div className="fw-bolder fs-4 mt-1">
          &nbsp;&nbsp;{userInfo.seasonDetgoris[0]}
        </div>
        <div className="">{detgoriList}</div>
      </ul>
      <div>{userInfo.detgori}</div>
      <div className="mt-3">
        <DetgoriUpload session={seasonSessions} onUpload={requestUserInfo} />
      </div>
      <div className="row m-0">
        {userWords !== null && <WordChart data={userWords} />}
      </div>
    </div>
  );
}

export default Mypage;
