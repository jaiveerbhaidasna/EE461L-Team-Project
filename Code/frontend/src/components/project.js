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
        onClick={() => {
          props.checkin(props.request, props.hardwareset.name);
        }}
      >
        Check in
      </Button>
    </td>
    <td>
      <Button
        onClick={() => {
          props.checkout(props.request, props.hardwareset.name);
        }}
      >
        Check out
      </Button>
    </td>
  </tr>
);



class Project extends Component {
  constructor(props){
  super(props);

  this.checkin = this.checkin.bind(this);
  this.checkout = this.checkout.bind(this);

  this.state = {
    hardwaresets:[],
    request: 0,
    projectid: ""
  };
}

  componentDidMount() {
    var url = window.location.pathname.substring(
      window.location.pathname.lastIndexOf("/" + 1)
    );
    url = url.substring(1);
    console.log(url);
    var flag = 0
    var new_url = ""

    for(var i = 0; i < url.length; i++){
      if(flag === 1){
        new_url += url.charAt(i)
      }
      if(url.charAt(i) === '/'){
        flag = 1
      }
    }

    console.log(new_url)

    this.setState({
      projectid : new_url
    });

    axios
      .get("https://dry-lowlands-32590.herokuapp.com/" + url, {withCredentials: true})
      .then((response) => {
        var i = 0
        var data = []

        for(i; i<response.data.length; i++){
          console.log(response.data[i])
          var setname = ""
          var setcapacity = ""
          var setavailable = ""
          var str = response.data[i]
          var flag = 0
          for(var j=0; j<str.length; j++){
            if(str.charAt(j) === '\''){
              flag++
            }
            if(flag === 1){
              setname += str.charAt(j)
            }
            if(flag === 3){
              setcapacity += str.charAt(j)
            }
            if(flag === 5){
              setavailable += str.charAt(j)
            }
          }
          setname = setname.substring(1)
          setcapacity = setcapacity.substring(1)
          setavailable = setavailable.substring(1)
          
          console.log(parseInt(setcapacity))

          const hwset = {
             name:setname,
             capacity:(setcapacity),
             available:(setavailable)
           }
          data.push(hwset)

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
          request = {this.state.request}
        />
      );
    });
  }

  checkin(num, name1) {
    console.log(num)
    const requestinfo = {
      name: name1,
      request: num,
    };

    console.log(this.state.projectid)

    axios
      .post("https://dry-lowlands-32590.herokuapp.com/project/checkin/" + this.state.projectid, requestinfo)
      .then((response) => console.log(response.data))
      .catch((error) => {
        console.log(error);
      });
    //window.location.reload(true);
  }

  checkout(num, name1) {
    const requestinfo = {
      name: name1,
      request: num,
    };

    axios
      .post("https://dry-lowlands-32590.herokuapp.com/project/checkout/" + this.state.projectid, requestinfo)
      .then((response) => console.log(response.data))
      .catch((error) => {
        console.log(error);
      });
    //window.location.reload(true);
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
