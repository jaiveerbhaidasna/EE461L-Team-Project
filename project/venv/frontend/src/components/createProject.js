import { Component } from "react";
import { Form, Button } from "react-bootstrap";
//import axios from 'axios'

class CreateProject extends Component {
  state = {
    name: "",
    id: "",
    description: ""
  };

  handleChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  handleSubmit = (e) => {
    e.preventDefault();

    // const user = {
    //     email: this.state.email,
    //     password: this.state.password,
    // }

    // axios.post("http://localhost:5000/auth/login", user)
    //     .then(res => {
    //         console.log(res.data);
    //         //window.location = "/";
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
            <Form.Label>Project Name</Form.Label>
            <Form.Control
              autoFocus
              type="email"
              name="email"
              onChange={this.handleChange}
            />
          </Form.Group>
          <Form.Group size="lg" controlId="password">
            <Form.Label>Description</Form.Label>
            <Form.Control
              type="password"
              name="password"
              onChange={this.handleChange}
            />
          </Form.Group>
          <Form.Group size="lg" controlId="password">
            <Form.Label>Project ID</Form.Label>
            <Form.Control
              type="password"
              name="password"
              onChange={this.handleChange}
            />
          </Form.Group>
          <Button block size="lg" type="submit">
            Create Project
          </Button>
        </Form>
      </div>
    );
  }
}

export default CreateProject;
