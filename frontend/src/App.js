import React, { Component } from 'react';
import MainPage from './pages/mainPage';
import Mypage from './pages/mypage';
import MetaSpace from './pages/metaSpace';
import Session from './pages/session';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import FreeNote from './pages/freeNote';
import LoginPage from './pages/loginPage';
import getCookieValue from './modules/getCookieValue';
import Header from './components/App/header';
import Footer from './components/App/footer';
import address from './config/address.json';

class App extends Component {
  state = {
    selected: {
      main: true,
      metaSpace: false,
      mypage: false,
    }
  };

  handleToggle = (e) => {
    this.setState({
      selected: {
        main: false,
        metaSpace: false,
        mypage: false,
        [e.target.name]: true,
      }
    });
    window.location.href = `/${e.target.name}`;
  };

  render() {
    const isLogined = getCookieValue(document.cookie, 'isLogin');
    if (isLogined===null || isLogined === 'false') {
      return (
        <LoginPage />
      );
    }
    return (
      <>
        <BrowserRouter>
        <div className="container">
          <Header selected={this.state.selected} handleToggle={this.handleToggle} address={address}/>
          <Switch>
            <Route exact path="/metaSpace" component={MetaSpace}/>
            <Route exact path="/mypage" component={Mypage}/>
            <Route exact path="/session" component={Session} />
            <Route exact path="/freeNote" component={FreeNote} />
            <Route path={['/', '/main']} component={MainPage} />
          </Switch>
          <Footer/>
        </div>
        </BrowserRouter>
      </>
    );
  }
}

export default App;
