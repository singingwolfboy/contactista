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
        <label>Username
          <input name="username" type="text" />
        </label>
        <label>Password
          <input name="password" type="password" />
        </label>
        <input type="submit" />
      </form>
    );
  }
}

export default createFragmentContainer(Login, {});
