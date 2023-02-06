import React, { Component } from 'react';
import getCookieValue from '../../modules/getCookieValue';

class ProfileColor extends Component {
  static defaultProps = {
    userInfo: {},
    onChange: null,
  };

  state = {
    update: false,
    ajaxError: false,
  };

  handleClick = () => {
    this.setState({ update: this.state.update === true ? false : true });
  };

  handleSubmit = (e) => {
    e.preventDefault();
    let formElement = e.target;
    let data = new FormData(formElement);
    let request_url = process.env.REACT_APP_API_URL + 'profileColor/';
    const xhr = new XMLHttpRequest();
    xhr.open('POST', request_url);
    xhr.withCredentials = true;
    xhr.setRequestHeader(
      'X-CSRFToken',
      getCookieValue(document.cookie, 'csrftoken'),
    );
    xhr.onreadystatechange = () => {
      if (xhr.readyState === 4 && xhr.status === 200) {
        this.setState({ update: false });
        this.props.onChange();
      }
      if (xhr.readyState === 4 && xhr.status === 400) {
        this.setState({ ajaxError: true });
      }
    };
    xhr.send(data);
  };

  render() {
    if (this.state.update) {
      return (
        <div>
          <form className="text-center" onSubmit={this.handleSubmit}>
            <input
              type="color"
              className="form-control form-control-color"
              id="exampleColorInput"
              defaultValue={this.props.userInfo.color}
              name="color"
              title="Choose your color"
            />
            <input
              type="hidden"
              name="authorId"
              value={this.props.userInfo.id}
            />
            {this.state.ajaxError ? (
              <span className="text-danger">
                프로필 색상 변경 중 오류가 발생했습니다.
              </span>
            ) : (
              ''
            )}
            <button className="btn btn-light border my-1">수정하기</button>
          </form>
          <button onClick={this.handleClick} className="btn btn-light border">
            수정취소
          </button>
        </div>
      );
    }
    return (
      <div className="text-center p-2">
        <span
          onClick={this.handleClick}
          className="dot border cursor2Pointer"
          style={{ backgroundColor: this.props.userInfo.color }}
        ></span>
      </div>
    );
  }
}

export default ProfileColor;
