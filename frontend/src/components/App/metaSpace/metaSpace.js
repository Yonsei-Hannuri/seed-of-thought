import React, { Component } from 'react';

class MetaSpace extends Component {
  static defaultProps = {
    active: false,
  };

  render() {
    if (this.props.active) {
      return (
        <div>
          <a href="/freeNote">
            <img
              className="m-3 p-3 cursor2Pointer"
              src="https://image.flaticon.com/icons/png/512/3324/3324709.png"
              width="220"
              height="220"
              alt="Notebook  free icon"
              title="Notebook free icon"
            ></img>
          </a>
        </div>
      );
    } else {
      return '';
    }
  }
}

export default MetaSpace;
