import ContactList from './ContactList';
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
      body = <ContactList viewer={viewer} />
    } else {
      body = <Login refreshEnvironment={refreshEnvironment} />
    }
    return (
      <div>
        <h1>Bradley Contacts</h1>
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
      ...ContactList_viewer,
    }
  `,
});
