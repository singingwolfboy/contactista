import React from 'react';
import {
  createFragmentContainer,
  graphql,
} from 'react-relay';

class Contact extends React.Component {
  render() {
    const { contact } = this.props.contact;
    return (
      <li>{contact.name}</li>
    );
  }
}

export default createFragmentContainer(Contact, {
  contact: graphql`
    fragment Contact_contact on Contact {
      name
    }
  `,
  viewer: graphql`
    fragment Contact_viewer on User {
      id
      username
    }
  `,
});
