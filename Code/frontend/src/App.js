import {React, Component} from "react";
import { BrowserRouter as Router, Switch, Route} from "react-router-dom";
import './style.css'

import {
  Nav,
  Navbar,
  Button,
  ButtonGroup,
} from "react-bootstrap";
//import "bootstrap/dist/css/bootstrap.min.css";
//import axios from "axios";

import Home from "./components/home";
import Signup from "./components/signup";
import Login from "./components/login";
import Project from "./components/project";
import Datasets from "./components/datasets";
import CreateProject from "./components/projects";


class App extends Component{


  componentDidMount

  render(){
    return (
      <Router>
        <div>
          <Navbar className="py-2" bg="light" expand="lg">
            <Navbar.Brand href="/" className="ml-5">
              Project Title
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="ml-auto">
                <ButtonGroup aria-label="Basic example" className="mr-2">
                  <Button href="/" variant="light">
                    Home
                  </Button>
                  <Button href="/datasets" variant="light">
                    Datasets
                  </Button>
                  <Button href="/login" variant="light">
                    Log In
                  </Button>
                </ButtonGroup>
              </Nav>
            </Navbar.Collapse>
          </Navbar>
  
          {/* A <Switch> looks through its children <Route>s and
              renders the first one that matches the current URL. */}
          <Switch>
            <Route path="/signup">
              <Signup />
            </Route>
            <Route path="/login">
              <Login />
            </Route>
            <Route path="/project">
              <Project />
            </Route>
            <Route path="/projects">
              <CreateProject />
            </Route>
            <Route path="/datasets">
              <Datasets />
            </Route>
            <Route path="/">
              <Home />
            </Route>
          </Switch>
        </div>
      </Router>
    );
  }
  
}

export default App;
