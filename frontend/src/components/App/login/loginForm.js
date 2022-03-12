function LoginForm (props){ 
    //loginUrl, sininSuccess, loginError
    return (  
        <main>
            <h1>생각의 씨앗,</h1>
            <h1>완전한 만남.</h1>
            <div className="lead my-3">
            <a href={props.loginUrl}>
                <img width="200px" src="/google.png" alt="google login" />
            </a>
            <p className="my-2 py-2">
                {props.signinSuccess
                ? '등록되었습니다. 임원진 확인 후 로그인 할 수 있습니다.'
                : ''}
            </p>
            <p className="my-2 py-2">
                {props.loginError ? '로그인에 실패했습니다.' : ''}
            </p>
            </div>
        </main>
    )
}

export default LoginForm;
