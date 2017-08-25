import ContactList from './ContactList';

import React from 'react';
import {
  createFragmentContainer,
  graphql,
} from 'react-relay';

class App extends React.Component {
  render() {
    const { viewer } = this.props;
    return (
      <div>
        <h1>Bradley Contacts</h1>
        <p>Username: {viewer.username}</p>
        <ContactList viewer={viewer} />
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
