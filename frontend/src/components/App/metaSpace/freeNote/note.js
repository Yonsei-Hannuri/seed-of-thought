import React, {Component} from 'react';
import errorReport from '../../../../modules/errorReport';
import address from '../../../../config/address.json';
import getCookieValue from '../../../../modules/getCookieValue';

export default class Note extends Component {
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
      const csrfToken = getCookieValue(document.cookie, 'csrftoken');
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
        const fontSelected = 'font-'+(randomNumber % 5 + 1)
        return (
          <div
            className={
              'textDiv w-100 h-100 p-3 rounded-3 ' + fontSelected
            }
            style={{ backgroundColor: '#f5f5f5' }}
          >
            {this.props.info.text}
          </div>
        );
      }
    }
  }
  