
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
        for(let note of this.props.info){
          newInfoState[note.position] = note;
        }
        this.setState({ info: newInfoState, writingPosition: -1 });
      }
    }
  
    handleClick = (position) => {
      this.setState({ writingPosition: position });
    };
  
    render() {
      const notes = this.state.info.map((_ ,idx)=> {
        return (
            <div style={{width:'50%'}} className="p-1 h-rem15" key={idx}>
              <Note
                info={this.state.info[idx]}
                onClick={this.handleClick}
                page={this.props.page}
                position={idx}
                onUpload={this.props.onUpload}
                writing={this.state.writing[idx]}
              />
            </div>
        )
      })
      return (
        <div style={{display:'flex', width:'100%',flexWrap:'wrap'}}>
          {notes}
        </div>
      )
    }
  }