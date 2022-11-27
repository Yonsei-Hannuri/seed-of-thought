import React, { Component } from 'react';
import SessionReadfile from '../components/session/sessionReadfile';
import errorReport from '../modules/errorReport';
import address from '../config/address.json';
import axios from 'axios';
import NameCard from '../components/session/nameCard';
import WordChart from '../components/session/wordChart/wordChart';
import PDFViewer from '../components/session/PDFViewer';
class Session extends Component {
  state = {
    info: null, //{}
    userId: null,
    chartData: null,
    currentDetgoriId: null,
    loading: false,
    chartDiv: '',
  };

  componentDidMount() {
    axios({
      method: 'GET',
      url: address.back + 'user/',
      params: { userInfo: true },
      withCredentials: true,
      validateStatus: function (status) {
        // 상태 코드가 200대가 아닐 경우 //이부분 반드시 필요 없는듯
        if (!(status < 300 && status >= 200)) {
          window.location.href = address.front;
          return false;
        }
        return true;
      },
    })
      .then((res) => res.data[0])
      .then((data) => {
        this.setState({ userId: data.id });
      })
      .catch((e) => errorReport(e, 'front-session'));

    const urlSearchParams = new URLSearchParams(window.location.search);
    const params = Object.fromEntries(urlSearchParams.entries());

    //Get session word cloud data
    axios({
      method: 'GET',
      url: address.back + 'session/' + params.sessionID + '/',
      withCredentials: true,
      validateStatus: function (status) {
        // 상태 코드가 200대가 아닐 경우 //이부분 반드시 필요 없는듯
        if (!(status < 300 && status >= 200)) {
          window.location.href = address.front;
          return false;
        }
        return true;
      },
    })
      .then((res) => res.data)
      .then((sessionData) => {
        if (sessionData === undefined) {
          window.location.href = address.front;
        }
        fetch(`${address.back}wordList/session/${sessionData.id}`, {
          credentials: 'include',
        })
          .then((res) => res.json())
          .then((data_) => {
            let data = data_.wordList;
            if (data.length === 0) {
              this.setState({ info: sessionData });
            } else {
              this.setState({
                chartDiv: <WordChart data={data} />,
                info: sessionData,
              });
            }
          })
          .catch((e) => errorReport(e, 'front-session'));
      })
      .catch((e) => errorReport(e, 'front-session'));
  }

  onNameClick = (googleId) => {
    document.body.scrollTop = document.documentElement.scrollTop = 0;
    setTimeout(() => {
      this.setState({
        currentDetgoriId: googleId,
        loading: true,
      });
    }, 500);
  };

  onClickCloseDetgori = () => {
    document.body.scrollTop = document.documentElement.scrollTop = 0;
    setTimeout(() => {
      this.setState({ currentDetgoriId: null });
    }, 500);
  };

  render() {
    if (this.state.info != null) {
      const name_list = this.state.info.detgori.map((detgoriInfo) => (
        <NameCard
          clickhandler={this.onNameClick}
          info={detgoriInfo}
          key={detgoriInfo.id}
        />
      ));

      return (
        <div className="container pt-3">
          <h2>{this.state.info.title}</h2>
          <SessionReadfile
            urls={this.state.info.readfile}
            googleFolderId={this.state.info.googleFolderId}
          />
          <hr />
          <div className="row">
            <span className="fw-bolder fs-4 py-1"> 댓거리</span>
            {this.state.currentDetgoriId !== null && (
              <PDFViewer
                key={this.state.currentDetgoriId}
                src={`${address.back}uploads/detgori/${this.state.currentDetgoriId}.pdf`}
              />
            )}
            <div>
              <ul className="d-flex p-0 clear-fix overflow-auto justify-content-start flex-wrap">
                {name_list}
              </ul>
            </div>
          </div>
          <hr />
          {this.state.chartDiv}
          <hr />
          <div className="text-end m-3">
            <a href="/">
              <button className="btn btn-light border">나가기</button>
            </a>
          </div>
        </div>
      );
    }
    return '';
  }
}

export default Session;
