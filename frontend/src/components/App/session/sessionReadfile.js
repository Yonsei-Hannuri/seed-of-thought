import React, { Component } from 'react';
import address from '../../../config/address.json';
import { Page, Document } from 'react-pdf';
import { pdfjs } from 'react-pdf';
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

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
    load_left_pdf: false,
  };

  handleClick = (e) => {
    let url = e.target.value;
    fetch(url, {
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

  componentDidUpdate(prevProps, prevState) {
    if (this.state.load_left_pdf) {
      const pdf_pages = [];
      fetch(
        address.back + 'uploads/session/' + this.state.info.googleId + '.pdf',
        {
          responseType: 'blob',
        },
      )
        .then((response) => response.blob())
        .then((blob) => {
          for (var i = 2; i <= this.state.numPages; i++) {
            pdf_pages.push(
              <div className="carousel-item" key={this.state.info.googleId + i}>
                <Document
                  file={blob}
                  options={{
                    cMapUrl: `//cdn.jsdelivr.net/npm/pdfjs-dist@${pdfjs.version}/cmaps/`,
                    cMapPacked: true,
                  }}
                >
                  <Page pageNumber={i} scale={1.88} />
                </Document>
              </div>,
            );
          }
          this.setState({ pdf_pages: pdf_pages, load_left_pdf: false });
        });
    }
  }

  onDocumentLoadSuccess = ({ numPages }) => {
    this.setState({ numPages: numPages, load_left_pdf: true });
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
          <div id="pdf">
            <div
              id="pdfSessionControl"
              className="carousel slide"
              data-bs-touch="false"
              data-bs-interval="false"
            >
              <div className="carousel-inner">
                <div className="carousel-item active">
                  <Document
                    file={
                      address.back +
                      'uploads/session/' +
                      this.state.info.googleId +
                      '.pdf'
                    }
                    onLoadSuccess={this.onDocumentLoadSuccess}
                    options={{
                      cMapUrl: `//cdn.jsdelivr.net/npm/pdfjs-dist@${pdfjs.version}/cmaps/`,
                      cMapPacked: true,
                    }}
                  >
                    <Page pageNumber={1} scale={1.88} />
                  </Document>
                </div>
                {this.state.pdf_pages}
              </div>
              <button
                className="carousel-control-prev"
                type="button"
                data-bs-target="#pdfSessionControl"
                data-bs-slide="prev"
              >
                <span
                  className="carousel-control-prev-icon"
                  aria-hidden="true"
                ></span>
              </button>
              <button
                className="carousel-control-next"
                type="button"
                data-bs-target="#pdfSessionControl"
                data-bs-slide="next"
              >
                <span
                  className="carousel-control-next-icon"
                  aria-hidden="true"
                ></span>
              </button>
            </div>
          </div>
        </div>
      );
    }
    return (
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
    );
  }
}

export default SessionReadfile;
