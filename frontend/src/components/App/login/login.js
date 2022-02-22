import React, { Component } from 'react';
import emailOauth from '../../../config/emailOauth.json';

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
    });
  };

  handleNameChange = (e) => {
    this.setState({ name: e.target.value });
  };

  handleGenerationChange = (e) => {
    this.setState({ generation: e.target.value });
  };

  render() {
    if (this.state.login) {
      return (
        <div className="d-flex text-center h-100 text-white bg-theme">
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
            <main>
              <h1>생각의 씨앗,</h1>
              <h1>완전한 만남.</h1>
              <div className="lead my-3">
                <a href={emailOauth.loginUrl}>
                  <img width="200px" src="/google.png" alt="google login" />
                </a>
                <p className="my-2 py-2">
                  {this.state.signinSuccess
                    ? '등록되었습니다. 임원진 확인 후 로그인 할 수 있습니다.'
                    : ''}
                </p>
                <p className="my-2 py-2">
                  {this.state.loginError ? '로그인에 실패했습니다.' : ''}
                </p>
              </div>
            </main>

            <footer className="mt-auto text-white-50"></footer>
          </div>
        </div>
      );
    } else if (this.state.signin) {
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
            <main className="px-3">
              <h1>생각의 씨앗,</h1>
              <h1>완전한 만남.</h1>
              <div style={{ width: '300px' }} className="m-auto">
                이름
                <input
                  className="form-control text-center"
                  value={this.state.name}
                  onChange={this.handleNameChange}
                  type="text"
                  required
                />
                기수
                <input
                  className="form-control text-center"
                  value={this.state.generation}
                  onChange={this.handleGenerationChange}
                  type="number"
                />
              </div>
              <p className="lead my-3">
                {this.state.signinError ? (
                  <span className="m-2">이미 등록되었습니다.</span>
                ) : (
                  <a
                    href={
                      emailOauth.signinUrl +
                      `&state={"name": "${this.state.name}", "generation": "${this.state.generation}"}`
                    }
                    className="btn btn-lg btn-secondary fw-bold border-white bg-white"
                  >
                    구글 이메일로 등록
                  </a>
                )}
              </p>
            </main>

            <footer className="mt-auto text-white-50"></footer>
          </div>
        </div>
      );
    }
  }
}

export default Login;
