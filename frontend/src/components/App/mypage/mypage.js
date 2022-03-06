import React, { Component } from 'react';
import DetgoriUpload from './detgoriUpload/detgoriUpload';
import ProfileColor from './profileColor';
import WordCloud from './wordcloud';
import axios from 'axios';
import address from '../../../config/address';
import errorReport from '../../../modules/errorReport';

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
  };

  componentDidMount() {
    this.getUserInfo();
  }

  getUserInfo = () => {
    axios({
      method: 'GET',
      url: address.back + 'mypageInfo',
      withCredentials: true,
    })
      .then((res) => res.data)
      .then((data) => {
        this.setState({
          userInfo: data,
          seasonDetgoris: data.seasonDetgoris,
          loaded: true,
        });
      })
      .catch((e) => {
        this.setState({ ajaxError: true });
        errorReport(e, 'Mypage_getUserInfo');
      });
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
    const reply = window.confirm("댓거리 삭제 시, 복구할 수 없습니다. 삭제하시겠습니까?");
    const csrfToken_ = document.cookie;
    const csrfToken = csrfToken_.split('=')[1];
    const csrfHeader = {
       'X-CSRFToken':  csrfToken
    };
    if (reply){
      axios({
        method: 'DELETE',
        url: address.back + 'detgori/'+ e.currentTarget.getAttribute('val')+'/',
        withCredentials: true,
        headers: csrfHeader,
      })
        .then(() => {
          this.getUserInfo();
          alert("댓거리가 삭제되었습니다.");
        })
        
    }
  }

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
      const detgoriList = this.state.seasonDetgoris.slice(1,).map((detgori, idx) => (
        <div className='d-flex' key={detgori.detgoriId}>
          <li className="list-group-item align-bottom w-90">
              <a
                rel="noreferrer"
                href={`https://drive.google.com/file/d/${detgori.googleId}/view`}
                target="_blank"
              >
                {detgori.sessionTitle}: {detgori.detgoriTitle}
              </a>
          </li>
          <li className="list-group-item p-0 pt-2 w-10 border text-center">
            <span val={detgori.detgoriId} onClick={this.deleteRequest} className="material-icons-outlined align-middle">delete_forever</span>
          </li>
        </div>
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
              {this.state.userInfo.seasons.length === 0 ?
              '' :
              <select
                className="d-inline form-select small-dropdown"
                onChange={this.getSeasonDetgori}
                name="학기"
              >
                {seasonOptions}
              </select>
              }
            </div>
            <div className="fw-bolder fs-4 mt-1">
              &nbsp;&nbsp;{this.state.seasonDetgoris[0]}
            </div>
            <div className="">{detgoriList}</div>
          </ul>
          <div>{this.state.userInfo.detgori}</div>
          <div className="mt-3">
            <DetgoriUpload onUpload={this.getUserInfo} />
          </div>
          <div>
            <WordCloud />
          </div>
        </div>
      );
    }
    return '';
  }
}

export default Mypage;
