import React from "react";
import { withRouter } from "react-router-dom";

class NotFound extends React.Component {
  componentDidMount = () => {
    this.props.history.push("/");
  };

  render() {
    return <React.Fragment></React.Fragment>;
  }
}

export default withRouter(NotFound);
