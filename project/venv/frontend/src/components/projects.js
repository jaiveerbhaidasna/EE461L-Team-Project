import { Component } from "react";
import { Form, Button } from "react-bootstrap";
import axios from 'axios'

class Projects extends Component {
  state = {
    name: "",
    id: "",
    description: "",
  };

  handleChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  handleSubmit = (e) => {
    e.preventDefault();

    const project = {
        name: this.state.email,
        id: this.state.password,
        description: this.state.description,
    }

    axios.post("http://localhost:5000/projects/", project)
        .then(res => {
            console.log(res.data);
            window.location = "/";
        })
        .catch(err => {
            console.log(err);
        })
  };

  render() {
    return (
      <div className="Login">
        <Form onSubmit={this.handleSubmit}>
          <Form.Group size="lg" controlId="name">
            <Form.Label>Project Name</Form.Label>
            <Form.Control
              autoFocus
              type="name"
              name="name"
              onChange={this.handleChange}
            />
          </Form.Group>
          <Form.Group size="lg" controlId="description">
            <Form.Label>Description</Form.Label>
            <Form.Control
              type="description"
              name="description"
              onChange={this.handleChange}
            />
          </Form.Group>
          <Form.Group size="lg" controlId="id">
            <Form.Label>Project ID</Form.Label>
            <Form.Control
              type="id"
              name="id"
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

export default Projects;
