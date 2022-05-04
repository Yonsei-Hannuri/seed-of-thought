import React, { Component } from 'react';
import httpsfy from '../../modules/httpsfy';
import axios from 'axios';

class NameCard extends Component {
    static defaultProps = {
      onClick: null,
      detgoriUrl: null,
    };
  
    state = {
      detgoriInfo: { authorName: '', googleId: '' },
      currentDetgoriId: null,
      clicked: false,
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
  
    handleClick() {
      setTimeout(() => this.setState({clicked: true}), 2000);
    }


    render() {
      const authorColor = this.state.detgoriInfo.authorColor
      return (
        <div>
          <button
            style={{
              border: `2px solid ${authorColor}`,
              boxShadow: `0px 0px 3px ${authorColor}`,
              color: `${this.state.clicked ? 'Gainsboro' : 'black'}`,
            }}
            className="btn m-1 btn-light"
            value={this.state.detgoriInfo.googleId}
            onClick={(e)=>{this.props.onClick(e); this.handleClick();}}
          >
            {this.state.detgoriInfo.authorName}
          </button>
        </div>
      );
    }
  }

  export default NameCard;