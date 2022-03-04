import React, { Component } from 'react';
import DetgoriUpload from './detgoriUpload';
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

  render() {
    if (this.state.ajaxError) {
      return <div>Error!</div>;
    }
    if (this.state.loaded) {
      const seasonOptions = [];
      const seasons = this.state.userInfo.seasons;
      for (var i = 0; i < seasons.length; i++) {
        seasonOptions.push(
          <option value={seasons[i].id} key={seasons[i].id}>
            {seasons[i].year} - {seasons[i].semester}
          </option>,
        );
      }
      const detgoriList = [];
      const detgoris = this.state.seasonDetgoris;
      for (i = 1; i < detgoris.length; i++) {
        detgoriList.push(
          <li className="list-group-item" key={detgoris[i].googleId}>
            <a
              rel="noreferrer"
              href={`https://drive.google.com/file/d/${detgoris[i].googleId}/view`}
              target="_blank"
            >
              {detgoris[i].sessionTitle}: {detgoris[i].detgoriTitle}
            </a>
          </li>,
        );
      }
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
