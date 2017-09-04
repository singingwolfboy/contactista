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
    // we *should* get `totalCount` from the GraphQL query,
    // but graphene doesn't implement that yet. The edge length will work,
    // as long as we don't paginate.
    const totalCount = this.props.viewer.contacts.edges.length
    return (
      <div>
        <p>You have {totalCount} contacts.</p>
        <ul className="contact-list">
          {this.renderContacts()}
        </ul>
      </div>
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
