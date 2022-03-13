import React, { Component } from 'react';
import SessionBanner from '../components/main/sessionBanner';
import NotificationBox from '../components/main/notificationBox';
import FolderUI from '../components/main/folderUI/folderUI';
import errorReport from '../modules/errorReport';
import address from '../config/address.json';
import axios from 'axios';

class MainPage extends Component {
  static defaultProps = {
    active: true,
  };

  state = {
    notifications: [],
    recentSession: { detgori: [], week: '', title: '', readfile: [] },
    ajaxError: false,
    loaded: false,
  };

  componentDidMount() {
    axios({
      method: 'GET',
      url: address.back + 'notification/',
      withCredentials: true,
    })
      .then((res) => res.data)
      .then((data) => {
        if (data.length) {
          this.setState({
            notifications: data,
          });
        } else {
          this.setState({ notifications: [] });
        }
      })
      .catch((e) => {
        this.setState({ ajaxError: true });
        errorReport(e, 'main_notification');
      });

    axios({
      method: 'GET',
      url: address.back + 'session/?current=true',
      withCredentials: true,
    })
      .then((res) => res.data)
      .then((data) => {
        if (data.length > 0) {
          this.setState({
            recentSession: data[0],
            loaded: true,
          });
        } else {
          this.setState({
            recentSession: { detgori: [], week: '', title: '', readfile: [] },
            loaded: true,
          });
        }
      })
      .catch((e) => {
        this.setState({ ajaxError: true, loaded: true });
        errorReport(e, 'main_session');
      });
  }

  render() {
    if (this.state.ajaxError) {
      return <div>Error!</div>;
    }
    if (this.state.loaded === true) {
      return (
        <div className={this.props.active === true ? '' : 'blank'}>
          <NotificationBox notifications={this.state.notifications}/>
          <SessionBanner recentSession={this.state.recentSession}/>
          <FolderUI/>
        </div>
      );
    }
    return '';
  }
}

export default MainPage;
