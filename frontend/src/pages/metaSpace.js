import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import EasterEgg from "../components/easterEgg";
import FreeNote from './freeNote';
import Archive from './archive/archive';

function MetaSpace(props) {
  return (
    <div className='d-flex flex-column'>
      <Router>
        <Switch>
            <Route exact path="/metaspace/freenote" component={FreeNote}/>
            <Route exact path="/metaspace/archive" component={Archive}/>
            <Route exact path="/metaspace">
              <Link to="/metaspace/freenote">
                <img
                  name='freeNote' 
                  className="m-3 p-3 cursor2Pointer"
                  src="img/notebook.png"
                  width="220"
                  height="220"
                  alt="Notebook  free icon"
                  title="Notebook free icon"
                />
              </Link>
              {/* <Link to="/metaspace/archive">
                <img
                  name='archive'
                  className="m-3 p-3 cursor2Pointer"
                  style={{alignSelf:'center'}}
                  src="img/fossil.png"
                  width="220"
                  height="220"
                  alt="arhchive"
                  title="arhchive"
                />
              </Link> */}
            <EasterEgg/>
          </Route>
        </Switch>
      </Router>
    </div>
  ); 
}

export default MetaSpace;
