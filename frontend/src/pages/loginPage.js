import LoginForm from '../components/login/loginForm';
import getQueryParams from '../modules/getQueryParams';

function Login() {
  const isError = getQueryParams()?.login === 'error';
  return (
    <div className="d-flex h-100 text-center text-white bg-theme">
      <div className="cover-container d-flex w-100 h-100 p-3 mx-auto flex-column">
        <header className="mb-auto">
          <h3 className="float-md-start mb-0">한누리</h3>
        </header>
        <LoginForm
          googleUrl={process.env.REACT_APP_GOOGLE_OAUTH_LOGIN_URL}
          isError={isError}
        />
        <footer className="mt-auto text-white-50"></footer>
      </div>
    </div>
  );
}

export default Login;
