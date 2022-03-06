import React, { Component } from 'react';
import httpsfy from '../../../modules/httpsfy';
import axios from 'axios';

class NameCard extends Component {
    static defaultProps = {
      onClick: null,
      detgoriUrl: null,
    };
  
    state = {
      detgoriInfo: { authorName: '', googleId: '' },
      currentDetgoriId: null,
    };
  
    componentDidMount() {
      axios({
        method: 'GET',
        url: httpsfy(this.props.detgoriUrl, process.env.NODE_ENV),
        withCredentials: true,
      })
        .then((res) => res.data)
        .then((data) => {
          this.setState({ detgoriInfo: data });
        });
    }
  
    render() {
      return (
        <div>
          <button
            className="btn m-1 btn-light border"
            value={this.state.detgoriInfo.googleId}
            onClick={this.props.onClick}
          >
            {this.state.detgoriInfo.authorName}
          </button>
        </div>
      );
    }
  }

  export default NameCard;