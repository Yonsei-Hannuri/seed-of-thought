import React, { Component } from 'react';
import MainPage from './pages/mainPage';
import Mypage from './pages/mypage';
import MetaSpace from './pages/metaSpace';
import Session from './pages/session';
import FreeNote from './pages/freeNote';
import LoginPage from './pages/loginPage';
import getCookieValue from './modules/getCookieValue';
import HeaderNav from './components/App/headerNav';
import Footer from './components/App/footer';
import address from './config/address.json';

class App extends Component {
  state = {
    selected: 'main',
    e: ''
  };

  pageSelect = (e) => {
    this.setState({
      selected: e.target.name,
      e : e
    });
  };

  render() {
    const isLogined = getCookieValue(document.cookie, 'isLogin');
    const path = window.location.pathname.trim().split('/');
    console.log(path);
    if (isLogined===null || isLogined === 'false') {
      return (
        <LoginPage />
      );
    } else if (path[1] === 'session'){
      return (
        <div className="container">
          <Session/>
        </div>
      );
    }
    return (   
      <>
        <div className="container">
          <HeaderNav selected={this.state.selected} pageSelect={this.pageSelect} address={address}/>
          {this.state.selected === 'main' ? 
            <MainPage/> : 
            this.state.selected === 'metaSpace' ? 
            <MetaSpace pageSelect={this.pageSelect}/> : 
            this.state.selected === 'mypage' ? 
            <Mypage/> :
            this.state.selected === 'freeNote' ?
            <FreeNote/> :
            <MainPage/>
          }
          <Footer/>
        </div>
      </>
    );
  }
}

export default App;
