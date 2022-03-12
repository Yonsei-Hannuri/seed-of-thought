import React, {Component} from 'react';

class SignInForm extends Component {
    static defaultProps ={
        signinError: false,
        signinUrl: false,
    };

    state = {
        name: '',
        generation: 20,
    };

    handleNameChange = (e) => {
        this.setState({ name: e.target.value });
      };
    
    handleGenerationChange = (e) => {
    this.setState({ generation: e.target.value });
    };

    render(){
        return (
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
                {this.props.signinError ? (
                  <span className="m-2">이미 등록되었습니다.</span>
                ) : (
                  <a
                    href={
                      this.props.signinUrl +
                      `&state={"name": "${this.state.name}", "generation": "${this.state.generation}"}`
                    }
                    className="btn btn-lg btn-secondary fw-bold border-white bg-white"
                  >
                    구글 이메일로 등록
                  </a>
                )}
              </p>
            </main>
        )
    }
}

export default SignInForm;
