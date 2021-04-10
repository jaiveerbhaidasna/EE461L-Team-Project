import { Component } from "react";
import { Form, Button } from "react-bootstrap";
import axios from 'axios';
import { Link } from "react-router-dom";

class Login extends Component {
  state = {
    email: "",
    password: "",
  };

  handleChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  handleSubmit = (e) => {
    e.preventDefault();

    const user = {
        email: this.state.email,
        password: this.state.password,
    }
    axios.post("https://dry-lowlands-32590.herokuapp.com/login", user)
        .then(res => {
            if(res.data === "error"){
              alert("Wrong Email and Password combination!")
            }
            else{
              window.location = "/";
              alert("Successfully logged in")
            }
            console.log(res.data);
        })
        .catch(err => {
            console.log(err);
        })
  };

  render() {
    return (
      <div className="Login">
        <Form onSubmit={this.handleSubmit}>
          <Form.Group size="lg" controlId="email">
            <Form.Label>Email</Form.Label>
            <Form.Control
              autoFocus
              type="email"
              name="email"
              onChange={this.handleChange}
            />
          </Form.Group>
          <Form.Group size="lg" controlId="password">
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              name="password"
              onChange={this.handleChange}
            />
          </Form.Group>
          <Button block size="lg" type="submit">
            Login
          </Button>
          <sub>
            <Link to="/signup">Don't have an account? Create one today.</Link>
          </sub>
        </Form>
      </div>
    );
  }
}

export default Login;
