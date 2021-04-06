import { Component } from "react";
import { Table, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
//import axios from 'axios'

// const HardwareSet = (props) => (
//   <tr>
//     <td>{props.hardwareset.name}</td>
//     <td>{props.hardwareset.capacity}</td>
//     <td>{props.hardwareset.availability}</td>
//     <td>{props.hardwareset.request}</td>
//     <td>
//       <input></input>
//     </td>
//     <td>
//       <Button href="." onClick={() => { props.checkin(props.hardwareset._id) }}>Check in</Button>
//     </td>
//     <td>
//       <Button href="." onClick={() => { props.checkout(props.hardwareset._id) }}>Check out</Button>
//     </td>
//   </tr>
// );

class Project extends Component {
  state = {
    name: "",
    capacity: 0,
    availability: 0,
    request: 0
  };

//   componentDidMount() {
//     axios
//       .get("/hardwaresets/" + this.props.match.params.id)
//       .then((response) => {
//         this.setState({
//           name: response.data.name,
//           capacity: response.data.capacity,
//           availability: response.data.availability,
//         });
//       })
//       .catch((error) => {
//         console.log(error);
//       });
//   }

  //   fillTable() {
  //     return this.state.hardwaresets.map(currentset => {
  //       return <HardwareSet hardwareset={currentset} checkin={this.checkin} checkout={this.checkout} key={currentset._id}/>;
  //     })
  //   }


//   checkin(id) {
//     axios.post('hardwaresets/checkin/' + id)
//         .then(response => console.log(response.data))
//         .catch((error) => {
//             console.log(error);
//         })
//     window.location.reload();
//   }

//   checkout(id) {
//     axios.post('hardwaresets/checkout/' + id)
//         .then(response => console.log(response.data))
//         .catch((error) => {
//             console.log(error);
//         })
//     window.location.reload();
//   }


  render() {
    return (
      <div>
        <Table striped bordered hover variant="dark">
          <thead>
            <tr>
              <th>Hardware Set Name</th>
              <th>Capacity</th>
              <th>Available</th>
              <th>Request</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Set 1</td>
              <td>100</td>
              <td>100</td>
              <td>
                <input></input>
              </td>
              <td>
                <Button>Check in</Button>
              </td>
              <td>
                <Button>Check out</Button>
              </td>
            </tr>
            <tr>
              <td>Set 2</td>
              <td>100</td>
              <td>100</td>
              <td>
                <input></input>
              </td>
              <td>
                <Button>Check in</Button>
              </td>
              <td>
                <Button>Check out</Button>
              </td>
            </tr>
            <tr>
              <td>Set 3</td>
              <td>100</td>
              <td>100</td>
              <td>
                <input></input>
              </td>
              <td>
                <Button>Check in</Button>
              </td>
              <td>
                <Button>Check out</Button>
              </td>
            </tr>

            {/* { this.fillTable() } */}
          </tbody>
        </Table>
        <Link to="/createProject">Create New Project</Link>
      </div>
    );
  }
}

export default Project;
