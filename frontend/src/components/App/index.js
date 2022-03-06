import React, { Component } from 'react';
import Main from './main/main';
import Mypage from './mypage/mypage';
import MetaSpace from './metaSpace/metaSpace';
import axios from 'axios';
import errorReport from '../../modules/errorReport';
import address from '../../config/address.json';
function delay(time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

class Index extends Component {
  state = {
    main: true,
    metaSpace: false,
    mypage: false,
    userInfo: null,
  };

  componentDidMount() {
    axios({
      method: 'GET',
      url: address.back + 'user/',
      params: { userInfo: true },
      withCredentials: true,
      validateStatus: function (status) {
        if (!(status < 300 && status >= 200)) {
          delay(1000).then(() => (window.location.href = '/login'));
          return false;
        }
        return true;
      },
    })
      .then((res) => res.data[0])
      .then((data) => {
        this.setState({ userInfo: data });
      })
      .catch((e) => errorReport(e, 'App.js'));

    const urlSearchParams = new URLSearchParams(window.location.search);
    const params = Object.fromEntries(urlSearchParams.entries());
    if (params.section === 'meta') {
      this.setState({ main: false, mypage: false, metaSpace: true });
    }
  }

  handleToggle = (e) => {
    this.setState({
      main: false,
      metaSpace: false,
      mypage: false,
      [e.target.name]: true,
    });
  };

  render() {
    if (!this.state.userInfo) {
      return (
        <div className="container h-100">
          <div className="row align-items-center h-100">
            <div className="col-1 mx-auto">
              <div className="jumbotron">
                <div
                  className="spinner-border text-primary align-middle"
                  role="status"
                ></div>
              </div>
            </div>
          </div>
        </div>
      );
    }
    return (
      <div className="container">
        <div name="header">
          <div className="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
            <span className="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none justify-content-center">
              <span className="fs-4 px-4">
                <img width="30px" src="blue.ico" alt="icon" />
                한누리
              </span>
            </span>
            <ul className="nav nav-pills justify-content-center">
              <li className="nav-item">
                <button
                  name="main"
                  className={'nav-link ' + (this.state.main ? 'active' : '')}
                  onClick={this.handleToggle}
                >
                  메인
                </button>
              </li>
              <li className="nav-item">
                <button
                  name="metaSpace"
                  className={
                    'nav-link ' + (this.state.metaSpace ? 'active' : '')
                  }
                  onClick={this.handleToggle}
                >
                  메타동방
                </button>
              </li>
              <li className="nav-item">
                <button
                  name="mypage"
                  className={'nav-link ' + (this.state.mypage ? 'active' : '')}
                  onClick={this.handleToggle}
                >
                  마이페이지
                </button>
              </li>
              <li className="nav-item">
                <a href={address.back + 'logout/'} className="nav-link">
                  로그아웃
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div>
          <Main active={this.state.main} />
          <Mypage active={this.state.mypage} />
          <MetaSpace active={this.state.metaSpace} />
        </div>

        <div className="text-end p-4 border-top font-3 fs-6">
          Copyright 2021-2022<br/> 
          연세대학교 상경대 인문사회학회 한누리
          <br />
        </div>
      </div>
    );
  }
}

export default Index;
