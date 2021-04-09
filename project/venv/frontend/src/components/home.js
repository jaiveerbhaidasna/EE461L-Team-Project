import { Component } from "react";
import { Table } from "react-bootstrap";
import { Link } from "react-router-dom";
import axios from 'axios'


const Project = (props) => (
  <tr>
    <td>{props.project.name}</td>
    <td>{props.project.id}</td>
    <td>{props.project.description}</td>
    <td>
      <Link style={{color:"Aqua"}} to={"/project/"+props.project.id}>Log in</Link>
    </td>
  </tr>
);

class Home extends Component {

  state = {
    projects: [],
    projectid: ""
  };

  componentDidMount() {
      // axios.get('http://localhost:5000/')
      //   .then(response => {
      //     this.setState({ projects: response.data });
      //   })
      //   .catch((error) => {
      //     console.log(error);
      //   })
    }

  fillTable() {
    return this.state.projects.map(currentproject => {
      return <Project project={currentproject} key={currentproject._id}/>;
    })
  }  

  handleChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
    console.log(e.target)
  };

  render() {
    return (
      <div>
        <h1 className="projects">Projects</h1>
        <Table  style={{color:"Aqua"}} striped bordered hover variant="dark">
          <thead>
            <tr>
              <th>Project Name</th>
              <th>ID</th>
              <th>Description</th>
              <th>Log in to Project</th>
            </tr>
          </thead>
          <tbody>
            {/* { this.fillTable() } */}
          </tbody>
        </Table>
        <Link id="newproject" to="/projects">Create New Project</Link>
        <input type="text" name="projectid" onChange={this.handleChange}></input>
        <Link style={{color:"Aqua"}} to={"/project/"+this.state.projectid}>Log in</Link>
      </div>
    );
  }
}

export default Home;
