import React, { Component } from 'react';
import MainPage from './pages/mainPage';
import Mypage from './pages/mypage';
import MetaSpace from './pages/metaSpace';
import Session from './pages/session';
import FreeNote from './pages/freeNote';
import Archive from './pages/archive/archive';
import LoginPage from './pages/loginPage';
import HeaderNav from './components/headerNav';
import Footer from './components/footer';
import getCookieValue from './modules/getCookieValue';
import address from './config/address.json';
import delay from './modules/delay'

import {
  RecoilRoot,
} from 'recoil';

class App extends Component {
  state = {
    selected: 'main',
  };


  componentDidMount(){
    document.getElementById('fadein').classList.remove('fadeinElem')
    document.getElementById('fadein').classList += ' fadeinElem';
    delay(700).then(() => document.getElementById('fadein').classList.remove('fadeinElem'));
  }

  pageSelect = (e) => {
    this.setState({
      selected: e.target.name,
    });
    document.getElementById('fadein').classList.remove('fadeinElem')
    document.getElementById('fadein').classList += 'fadeinElem';
    delay(700).then(() => document.getElementById('fadein').classList.remove('fadeinElem'));
  };

  render() {
    const isLogined = getCookieValue(document.cookie, 'isLogin');
    const path = window.location.pathname.trim().split('/');
    if (isLogined===null || isLogined === 'false') {
      return (
        <div id='fadein' className='h-100'>
          <LoginPage />
        </div>
      );
    } else if (path[1] === 'session'){
      return (
        <div id='fadein' className="container">
          <Session/>
        </div>
      )};
    return (   
      <>
        <div className="container">
          <HeaderNav selected={this.state.selected} pageSelect={this.pageSelect} address={address}/>
          <div id="fadein">
            {this.state.selected === 'main' ? 
              <MainPage/> : 
              this.state.selected === 'metaSpace' ? 
              <MetaSpace pageSelect={this.pageSelect}/> : 
              this.state.selected === 'mypage' ? 
              <Mypage/> :
              this.state.selected === 'freeNote' ?
              <FreeNote pageSelect={this.pageSelect}/> :
              this.state.selected === 'archive'? 
              <RecoilRoot>
                <Archive pageSelect={this.pageSelect}/>
              </RecoilRoot>
              :
              <MainPage/>
            }
          <Footer/>
          </div>
        </div>
      </>
    );
  }
}

export default App;
