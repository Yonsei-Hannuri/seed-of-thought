import React, { Component } from 'react';
import httpsfy from '../../modules/httpsfy';
import PDFViewer from './PDFViewer';

class SessionReadfile extends Component {
  static defaultProps = {
    urls: [],
    googleFolderId: '',
  };
  state = {
    opened: false,
    info: {},
    ajaxError: false,
    numPages: null,
    pdf_pages: [],
    render_more_pdf: false,
  };

  handleClick = (e) => {
    const url = e.target.value;
    fetch(httpsfy(url, process.env.NODE_ENV), {
      credentials: 'include',
    })
      .then((res) => res.json())
      .then((data) => {
        this.setState({ opened: true, info: data });
      })
      .catch((e) => this.setState({ ajaxError: true }));
  };

  handleCloseClick = () => {
    this.setState({ opened: false });
  };

  render() {
    if (this.state.ajaxError) {
      return <div>Error!</div>;
    }
    const readfile_list = this.props.urls.map((url, idx) => (
      <button
        key={url}
        className="btn btn-outline-secondary mx-1 my-1.88"
        value={url}
        onClick={this.handleClick}
      >
        자료 {idx + 1}
      </button>
    ));
    if (this.state.opened) {
      readfile_list.push(
        <button
          key={'closeButton'}
          className="btn btn-outline-secondary mx-1 my-2 float-end"
          onClick={this.handleCloseClick}
        >
          자료 닫기
        </button>,
      );
    }
    return (
      <div>
        <div>
          {readfile_list}
          <a
            href={`https://drive.google.com/drive/folders/${this.props.googleFolderId}?usp=sharing`}
          >
            <img
              className="mx-2"
              style={{ width: '40px' }}
              src="https://fonts.gstatic.com/s/i/productlogos/drive_2020q4/v8/web-64dp/logo_drive_2020q4_color_2x_web_64dp.png"
              alt="google drive"
            />
          </a>
        </div>
        {this.state.opened && (
          <PDFViewer
            key={this.state.info.googleId}
            src={`${process.env.REACT_APP_API_URL}uploads/session/${this.state.info.googleId}.pdf`}
          />
        )}
      </div>
    );
  }
}

export default SessionReadfile;
