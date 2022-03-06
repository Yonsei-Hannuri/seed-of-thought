import axios from "axios";
import React, { Component } from "react";
import Folder from "./folder";
import address from '../../../../../config/address.json';
import errorReport from "../../../../../modules/errorReport";

class FolderUI extends Component {
    state = {
        seasonSessionInfos: [],
        ajaxError: false,
    }

    componentDidMount(){
        this.getSessionInfos()
    }

    getSessionInfos = () => {
        axios({
            method: 'GET',
            url: address.back + 'session/',
            params: {
                seasonSessionInfos: true
            },
            withCredentials: true,
          })
            .then((res) => res.data)
            .then((data) => {
              this.setState({
                seasonSessionInfos: data
              });
            })
            .catch((e) => {
              this.setState({ ajaxError: true });
              errorReport(e, 'folderUI');
            });
    }
    
    render(){
        const Folders = this.state.seasonSessionInfos.map((sessionInfo, idx) => (
            <Folder sessionInfo={sessionInfo} idx={idx} key={idx}/>
        ))
        return(
            <div className="folderUI">
                {Folders}
            </div>
        )
    }
}

export default FolderUI;
