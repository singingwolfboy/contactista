import LoginMutation from './mutations/LoginMutation'

import React from 'react';
import PropTypes from 'prop-types';
import { createFragmentContainer } from 'react-relay';

class Login extends React.Component {
  static propTypes = {
    refreshEnvironment: PropTypes.func.isRequired
  }
  handleSubmit = (event) => {
    event.preventDefault()
    LoginMutation.commit(
      this.props.relay.environment,
      event.target.username.value,
      event.target.password.value,
      this.props.refreshEnvironment,
    );
  }
  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <div className="form-group">
          <label>Username
            <input name="username" type="text" className="form-control" />
          </label>
        </div>
        <div className="form-group">
          <label>Password
            <input name="password" type="password" className="form-control" />
          </label>
        </div>
        <button type="submit" className="btn btn-primary">Login</button>
      </form>
    );
  }
}

export default createFragmentContainer(Login, {});
