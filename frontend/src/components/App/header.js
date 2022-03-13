function Header(props){
    // selected, handleToggle, address
    console.log(props.selected);
    return (
        <div name="header">
        <div className="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
          <span className="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none justify-content-center">
            <span className="fs-4 px-4">
              <img width="30px" src="blue.ico" alt="icon" />
              한누리
            </span>
          </span>
          <ul className="nav nav-pills justify-content-center">
            <li className="nav-item">
              <button
                name="main"
                className={'nav-link ' + (props.selected.main ? 'active' : '')}
                onClick={props.handleToggle}
              >
                메인
              </button>
            </li>
            <li className="nav-item">
              <button
                name="metaSpace"
                className={
                  'nav-link ' + (props.selected.metaSpace ? 'active' : '')
                }
                onClick={props.handleToggle}
              >
                메타동방
              </button>
            </li>
            <li className="nav-item">
              <button
                name="mypage"
                className={'nav-link ' + (props.selected.mypage ? 'active' : '')}
                onClick={props.handleToggle}
              >
                마이페이지
              </button>
            </li>
            <li className="nav-item">
              <a href={props.address.back + 'logout/'} className="nav-link">
                로그아웃
              </a>
            </li>
          </ul>
        </div>
      </div>
    )
}

export default Header;
