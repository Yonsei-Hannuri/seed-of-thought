import React, { Component } from "react";
import address from '../../../../../config/address.json'

class Folder extends Component {
    static defaultProps = {
        idx: '',
        sessionInfo: ''
    }

    clickFolderTagText = (e) => {
        const topAdjustCoeff = this.props.idx;
        const folder = e.target.parentElement.parentElement;
        if (Number(folder.style.top.slice(0,2)) > 50) {
            folder.style.top = Number(folder.style.top.slice(0,2))-45+'%';
        } else{
            folder.style.top = (82 - topAdjustCoeff * 3) + '%';
        }
    }

    render(){
        const leftAdjustCoeff = this.props.idx % 4;
        const topAdjustCoeff = this.props.idx;
        const folderStyle={
            width:  98 - 3*this.props.idx +'%',
            top: (82 - topAdjustCoeff * 3) + '%',
            zIndex: 10 - this.props.idx,
            left: Math.random()*6 + '%'
        }
        const folderTagStyle = {
            backgroundColor: '#cadcf8',
            left: leftAdjustCoeff * 25 + '%',

        }
        const folderBodyStyle = {
            backgroundColor: '#cadcf8',
        }
        return(
            <div className="folder" style={folderStyle}>
                <div className="folderTag" style={folderTagStyle}>
                    <div className="folderTagText" onClick={this.clickFolderTagText}>
                        {this.props.sessionInfo.week + ' 주차'}
                    </div>
                </div>
                <div className="folderBody" style={folderBodyStyle}>
                    <div className="folderBodyText">
                        <a className="folderUI_link" href={address.front + 'session/?sessionID='+this.props.sessionInfo.id}>
                            {this.props.sessionInfo.title}
                        </a>
                    </div>
                </div>
            </div>
        )
    }
}

export default Folder;