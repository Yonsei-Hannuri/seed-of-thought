import React, { Component } from 'react';
import axios from 'axios';
import Page from '../components/freeNote/page';
import errorReport from '../modules/errorReport';
import postRequest from '../api/postRequest';
import { Link } from 'react-router-dom';

class FreeNote extends Component {
  static defaultProps = {
    pageSelect: '',
  };

  state = {
    notes: [{}],
    page: 1,
    ajaxError: false,
  };

  componentDidMount() {
    axios({
      method: 'GET',
      url: process.env.REACT_APP_API_DOMAIN + 'freeNote/',
      params: { recentNotePage: true },
      withCredentials: true,
    })
      .then((res) => res.data)
      .then((data) => {
        if (data.length !== 0)
          this.setState({ page: data[0].page, notes: data });
      })
      .catch((e) => {
        this.setState({ ajaxError: true });
        errorReport(e, 'FreeNote_componentDidMount');
      });
  }

  getInfoAndPageFlip = (flip) => {
    axios({
      method: 'GET',
      url: process.env.REACT_APP_API_DOMAIN + 'freeNote/',
      params: { notePage: this.state.page + flip },
      withCredentials: true,
    })
      .then((res) => res.data)
      .then((data) => {
        this.setState({ page: this.state.page + flip, notes: data });
      })
      .catch((e) => {
        this.setState({ ajaxError: 1 });
        errorReport(e, 'FreeNote_getInfoAndPageFlip');
      });
  };

  handleUpload = async (e) => {
    const res = await postRequest(e, 'freeNote/', () =>
      this.getInfoAndPageFlip(0),
    );
    if (res === false) this.setState({ ajaxError: 2 });
  };

  handleNextPage = () => {
    if (this.state.page + 1 < 101) {
      this.getInfoAndPageFlip(1);
    }
  };
  handlePreviousPage = () => {
    if (this.state.page - 1 > 0) {
      this.getInfoAndPageFlip(-1);
    }
  };

  render() {
    return (
      <div>
        <button
          className="btn col-3 border mx-1 btn-light"
          onClick={this.handlePreviousPage}
        >
          {'<'}
        </button>
        <button
          className="btn col-3 border mx-1 btn-light"
          onClick={this.handleNextPage}
        >
          {'>'}
        </button>
        <span className="col-3 mx-1">페이지 {this.state.page}</span>
        {this.state.ajaxError === false ? (
          ''
        ) : this.state.ajaxError === 1 ? (
          <span className="text-danger">
            페이지 불러오는 중 오류가 발생했습니다.
          </span>
        ) : this.state.ajaxError === 2 ? (
          <span className="text-danger">
            페이지 불러오는 중 오류가 발생했습니다.
          </span>
        ) : (
          ''
        )}
        <Link to="/metaspace" className=" float-end mx-3">
          <span
            style={{ color: 'tomato', fontSize: 'x-large', fontWeight: 'bold' }}
          >
            X
          </span>
        </Link>
        <Page
          info={this.state.notes}
          onUpload={this.handleUpload}
          page={this.state.page}
        />
      </div>
    );
  }
}

export default FreeNote;
