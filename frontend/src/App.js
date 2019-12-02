import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Table } from 'reactstrap';
import axios from 'axios';
const FILE_SERVICE_URL = 'http://localhost:8000/celery/files';


function App() {
  const [data, setData] = useState({ files: [], isFetching: false });

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        setData({ files: data.files, isFetching: true });
        const response = await axios.get(FILE_SERVICE_URL);
        setData({ files: response.data, isFetching: false });
      } catch (e) {
        console.log(e);
        setData({ files: data.files, isFetching: false });
      }
    };
    fetchFiles();
  }, []);

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
              {data.files.map(f => (
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

export default App;