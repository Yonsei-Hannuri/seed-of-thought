import React, { Component } from 'react';
import axios from 'axios';
import errorReport from '../../../modules/errorReport';
import address from '../../../config/address.json';

class Note extends Component {
  static defaultProps = {
    info: false,
    writing: false,
    onClick: null,
    position: -1,
    page: 0,
    onUpload: null,
  };

  state = {
    ajaxError: false,
  };

  handleSubmit = (e) => {
    e.preventDefault();
    let formElement = e.target;
    let data = new FormData(formElement);
    let request_url = address.back + 'freeNote/';
    const xhr = new XMLHttpRequest();
    xhr.open('POST', request_url);
    xhr.withCredentials = true;
    let csrfToken_ = document.cookie;
    let csrfToken = csrfToken_.split('=')[1];
    xhr.setRequestHeader('X-CSRFToken', csrfToken);
    xhr.onreadystatechange = () => {
      if (xhr.readyState === 4 && xhr.status === 201) {
        this.props.onUpload();
      }
      if (xhr.readyState === 4 && xhr.status >= 400) {
        this.setState({ ajaxError: true });
        errorReport(xhr.statusText, 'freeNtoe-upload');
      }
    };
    xhr.send(data);
  };

  render() {
    if (this.props.info === false) {
      if (this.props.writing) {
        return (
          <div
            style={{ backgroundColor: '#f5f5f5' }}
            className="w-100 h-100 rounded-3 "
          >
            <form className="w-100 h-100" onSubmit={this.handleSubmit}>
              <textarea
                style={{ backgroundColor: '#f5f5f5' }}
                className="w-100 h-75 rounded-3 form-control"
                name="text"
                required
              ></textarea>
              <input type="hidden" name="page" value={this.props.page}></input>
              <input
                type="hidden"
                name="position"
                value={this.props.position}
              ></input>
              {this.state.ajaxError ? (
                <span className="text-danger">
                  등록 중 오류가 발생했습니다.
                </span>
              ) : (
                ''
              )}
              <button className="btn btn-light float-end m-2">끄적이기</button>
            </form>
          </div>
        );
      } else {
        return (
          <div
            className="w-100 h-100 rounded-3 cursor2Pointer"
            style={{ backgroundColor: '#f5f5f5' }}
            onClick={() => this.props.onClick(this.props.position)}
          ></div>
        );
      }
    } else {
      let randomNumber = 0;
      let source = this.props.info.text.slice(0, 10);
      let words = source.split('');
      for (let i = 0; i < words.length; i++) {
        randomNumber += words[i].charCodeAt(0);
      }
      randomNumber += this.props.info.id;

      return (
        <div
          className={
            'textDiv w-100 h-100 p-3 rounded-3 font-' +
            String((randomNumber % 5) + 1)
          }
          style={{ backgroundColor: '#f5f5f5' }}
        >
          {this.props.info.text}
        </div>
      );
    }
  }
}

class Page extends Component {
  static defaultProps = {
    info: [],
    page: 1,
    onUpload: null,
  };

  state = {
    info: [false, false, false, false, false, false, false, false],
    writing: [false, false, false, false, false, false, false, false],
    writingPosition: -1,
  };

  componentDidMount() {
    let newInfoState = [false, false, false, false, false, false, false, false];
    for (let i = 0; i < this.props.info.length; i++) {
      let note = this.props.info[i];
      newInfoState = newInfoState
        .slice(0, note.position)
        .concat([note])
        .concat(newInfoState.slice(note.position + 1, 8));
    }
    this.setState({ info: newInfoState });
  }

  componentDidUpdate(prevProps, prevState) {
    //when clicked for update => set state which note is selected(only one at once)
    if (prevState.writingPosition !== this.state.writingPosition) {
      let newWritingState = [
        false,
        false,
        false,
        false,
        false,
        false,
        false,
        false,
      ];
      newWritingState[this.state.writingPosition] = true;
      this.setState({
        writing: newWritingState,
      });
    }

    //when page is changed => new info state
    if (prevProps.info !== this.props.info) {
      let newInfoState = [
        false,
        false,
        false,
        false,
        false,
        false,
        false,
        false,
      ];
      for (let i = 0; i < this.props.info.length; i++) {
        let note = this.props.info[i];
        newInfoState = newInfoState
          .slice(0, note.position)
          .concat([note])
          .concat(newInfoState.slice(note.position + 1, 8));
      }
      this.setState({ info: newInfoState, writingPosition: -1 });
    }
  }

