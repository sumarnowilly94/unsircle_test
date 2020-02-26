import React from "react";
import { withRouter } from "react-router-dom";
import { Container, Row, Col, Button } from "react-bootstrap";
import "../styles/dashboard.css";

class Dashboard extends React.Component {
  componentDidMount = () => {
    if (localStorage.getItem("token") === null) {
      this.props.history.push("/");
    }
  };

  /**
   * Handle logout action by remove token and email from local storage
   */
  handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("email");
    alert("Berhasil logout!");
    this.props.history.push("/");
  };

  render() {
    return (
      <Container className="dashboard">
        <Row>
          <Col md="3"></Col>
          <Col md="6" className="dashboard-center">
            <h6>Selamat Datang {localStorage.getItem("email")}</h6>
            <Button variant="danger" onClick={() => this.handleLogout()}>
              Logout
            </Button>
          </Col>
        </Row>
      </Container>
    );
  }
}

export default withRouter(Dashboard);
