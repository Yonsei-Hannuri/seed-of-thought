import React, { Component } from 'react';
import SessionOption from './sessionOption';
import errorReport from '../../../../modules/errorReport';
import address from '../../../../config/address.json';
import getCookieValue from '../../../../modules/getCookieValue';
import axios from 'axios';

class DetgoriUpload extends Component {
  state = {
    opened: false,
    onUpload: null,
    seasonInfo: { session: [] },
    uploading: false,
    uploadError: false,
  };

  handleClick = () => {
    this.setState({ opened: this.state.opened ? false : true });
  };

  componentDidUpdate = (prevProps, prevState) => {
    if (prevState.opened === false && this.state.opened === true) {
      axios({
        method: 'GET',
        url: address.back + 'season/',
        params: { current: true },
        withCredentials: true,
      })
        .then((res) => res.data)
        .then((data) => {
          if (data.length > 0) {
            this.setState({ seasonInfo: data[0] });
          } else {
            this.setState({ seasonInfo: { session: [] } });
          }
        })
        .catch((e) =>
          errorReport(e, 'DetgoriUpload_componentDidupdate_sessionSelect'),
        );
    }
  };

  handlePost = (e) => {
    this.setState({ uploading: true });
    e.preventDefault();
    let formElement = e.target;
    let data = new FormData(formElement);
    let request_url = address.back + 'detgori/';
    const xhr = new XMLHttpRequest();
    xhr.open('POST', request_url);
    xhr.withCredentials = true;
    const csrfToken = getCookieValue(document.cookie, 'csrftoken');
    xhr.setRequestHeader('X-CSRFToken', csrfToken);
    xhr.onreadystatechange = () => {
      if (xhr.readyState === 4 && xhr.status === 201) {
        this.setState({ opened: false, uploading: false, uploadError: false });
        this.props.onUpload();
      }
      if (xhr.readyState === 4 && xhr.status >= 400) {
        this.setState({ uploading: false, uploadError: true });
        errorReport(xhr.statusText, 'detgori-upload');
      }
    };
    xhr.send(data);
  };

  render() {
    if (this.state.uploading) {
      return (
        <div className="text-center my-5">
          <div className="spinner-grow text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <div className="spinner-grow text-secondary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <div className="spinner-grow text-success" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <div className="spinner-grow text-danger" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <div className="spinner-grow text-warning" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <div className="spinner-grow text-info" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      );
    }

    if (this.state.opened === true) {
      const sessionOptions = this.state.seasonInfo.session.slice().reverse().map(
        (sessionUrl, idx) => <SessionOption url={sessionUrl} key={idx} />,
      );
      return (
        <div className="border rounded mb-3">
          <div className="m-3 row " width="100%">
            <form id="detgoriForm" onSubmit={this.handlePost}>
              <select
                className="form-select form-select-md mb-3"
                name="parentSession"
              >
                {sessionOptions}
              </select>
              <p>
                <input
                  className="form-control"
                  name="title"
                  type="text"
                  placeholder="제목을 입력해주세요"
                />
              </p>
              <p>
                <input className="form-control" name="pdf" type="file" />
              </p>
              {this.state.uploadError ? (
                <p className="text-danger">
                  업로드 과정에서 오류가 생겼습니다. (PDF파일만 업로드
                  가능합니다.)
                </p>
              ) : (
                ''
              )}
              <button className="btn btn-light border float-end">
                {' '}
                등록하기{' '}
              </button>
              <button
                className="btn float-end mx-2 btn-light border"
                onClick={this.handleClick}
              >
                업로드 취소
              </button>
            </form>
          </div>
        </div>
      );
    }

    return (
      <div className="row m-0">
        <div className="col-sm-9"></div>
        <button
          onClick={this.handleClick}
          className="col-sm-3 btn btn-outline-secondary mb-3"
        >
          댓거리 업로드
        </button>
      </div>
    );
  }
}

export default DetgoriUpload;
