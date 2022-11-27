import React, { Component } from 'react';
import DetgoriUpload from '../components/mypage/detgoriUpload/detgoriUpload';
import ProfileColor from '../components/mypage/profileColor';
import Detgori from '../components/mypage/detgori';
import axios from 'axios';
import address from '../config/address';
import errorReport from '../modules/errorReport';
import getCookieValue from '../modules/getCookieValue';
import WordChart from '../components/wordChart/WordChart';

class Mypage extends Component {
  static defaultProps = {
    active: true,
  };

  state = {
    userInfo: {},
    seasonDetgoris: [],
    userSeasons: [],
    loaded: false,
    ajaxError: false,
    seasonInfo: { session: [] },
    showWordCloud: false,
    userWords: null,
  };

  componentDidMount() {
    this.getMypageInfo();
  }

  getMypageInfo = async () => {
    try {
      const [myPageData, seasonData, userWords] = await Promise.all([
        axios({
          method: 'GET',
          url: address.back + 'mypageInfo',
          withCredentials: true,
        }),
        axios({
          method: 'GET',
          url: address.back + 'season/',
          params: { current: true },
          withCredentials: true,
        }),
        axios({
          method: 'GET',
          url: `${address.back}wordList/mypage/0`,
          withCredentials: true,
        }),
      ]);

      this.setState({
        userInfo: myPageData.data,
        seasonDetgoris: myPageData.data.seasonDetgoris,
        seasonInfo:
          seasonData.data.length > 0
            ? seasonData.data[0]
            : this.state.seasonInfo,
        loaded: true,
        userWords: userWords.data.wordList,
      });
    } catch (e) {
      this.setState({ ajaxError: true });
      errorReport(e, 'mypage');
    }
  };

  getSeasonDetgori = (e) => {
    axios({
      method: 'GET',
      url: address.back + 'mypageInfo',
      withCredentials: true,
      params: {
        seasonId: e.target.value,
      },
    })
      .then((res) => res.data)
      .then((data) => {
        this.setState({ seasonDetgoris: data.seasonDetgoris });
      });
  };

  deleteRequest = (e) => {
    const reply = window.confirm(
      '댓거리 삭제 시, 복구할 수 없습니다. 삭제하시겠습니까?',
    );
    const csrfToken = getCookieValue(document.cookie, 'csrftoken');
    const Header = {
      'X-CSRFToken': csrfToken,
    };
    if (reply) {
      axios({
        method: 'DELETE',
        url:
          address.back + 'detgori/' + e.currentTarget.getAttribute('val') + '/',
        withCredentials: true,
        headers: Header,
      }).then(() => {
        this.getMypageInfo();
        alert('댓거리가 삭제되었습니다.');
      });
    }
  };

  render() {
    if (this.state.ajaxError) {
      return <div>Error!</div>;
    }
    if (this.state.loaded) {
      const seasonOptions = this.state.userInfo.seasons.map((season, idx) => (
        <option value={season.id} key={season.id}>
          {season.year} - {season.semester}
        </option>
      ));
      const detgoriList = this.state.seasonDetgoris
        .slice(1)
        .map((detgori, idx) => (
          <Detgori
            key={detgori.detgoriId}
            detgori={detgori}
            deleteRequest={this.deleteRequest}
          />
        ));
      return (
        <div className={this.props.active === true ? '' : 'blank'}>
          <div className="d-flex m-3" id="profile_box">
            <div className="text-center">
              <ProfileColor
                userInfo={this.state.userInfo}
                onChange={this.getUserInfo}
              />
            </div>
            <div className="m-3">
              <h3>&nbsp;&nbsp;&nbsp; {this.state.userInfo.name} 학회원님</h3>
              <h5>
                &nbsp;&nbsp;&nbsp;&nbsp; {this.state.userInfo.generation}기
              </h5>
              {this.state.userInfo.is_staff ? (
                <a href={`${address.back}admin`}>
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
              {this.state.userInfo.seasons.length === 0 ? (
                ''
              ) : (
                <select
                  className="d-inline form-select small-dropdown"
                  onChange={this.getSeasonDetgori}
                  name="학기"
                >
                  {seasonOptions}
                </select>
              )}
            </div>
            <div className="fw-bolder fs-4 mt-1">
              &nbsp;&nbsp;{this.state.seasonDetgoris[0]}
            </div>
            <div className="">{detgoriList}</div>
          </ul>
          <div>{this.state.userInfo.detgori}</div>
          <div className="mt-3">
            <DetgoriUpload
              seasonInfo={this.state.seasonInfo}
              onUpload={this.getMypageInfo}
            />
          </div>
          <div className="row m-0">
            {this.state.userWords !== null && (
              <WordChart data={this.state.userWords} />
            )}
            {/* <div className="col-sm-9"></div>
            <WordCloudButton
              className="col-sm-3"
              onClick={() => {
                this.setState({ showWordCloud: !this.state.showWordCloud });
              }}
            />
            {this.state.showWordCloud && (
              <WordCloud src={`${address.back}wordList/mypage/0`} />
            )} */}
          </div>
        </div>
      );
    }
    return '';
  }
}

export default Mypage;
