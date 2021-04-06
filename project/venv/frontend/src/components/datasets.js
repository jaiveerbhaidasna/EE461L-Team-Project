import { Component } from "react";
import { Table } from "react-bootstrap";


class Datasets extends Component {


  render() {
    return (
      <div>
        <h1>Datasets</h1>
        <Table striped bordered hover variant="dark">
          <thead>
            <tr>
              <th>Dataset</th>
              <th>Description</th>
              <th>Download Links</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Abdominal and Direct Fetal ECG Database</td>
              <td>Multichannel fetal electrocardiogram recordings obtained from 5 different women in labor, between 38 and 41 weeks of gestation.</td>
              <td><a href='https://physionet.org/content/adfecgdb/1.0.0/'>Link to Download</a></td>
            </tr>
            <tr>
              <td>Apnea-ECG Database</td>
              <td>Seventy ECG signals with expert-labelled apnea annotations and machine-generated QRS annotations.</td>
              <td><a href='https://physionet.org/content/apnea-ecg/1.0.0/'>Link to Download</a></td>
            </tr>
            <tr>
              <td >CAP Sleep Database</td>
              <td>The CAP Sleep Database is a collection of 108 polysomnographic recordings registered at the Sleep Disorders Center of the Ospedale Maggiore of Parma, Italy. The waveforms (contained in the .edf files…</td>
              <td><a href='https://physionet.org/content/capslpdb/1.0.0/'>Link to Download</a></td>
            </tr>
          </tbody>
        </Table>
      </div>
    );
  }
}

export default Datasets;