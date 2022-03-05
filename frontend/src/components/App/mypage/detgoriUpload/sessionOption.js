import React, {Component} from 'react';
import axios from 'axios';
import errorReport from '../../../../modules/errorReport';

export default class SessionOption extends Component {
    static defaultProps = {
      url: '',
    };
    state = {
      info: {},
    };
    componentDidMount() {
      let url = this.props.url;
      axios({
        method: 'GET',
        url: url,
        withCredentials: true,
      })
        .then((res) => res.data)
        .then((data) => this.setState({ info: data }))
        .catch((e) => errorReport(e, 'sessionOption_componentDidMount'));
    }
    render() {
      return (
        <option value={this.state.info.id}>
          {this.state.info.week}주차: {this.state.info.title}
        </option>
      );
    }
  }