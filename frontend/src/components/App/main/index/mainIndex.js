import React, { Component } from 'react';
import NotificationBox from './notification';
import SessionBanner from './sessionBanner';

class Index extends Component {
  static defaultProps = {
    notifications: {},
    recentSession: {},
  };

  render() {
    return (
      <div>
        <NotificationBox notifications={this.props.notifications}/>
        <SessionBanner recentSession={this.props.recentSession}/>
      </div>
    );
  }
}

export default Index;
