import { useHistory } from "react-router";
import { useState } from "react";
function Header({links, defaultLinkState}){
    const [link, setLink] = useState(defaultLinkState);
    const history = useHistory();
    const onNavClick = (link) => {
      history.push({
        pathname: link
      });
      setLink(link);
    }
    // selected, pageSelect, address
    return (
        <div name="header">
        <div className="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
          <span className="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none justify-content-center">
            <span className="fs-4 px-4">
              <img width="30px" src="/blue.ico" alt="icon" />
              한누리
            </span>
          </span>
          <ul className="nav nav-pills justify-content-center">
            {links(link, onNavClick)}
          </ul>
        </div>
      </div>
    )
}

export default Header;
