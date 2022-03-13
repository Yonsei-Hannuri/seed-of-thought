import React, { Component } from 'react';
import emailOauth from '../config/emailOauth.json';
import LoginForm from '../components/login/loginForm';
import SignInForm from '../components/login/signinForm';

class Login extends Component {
  state = {
    signinError: false,
    signinSuccess: false,
    login: true,
    loginError: false,
    signin: false,
    name: '',
    generation: 20,
  };

  componentDidMount() {
    const urlSearchParams = new URLSearchParams(window.location.search);
    const params = Object.fromEntries(urlSearchParams.entries());
    if (params.type === 'signinError') {
      this.setState({ signinError: true, signin: true, login: false });
    } else if (params.type === 'signinSuccess') {
      this.setState({ signinSuccess: true, signin: false, login: true });
    } else if (params.login === 'error') {
      this.setState({ loginError: true, login: true, signin: false });
    }
  }

  handleClick = (e) => {
    this.setState({
      login: false,
      signin: false,
      [e.target.name]: true,
    })
  }

  render() {
      return (
        <div className="d-flex h-100 text-center text-white bg-theme">
          <div className="cover-container d-flex w-100 h-100 p-3 mx-auto flex-column">
            <header className="mb-auto">
              <div>
                <h3 className="float-md-start mb-0">한누리</h3>
                <nav className="nav nav-masthead justify-content-center float-md-end">
                  <button
                    className={
                      this.state.login
                        ? 'nav-link active link-button2'
                        : 'nav-link link-button2'
                    }
                    name="login"
                    onClick={this.handleClick}
                    href="#"
                  >
                    로그인
                  </button>
                  {/*<a className="nav-link" href="#">홍보</a>*/}
                  <button
                    className={
                      this.state.signin
                        ? 'nav-link active link-button2'
                        : 'nav-link link-button2'
                    }
                    name="signin"
                    onClick={this.handleClick}
                    href="#"
                  >
                    가입요청
                  </button>
                </nav>
              </div>
            </header>
            {this.state.login ? 
              <LoginForm 
                loginUrl={emailOauth.loginUrl} 
                signinSuccess={this.state.signinSuccess} 
                loginError={this.state.loginError}
              /> : 
              <SignInForm
                signinError={this.state.signinError}
                signinUrl={emailOauth.signinUrl}
              />}
            <footer className="mt-auto text-white-50"></footer>
          </div>
        </div>
      );
    }
}

export default Login;
