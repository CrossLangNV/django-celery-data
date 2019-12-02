import React, { Component } from 'react';
import { Container, Row, Col, Table } from 'reactstrap';

class App extends Component {
  state = {
    files: []
  };

  async componentDidMount() {
    try {
      const res = await fetch('http://localhost:8000/celery/files');
      const files = await res.json();
      this.setState({
        files
      });
    } catch (e) {
      console.log(e);
    }
  }

  render() {
    return (
      <Container>
        <Row>
          <Col>
            <h1>Files</h1>
          </Col>
        </Row>
        <Row>
          <Col>
            <Table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Filename</th>
                  <th>Number of lines</th>
                </tr>
              </thead>
              <tbody>
                {this.state.files.map(f => (
                  <tr>
                    <td>{f.id}</td>
                    <td>{f.name}</td>
                    <td>{f.line_count}</td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </Col>
        </Row>
      </Container>
    );
  }
}

export default App;