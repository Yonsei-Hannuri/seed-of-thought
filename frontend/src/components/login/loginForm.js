/**
 *
 * @param {{ googleUrl, isError }} props
 * @returns
 */
function LoginForm(props) {
  return (
    <main>
      <h1>생각의 씨앗,</h1>
      <h1>완전한 만남.</h1>
      <div className="lead my-3">
        <a href={props.googleUrl}>
          <img width="200px" src="/google.png" alt="google login" />
        </a>
        <p className="my-2 py-2">
          {props.isError ? '로그인에 실패했습니다.' : ''}
        </p>
      </div>
    </main>
  );
}

export default LoginForm;
