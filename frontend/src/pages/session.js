import React, { Component } from 'react';
import { Bar } from 'react-chartjs-2';
import SessionReadfile from '../components/App/session/sessionReadfile';
import errorReport from '../modules/errorReport';
import address from '../config/address.json';
import axios from 'axios';
import { Page, Document } from 'react-pdf';
import { pdfjs } from 'react-pdf';
import NameCard from '../components/App/session/nameCard';
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

class Session extends Component {
  state = {
    info: null, //{}
    userId: null,
    chartData: null,
    currentDetgoriId: null,
    numPages: null,
    load_left_pdf: false,
    pdf_pages: [],
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
            if (data.length > 0) {
              const words = JSON.parse(data[0]);
              for (let i = 1; i < data.length; i++) {
                let words_ = JSON.parse(data[i]);
                for (let key in words_) {
                  if (Object.keys(words).includes(key)) {
                    words[key] += words_[key];
                  } else {
                    words[key] = words_[key];
                  }
                }
              }
              // make a rank
              let wordArray = [];
              for (let key in words) {
                let count = words[key];
                wordArray.push([key, count]);
              }
              wordArray.sort(function (a, b) {
                return -(a[1] - b[1]);
              });

              // chart config
              let chartData = {
                labels: wordArray.slice(0, 5).map((item) => item[0]), //많이 언급된 단어 라벨
                datasets: [
                  {
                    label: '', //이건 왜 있는 걸까?
                    data: wordArray.slice(0, 5).map((item) => item[1]), //언급 횟수
                    backgroundColor: [
                      'rgba(255, 99, 132, 0.2)',
                      'rgba(54, 162, 235, 0.2)',
                      'rgba(255, 206, 86, 0.2)',
                      'rgba(75, 192, 192, 0.2)',
                      'rgba(153, 102, 255, 0.2)',
                      'rgba(255, 159, 64, 0.2)',
                    ],
                    borderColor: [
                      'rgba(255, 99, 132, 1)',
                      'rgba(54, 162, 235, 1)',
                      'rgba(255, 206, 86, 1)',
                      'rgba(75, 192, 192, 1)',
                      'rgba(153, 102, 255, 1)',
                      'rgba(255, 159, 64, 1)',
                    ],
                    borderWidth: 1,
                  },
                ],
              };
              const options = {
                indexAxis: 'y',
                // Elements options apply to all of the options unless overridden in a dataset
                // In this case, we are setting the border of each horizontal bar to be 2px wide
                elements: {
                  bar: {
                    borderWidth: 2,
                  },
                },
                responsive: true,
                plugins: {
                  legend: {
                    position: 'right',
                  },
                  title: {
                    display: true,
                    text: '단어 언급 횟수',
                  },
                },
              };
              const chartDiv = (
                <div className="mt-3 py-3" id="statics">
                  <span className="fw-bolder fs-4 m-0">통계</span>
                  <div className="maxWidth m-auto">
                    <Bar data={chartData} options={options} />
                  </div>
                </div>
              );
              this.setState({ chartDiv: chartDiv, info: sessionData });
            }
          })
          .catch((e) => errorReport(e, 'front-session'));
      })
      .catch((e) => errorReport(e, 'front-session'));
  }

  //
  componentDidUpdate(prevProps, prevState) {
    if (this.state.load_left_pdf) {
      const pdf_pages = [];
      fetch(
        address.back +
          'uploads/detgori/' +
          this.state.currentDetgoriId +
          '.pdf',
        {
          //headers: {
          //  'Content-Type': 'application/pdf'
          //},
          responseType: 'blob',
        },
      )
        .then((response) => response.blob())
        .then((blob) => {
          for (var i = 2; i <= this.state.numPages; i++) {
            pdf_pages.push(
              <div className="carousel-item" key={i}>
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

  onNameClick = (e) => {
    document.body.scrollTop = document.documentElement.scrollTop = 0;
    setTimeout(() => {
      this.setState({
        currentDetgoriId: e.target.value,
        pdf_pages: [],
        loading: true,
      });
      document.getElementById('firstPage').classList.add('active');
    }, 500);
    setTimeout(() => {
      this.setState({ loading: false });
    }, 1500);
  };

  onClickCloseDetgori = () => {
    document.body.scrollTop = document.documentElement.scrollTop = 0;
    setTimeout(() => {
      this.setState({ currentDetgoriId: null });
    }, 500);
  };

  render() {
    if (this.state.info != null) {
      const name_list = this.state.info.detgori.map((detgoriUrl) => (
        <NameCard
          onClick={this.onNameClick}
          detgoriUrl={detgoriUrl}
          key={detgoriUrl}
        />
      ));

      return (
        <div>
          <h2>{this.state.info.title}</h2>
          <SessionReadfile
            urls={this.state.info.readfile}
            googleFolderId={this.state.info.googleFolderId}
          />
          <div className="row">
            <span className="fw-bolder fs-4 py-1"> 댓거리</span>
            <div
              id="pdfLoading"
              className={this.state.loading ? 'blankBox250 ' : 'blank'}
            >
              <div className="d-flex justify-content-center">
                <div className="spinner-border text-primary m-5" role="status">
                  <span className="sr-only"></span>
                </div>
              </div>
            </div>
            <div
              id="pdf"
              className={
                this.state.loading || this.state.currentDetgoriId === null
                  ? 'blank'
                  : ''
              }
            >
              <div
                id={`pdfDetgoriControl`}
                className="carousel slide"
                data-bs-touch="false"
                data-bs-interval="false"
              >
                <div className="carousel-inner">
                  <div id="firstPage" className="carousel-item active">
                    {this.state.currentDetgoriId ? (
                      <Document
                        file={
                          address.back +
                          'uploads/detgori/' +
                          this.state.currentDetgoriId +
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
                    ) : (
                      ''
                    )}
                  </div>
                  {this.state.pdf_pages}
                </div>
                <button
                  className="carousel-control-prev"
                  type="button"
                  data-bs-target={`#pdfDetgoriControl`}
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
                  data-bs-target={`#pdfDetgoriControl`}
                  data-bs-slide="next"
                >
                  <span
                    className="carousel-control-next-icon"
                    aria-hidden="true"
                  ></span>
                </button>
              </div>
            </div>
            <div>
              <ul className="d-flex p-0 clear-fix overflow-auto">
                {name_list}
                {name_list.length === 0 ? 
                '' :
                <button
                  className="btn m-1 btn-primary border"
                  onClick={this.onClickCloseDetgori}
                >
                  닫기
                </button>}
              </ul>
            </div>
          </div>
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