  handleClick = (position) => {
    this.setState({ writingPosition: position });
  };

  render() {
    return (
      <div>
        <div className="row">
          <div className="p-2 col-sm-6 h-rem15">
            <Note
              info={this.state.info[0]}
              onClick={this.handleClick}
              onUpload={this.props.onUpload}
              page={this.props.page}
              position={0}
              writing={this.state.writing[0]}
            />
          </div>
          <div className="p-2 col-sm-6 h-rem15">
            <Note
              info={this.state.info[1]}
              onClick={this.handleClick}
              onUpload={this.props.onUpload}
              page={this.props.page}
              position={1}
              writing={this.state.writing[1]}
            />
          </div>
        </div>
        <div className="row">
          <div className="p-2 col-sm-6 h-rem15">
            <Note
              info={this.state.info[2]}
              onClick={this.handleClick}
              onUpload={this.props.onUpload}
              page={this.props.page}
              position={2}
              writing={this.state.writing[2]}
            />
          </div>
          <div className="p-2 col-sm-6 h-rem15">
            <Note
              info={this.state.info[3]}
              onClick={this.handleClick}
              onUpload={this.props.onUpload}
              page={this.props.page}
              position={3}
              writing={this.state.writing[3]}
            />
          </div>
        </div>
        <div className="row =">
          <div className="p-2 col-sm-6 h-rem15">
            <Note
              info={this.state.info[4]}
              onClick={this.handleClick}
              onUpload={this.props.onUpload}
              page={this.props.page}
              position={4}
              writing={this.state.writing[4]}
            />
          </div>
          <div className="p-2 col-sm-6 h-rem15">
            <Note
              info={this.state.info[5]}
              onClick={this.handleClick}
              onUpload={this.props.onUpload}
              page={this.props.page}
              position={5}
              writing={this.state.writing[5]}
            />
          </div>
        </div>
        <div className="row">
          <div className="p-2 col-sm-6 h-rem15">
            <Note
              info={this.state.info[6]}
              onClick={this.handleClick}
              onUpload={this.props.onUpload}
              page={this.props.page}
              position={6}
              writing={this.state.writing[6]}
            />
          </div>
          <div className="p-2 col-sm-6 h-rem15">
            <Note
              info={this.state.info[7]}
              onClick={this.handleClick}
              onUpload={this.props.onUpload}
              page={this.props.page}
              position={7}
              writing={this.state.writing[7]}
            />
          </div>
        </div>
      </div>
    );
  }
}

class FreeNote extends Component {
  state = {
    notes: [{}],
    page: 1,
    ajaxError: false,
  };

  componentDidMount() {
    //const rand_0_99 = Math.floor(Math.random() * 100);
    //this.getInfoAndPageFlip(rand_0_99)
    axios({
      method: 'GET',
      url: address.back + 'freeNote/',
      params: { recentNotePage: true },
      withCredentials: true,
    })
      .then((res) => res.data)
      .then((data) => {
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
      url: address.back + 'freeNote/',
      params: { notePage: this.state.page + flip },
      withCredentials: true,
    })
      .then((res) => res.data)
      .then((data) => {
        this.setState({ page: this.state.page + flip, notes: data });
      })
      .catch((e) => {
        this.setState({ ajaxError: true });
        errorReport(e, 'FreeNote_getInfoAndPageFlip');
      });
  };

  handleUpload = () => {
    this.getInfoAndPageFlip(0);
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
          이전
        </button>
        <button
          className="btn col-3 border mx-1 btn-light"
          onClick={this.handleNextPage}
        >
          다음
        </button>
        <span className="col-3 mx-1">페이지 {this.state.page}</span>
        {this.state.ajaxError ? (
          <span className="text-danger">
            페이지 불러오는 중 오류가 발생했습니다.
          </span>
        ) : (
          ''
        )}
        <a href="/?section=meta">
          <button className="btn col-3 border float-end mx-1 btn-light">
            나가기
          </button>
        </a>
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
