import './App.scss';
import ContactBookGrid from './ContactBookGrid';
import Login from './Login';

import React from 'react';
import {
  createFragmentContainer,
  graphql,
} from 'react-relay';

class App extends React.Component {
  render() {
    const { viewer, refreshEnvironment } = this.props;
    let body;
    if (viewer) {
      body = <ContactBookGrid viewer={viewer} />
    } else {
      body = <Login refreshEnvironment={refreshEnvironment} />
    }
    return (
      <div>
        <h1>Contactista</h1>
        {body}
      </div>
    );
  }
}

export default createFragmentContainer(App, {
  viewer: graphql`
    fragment App_viewer on User {
      id,
      username,
      ...ContactBookGrid_viewer,
    }
  `,
});
