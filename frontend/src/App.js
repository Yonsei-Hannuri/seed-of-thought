import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import MainPage from './pages/mainPage';
import Mypage from './pages/mypage';
import Session from './pages/session';
import LoginPage from './pages/loginPage';
import HeaderNav from './components/headerNav';
import Footer from './components/footer';
import getCookieValue from './modules/getCookieValue';

class App extends Component {
  render() {
    const isLogined = getCookieValue(document.cookie, 'isLogin');
    if (isLogined === null || isLogined === 'false') {
      return (
        <div id="fadein" className="h-100">
          <LoginPage />
        </div>
      );
    }
    return (
      <div className="container">
        <Router>
          <Switch>
            <Route path="/session" component={Session} />
            <Route>
              <HeaderNav
                defaultLinkState={'/' + window.location.pathname.split('/')[1]}
                links={(link, onNavClick) => {
                  return (
                    <>
                      <li className="nav-item">
                        <button
                          name="main"
                          className={
                            'nav-link ' + (link === '/' ? 'active' : '')
                          }
                          onClick={() => onNavClick('/')}
                        >
                          메인
                        </button>
                      </li>
                      <li className="nav-item">
                        <button
                          name="mypage"
                          className={
                            'nav-link ' + (link === '/mypage' ? 'active' : '')
                          }
                          onClick={() => onNavClick('/mypage')}
                        >
                          마이페이지
                        </button>
                      </li>
                      <li className="nav-item">
                        <a
                          href={process.env.REACT_APP_API_URL + 'logout/'}
                          className="nav-link"
                        >
                          로그아웃
                        </a>
                      </li>
                    </>
                  );
                }}
              />
              <Switch>
                <Route exact path="/" component={MainPage} />
                <Route exact path="/mypage" component={Mypage} />
              </Switch>
            </Route>
          </Switch>
        </Router>
        <Footer />
      </div>
    );
  }
}

export default App;
