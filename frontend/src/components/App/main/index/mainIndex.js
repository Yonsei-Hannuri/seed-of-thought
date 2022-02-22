import React, { Component } from 'react';
import NotificationBox from './notification';

class Index extends Component {
  static defaultProps = {
    notifications: {},
    recentSession: {},
  };

  render() {
    return (
      <div>
        <NotificationBox notifications={this.props.notifications} />
        <div className="px-4 py-5 my-5 text-center">
          <h3 className="display-5 fw-normal">
            {this.props.recentSession.week} 주차
          </h3>
          <h1 className="display-5 fw-bold">
            {this.props.recentSession.title}
          </h1>
          <div className="col-lg-6 mx-auto">
            <div className="d-grid gap-2 d-sm-flex justify-content-sm-center">
              <a href={'/session/?sessionID=' + this.props.recentSession.id}>
                <button
                  type="button"
                  className="btn btn-light border btn-lg px-4 gap-3"
                >
                  세션 입장하기
                </button>
              </a>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Index;
