import React, { Component } from 'react';
import SessionBanner from '../components/main/sessionBanner';
import FolderUI from '../components/main/folderUI/folderUI';
import errorReport from '../modules/errorReport';
import axios from 'axios';

class MainPage extends Component {
  state = {
    sessions: [],
    ajaxError: false,
    loaded: false,
  };

  componentDidMount() {
    (async () => {
      try {
        const seasonData = await axios({
          method: 'GET',
          url: process.env.REACT_APP_API_URL + 'season/?current=True',
          withCredentials: true,
        });

        this.setState({
          sessions:
            seasonData.data[0].session.length > 0
              ? seasonData.data[0].session
              : this.state.sessions,
          loaded: true,
        });
      } catch (e) {
        this.setState({ ajaxError: true });
        errorReport(e, 'mainPage');
      }
    })();
  }

  render() {
    if (this.state.ajaxError) {
      return <div>Error!</div>;
    }
    if (this.state.loaded === true) {
      return (
        <div>
          <SessionBanner
            recentSession={this.state.sessions[this.state.sessions.length - 1]}
          >
            <button
              type="button"
              className="btn btn-light border btn-lg px-4 gap-3"
              onClick={() => {
                this.props.history.push({
                  pathname:
                    '/session/?sessionID=' +
                    this.state.sessions[this.state.sessions.length - 1].id,
                });
              }}
            >
              세션 입장하기
            </button>
          </SessionBanner>
          <FolderUI seasonSessionInfos={this.state.sessions} />
        </div>
      );
    }
    return '';
  }
}

export default MainPage;
