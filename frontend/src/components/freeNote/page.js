
import React, {Component} from 'react';
import Note from './note';

export default class Page extends Component {
    static defaultProps = {
      info: [],
      page: 1,
      onUpload: null,
    };
  
    state = {
      info: [false, false, false, false, false, false, false, false],
      writing: [false, false, false, false, false, false, false, false],
      writingPosition: -1,
    };
  
    componentDidMount() {
      let newInfoState = [false, false, false, false, false, false, false, false];
      for (let i = 0; i < this.props.info.length; i++) {
        let note = this.props.info[i];
        newInfoState = newInfoState
          .slice(0, note.position)
          .concat([note])
          .concat(newInfoState.slice(note.position + 1, 8));
      }
      this.setState({ info: newInfoState });
    }
  
    componentDidUpdate(prevProps, prevState) {
      //when clicked for update => set state which note is selected(only one at once)
      if (prevState.writingPosition !== this.state.writingPosition) {
        let newWritingState = [
          false,
          false,
          false,
          false,
          false,
          false,
          false,
          false,
        ];
        newWritingState[this.state.writingPosition] = true;
        this.setState({
          writing: newWritingState,
        });
      }
  
      //when page is changed => new info state
      if (prevProps.info !== this.props.info) {
        let newInfoState = [
          false,
          false,
          false,
          false,
          false,
          false,
          false,
          false,
        ];
        for (let i = 0; i < this.props.info.length; i++) {
          let note = this.props.info[i];
          newInfoState = newInfoState
            .slice(0, note.position)
            .concat([note])
            .concat(newInfoState.slice(note.position + 1, 8));
        }
        this.setState({ info: newInfoState, writingPosition: -1 });
      }
    }
  
    handleClick = (position) => {
      this.setState({ writingPosition: position });
    };
  
    render() {
      return (
        <div>
          <div className="row">
            <div className="p-2 col-sm-6 h-rem15">
              <Note
                info={this.state.info[0]}
                onClick={this.handleClick}
                onUpload={this.props.onUpload}
                page={this.props.page}
                position={0}
                writing={this.state.writing[0]}
              />
            </div>
            <div className="p-2 col-sm-6 h-rem15">
              <Note
                info={this.state.info[1]}
                onClick={this.handleClick}
                onUpload={this.props.onUpload}
                page={this.props.page}
                position={1}
                writing={this.state.writing[1]}
              />
            </div>
          </div>
          <div className="row">
            <div className="p-2 col-sm-6 h-rem15">
              <Note
                info={this.state.info[2]}
                onClick={this.handleClick}
                onUpload={this.props.onUpload}
                page={this.props.page}
                position={2}
                writing={this.state.writing[2]}
              />
            </div>
            <div className="p-2 col-sm-6 h-rem15">
              <Note
                info={this.state.info[3]}
                onClick={this.handleClick}
                onUpload={this.props.onUpload}
                page={this.props.page}
                position={3}
                writing={this.state.writing[3]}
              />
            </div>
          </div>
          <div className="row =">
            <div className="p-2 col-sm-6 h-rem15">
              <Note
                info={this.state.info[4]}
                onClick={this.handleClick}
                onUpload={this.props.onUpload}
                page={this.props.page}
                position={4}
                writing={this.state.writing[4]}
              />
            </div>
            <div className="p-2 col-sm-6 h-rem15">
              <Note
                info={this.state.info[5]}
                onClick={this.handleClick}
                onUpload={this.props.onUpload}
                page={this.props.page}
                position={5}
                writing={this.state.writing[5]}
              />
            </div>
          </div>
          <div className="row">
            <div className="p-2 col-sm-6 h-rem15">
              <Note
                info={this.state.info[6]}
                onClick={this.handleClick}
                onUpload={this.props.onUpload}
                page={this.props.page}
                position={6}
                writing={this.state.writing[6]}
              />
            </div>
            <div className="p-2 col-sm-6 h-rem15">
              <Note
                info={this.state.info[7]}
                onClick={this.handleClick}
                onUpload={this.props.onUpload}
                page={this.props.page}
                position={7}
                writing={this.state.writing[7]}
              />
            </div>
          </div>
        </div>
      );
    }
  }