import React, { Component } from 'react';
import Login from './components/App/login/login';
import Index from './components/App/index';
import Session from './components/App/session/session';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import freeNote from './components/App/metaSpace/freeNote/freeNote';

class App extends Component {
  render() {
    return (
      <>
        <BrowserRouter>
          <Route exact path="/login" component={Login} />
          <Route exact path="/" component={Index} />
          <div className="container">
            <br />
            <Switch>
              <Route exact path="/session" component={Session} />
              <Route exact path="/freeNote" component={freeNote} />
            </Switch>
          </div>
          <br />
        </BrowserRouter>
      </>
    );
  }
}

export default App;
