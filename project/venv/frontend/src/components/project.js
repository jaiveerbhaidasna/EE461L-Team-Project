import { Component } from "react";
import { Table, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import axios from "axios";

const HardwareSet = (props) => (
  <tr>
    <td>{props.hardwareset.name}</td>
    <td>{props.hardwareset.capacity}</td>
    <td>{props.hardwareset.available}</td>
    <td>
      <Button
        href="."
        onClick={() => {
          props.checkin(props.hardwareset.name);
        }}
      >
        Check in
      </Button>
    </td>
    <td>
      <Button
        href="."
        onClick={() => {
          props.checkout(props.hardwareset.name);
        }}
      >
        Check out
      </Button>
    </td>
  </tr>
);

class Project extends Component {
  state = {
    hardwaresets: [
      // {
      //   name: 'Hardware Set 1',
      //   capacity: 100,
      //   available: 100
      // },
      // {
      //   name: 'Hardware Set 2',
      //   capacity: 100,
      //   available: 100
      // }
    ],
    requests: 0,
  };

  componentDidMount() {
    var url = window.location.pathname.substring(
      window.location.pathname.lastIndexOf("/" + 1)
    );
    url = url.substring(1);
    console.log(url);

    axios
      .get("http://localhost:5000/" + url)
      .then((response) => {
        var i = 0
        var data = []

        for(i; i<response.data.length; i++){
          console.log(response.data[i])
          var mystring = ""
          var str = response.data[i]
          var flag = 0
          for(var j=0; j<str.length; j++){
            if(str.charAt(j) === '\''){
              flag++
            }
            if(flag === 1){
              mystring += str.charAt(j)
            }
          }
          mystring += "\'"
           const hwset = {
             name:mystring,
             capacity:0,
             available:0
           }
          data.push(hwset)
          console.log(mystring)

        }
        this.setState({
          hardwaresets: (data)
        });
      })
      .catch((error) => {
        console.log(error);
      });
  }

  fillTable() {
    return this.state.hardwaresets.map((currentset) => {
      return (
        <HardwareSet
          hardwareset={currentset}
          checkin={this.checkin}
          checkout={this.checkout}
          key={currentset._id}
        />
      );
    });
  }

  checkin(name1) {
    const requestinfo = {
      name: name1,
      request: this.state.request,
    };

    axios
      .post("http://localhost:5000/project/checkin/", requestinfo)
      .then((response) => console.log(response.data))
      .catch((error) => {
        console.log(error);
      });
    window.location.reload();
  }

  checkout(name1) {
    const requestinfo = {
      name: name1,
      request: this.state.request,
    };

    axios
      .post("http://localhost:5000/project/checkout/", requestinfo)
      .then((response) => console.log(response.data))
      .catch((error) => {
        console.log(error);
      });
    window.location.reload();
  }

  handleChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  render() {
    return (
      <div>
        <h1 className="project">{this.state.name}</h1>
        <Table
          style={{ color: "yellow" }}
          striped
          bordered
          hover
          variant="dark"
        >
          <thead>
            <tr>
              <th>Hardware Set Name</th>
              <th>Capacity</th>
              <th>Available</th>
              <th>
                <input
                  type="number"
                  name="request"
                  placeholder="Number"
                  onChange={this.handleChange}
                ></input>
              </th>
            </tr>
          </thead>
          <tbody>{this.fillTable()}</tbody>
        </Table>
        <Link id="newproject" to="..">
          Log out of project
        </Link>
      </div>
    );
  }
}

export default Project;
