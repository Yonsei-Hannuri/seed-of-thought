import React, { Component } from 'react';

class NotificationBox extends Component {
  static defaultProps = {
    notifications: [],
  };
  render() {
    const notification_list = this.props.notifications.map((info, idx) => (
      <Notification index={idx + 1} info={info} key={info.id} />
    ));
    if (notification_list.length !== 0) {
      return (
        <div className="my-5">
          <div className="row p-4 align-items-center rounded-3 border shadow-lg">
            <div className="text-start">
              <h4>공지사항</h4>
            </div>
            <table className="table">
              <tbody>{notification_list}</tbody>
            </table>
          </div>
        </div>
      );
    } else {
      return '';
    }
  }
}

class Notification extends Component {
  state = {
    clicked: false,
  };

  static defaultProps = {
    index: 0,
    info: {},
  };

  handleClick = () => {
    this.setState({ clicked: this.state.clicked ? false : true });
  };
  render() {
    if (this.state.clicked === true) {
      return (
        <tr>
          <th className="col-3 text-center">{this.props.index}</th>
          <td>
            <h3>
              {this.props.info.title}
              <button
                className="float-end link-button"
                onClick={this.handleClick}
              >
                X
              </button>
            </h3>
            <p>{this.props.info.date.slice(0, 10)}</p>
            <p>{this.props.info.description}</p>
          </td>
        </tr>
      );
    }
    return (
      <tr>
        <th className="col-3 text-center">{this.props.index}</th>
        <td>
          <button
            className="col-9 text-start link-button"
            onClick={this.handleClick}
          >
            {this.props.info.title}
          </button>
        </td>
      </tr>
    );
  }
}

export default NotificationBox;
