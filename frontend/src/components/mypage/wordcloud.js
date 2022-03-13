import React, { Component } from 'react';
import ReactWordcloud from 'react-wordcloud';
import errorReport from '../../modules/errorReport';
import address from '../../config/address.json';

class WordCloud extends Component {
  state = {
    words: [{}],
    size: [100, 100],
    ajaxError: false,
  };

  handleClickCloud = () => {
    fetch(address.back + 'wordList/mypage/0', {
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

          //step3. setting for wordcloud
          let wordList = [];
          for (let key in words) {
            if (words[key] < 3) {
              continue;
            }
            let obj_ = { text: key, value: words[key] };
            wordList.push(obj_);
          }
          let width = document.getElementById('wc_box').offsetWidth;
          let height = document.getElementById('wc_box').offsetHeight;
          this.setState({ words: wordList, size: [width, height] });
        } else {
          this.setState({ words: [], size: [10, 10] });
        }
      })
      .catch((e) => {
        this.setState({ ajaxError: true });
        errorReport(e, 'wordcloud_mypage_handleClickCloud');
      });
  };

  render() {
    if (this.state.ajaxError) {
      return <div>Error!</div>;
    }
    return (
      <div className="row m-0">
        <div className="col-sm-9"></div>
        <button
          className="btn col-sm-3 btn-outline-secondary mb-1"
          onClick={this.handleClickCloud}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="currentColor"
            className="bi bi-cloud p-0"
            viewBox="0 0 16 16"
          >
            <path d="M4.406 3.342A5.53 5.53 0 0 1 8 2c2.69 0 4.923 2 5.166 4.579C14.758 6.804 16 8.137 16 9.773 16 11.569 14.502 13 12.687 13H3.781C1.708 13 0 11.366 0 9.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383zm.653.757c-.757.653-1.153 1.44-1.153 2.056v.448l-.445.049C2.064 6.805 1 7.952 1 9.318 1 10.785 2.23 12 3.781 12h8.906C13.98 12 15 10.988 15 9.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 4.825 10.328 3 8 3a4.53 4.53 0 0 0-2.941 1.1z" />
          </svg>
        </button>
        <div className="text-center" id="wc_box">
          <ReactWordcloud
            words={this.state.words}
            size={this.state.size}
            options={{ fontSizes: [8, 60] }}
          />
        </div>
      </div>
    );
  }
}

export default WordCloud;
