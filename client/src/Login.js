import LoginMutation from './mutations/LoginMutation'

import React from 'react';
import {
  createFragmentContainer,
  graphql,
} from 'react-relay';

class Login extends React.Component {
  handleSubmit = (event) => {
    event.preventDefault()
    LoginMutation.commit(
      this.props.relay.environment,
      event.target.username.value,
      event.target.password.value,
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
