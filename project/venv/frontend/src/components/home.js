import { Component } from "react";
import { Table } from "react-bootstrap";
import { Link } from "react-router-dom";
import axios from 'axios'


const Project = (props) => (
  <tr>
    <td>{props.projects.name}</td>
    <td>{props.projects.id}</td>
    <td>{props.projects.description}</td>
    <td>
      <Link style={{color:"Aqua"}} to={"/projects/"+props.projects._id}>Log in</Link>
    </td>
  </tr>
);

class Home extends Component {

  state = {
    projects: []
  };

  componentDidMount() {
      axios.get('/')
        .then(response => {
          this.setState({ projects: response.data });
        })
        .catch((error) => {
          console.log(error);
        })
    }

  fillTable() {
    console.log(this.state.projects)
    return this.state.projects.map(currentproject => {
      return <Project project={currentproject} key={currentproject._id}/>;
    })
  }  

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
            <tr>
              <td>Project 1</td>
              <td>111</td>
              <th>Description</th>
              <td><Link  style={{color:"Aqua"}} to="/project">Log in</Link></td>
            </tr>
            <tr>
              <td>Project 2</td>
              <td>222</td>
              <th>Description</th>
              <td><Link  style={{color:"Aqua"}} to="/project">Log in</Link></td>
            </tr>
            <tr>
              <td >Project3</td>
              <td>333</td>
              <th>Description</th>
              <td><Link style={{color:"Aqua"}} to="/project/1234">Log in</Link></td>
            </tr>
            { this.fillTable() }
          </tbody>
        </Table>
        <Link id="newproject" to="/createProject">Create New Project</Link>
      </div>
    );
  }
}

export default Home;
