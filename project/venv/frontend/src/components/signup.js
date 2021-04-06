import { Component } from "react";
import { Form, Button} from "react-bootstrap";
//import axios from 'axios'

class Signup extends Component {
  state = {
    email: "",
    password: "",
  };

  handleChange = (e) => {
      this.setState(
        {
          [e.target.name]: e.target.value,
        },
        () => {
          console.log(this.state);
        }
      );
  };

  handleSubmit = (e) => {
    e.preventDefault();

    // const user = {
    //     isMentor: this.state.isMentor,
    //     email: this.state.email,
    //     password: this.state.password,
    //     firstName: this.state.firstname,
    //     lastName: this.state.lastname,
    //     age: this.state.age
    // }

    // axios.post("http://localhost:5000/auth/register", user)
    //     .then(res => {
    //         console.log(res.data);
    //         window.location = "/";
    //     })
    //     .catch(err => {
    //         console.log(err);
    //     })
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
            Sign Up
          </Button>
        </Form>
      </div>
    );
  }
}

export default Signup;
