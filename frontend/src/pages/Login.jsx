import React from "react";
import axios from "axios";
import { withRouter } from "react-router-dom";
import { Container, Row, Col, Form, Button } from "react-bootstrap";
import "../styles/login.css";

class Login extends React.Component {
  state = {
    email: "",
    password: ""
  };

  componentDidMount = () => {
    if (localStorage.getItem("token") !== null) {
      this.props.history.push("/dashboard");
    }
  };

  /**
   * Send request (email and password) to backend,
   * then get token for login
   */
  handleLogin = () => {
    const request = {
      method: "post",
      url: "http://localhost:5000/auth/login",
      data: {
        email: this.state.email,
        password: this.state.password
      },
      headers: {
        "Content-Type": "application/json"
      }
    };
    axios(request)
      .then(response => {
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("email", this.state.email);
        alert("Berhasil login!");
        this.props.history.push("/dashboard");
      })
      .catch(() => alert("Email atau password anda salah!"));
  };

  render() {
    return (
      <Container className="login">
        <Row>
          <Col md="4"></Col>
          <Col md="4">
            <Form onSubmit={event => event.preventDefault()}>
              <Form.Group>
                <Form.Control
                  type="email"
                  placeholder="Email"
                  onChange={event =>
                    this.setState({ email: event.target.value })
                  }
                />
              </Form.Group>
              <Form.Group>
                <Form.Control
                  type="password"
                  placeholder="Password"
                  onChange={event =>
                    this.setState({ password: event.target.value })
                  }
                />
              </Form.Group>
              <Button type="submit" onClick={() => this.handleLogin()}>
                Login
              </Button>
            </Form>
          </Col>
        </Row>
      </Container>
    );
  }
}

export default withRouter(Login);
