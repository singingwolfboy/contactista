import Contact from './Contact';

import React from 'react';
import {
  createFragmentContainer,
  graphql,
} from 'react-relay';

class ContactList extends React.Component {
  renderContacts() {
    return this.props.viewer.contacts.edges.map(edge =>
      <Contact
        key={edge.node.id}
        contact={edge.node}
        viewer={this.props.viewer}
      />
    );
  }
  render() {
    return (
      <ul className="contact-list">
        {this.renderContacts()}
      </ul>
    );
  }
}

export default createFragmentContainer(ContactList, {
  viewer: graphql`
    fragment ContactList_viewer on User {
      contacts {
        edges {
          node {
            id,
            ...Contact_contact,
          },
        },
      },
      id,
      ...Contact_viewer,
    }
  `,
});
