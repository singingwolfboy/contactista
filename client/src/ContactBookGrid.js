import ContactBookSidebarItem from './ContactBookSidebarItem';
import Contact from './Contact';

import React from 'react';
import {
  createFragmentContainer,
  graphql,
} from 'react-relay';

class ContactBookGrid extends React.Component {
  renderSidebar() {
    const className = "contact-sidebar col-md-4"
    const edges = this.props.viewer.contacts.edges
    if (!edges) {
      return (
        <div className={className}>
          <span className="text-center">
            No contacts
          </span>
        </div>
      )
    }
    const items = edges.map(edge =>
      <ContactBookSidebarItem
        key={edge.node.id}
        contact={edge.node}
      />
    )
    return (
      <ul className={`list-unstyled ${className}`}>
        {items}
      </ul>
    )
  }
  renderContact() {
    const className = "contact-shown col-md-8"
    const numContacts = this.props.viewer.contacts.totalCount
    if (numContacts === 0) {
      return (
        <div className={`${className} text-center`}>
          You have no contacts. Would you like to add one?
        </div>
      )
    }
    const contact = this.props.viewer.contacts.edges[0].node
    if (!contact) {
      return (
        <div className={`${className} text-center`}>
          Select a contact
        </div>
      )
    }
    return (
      <div className={className}>
        <Contact contact={contact} />
      </div>
    )
  }
  render() {
    return (
      <div className="container-fluid">
        <div className="row">
          {this.renderSidebar()}
          {this.renderContact()}
        </div>
      </div>
    );
  }
}

export default createFragmentContainer(ContactBookGrid, {
  viewer: graphql`
    fragment ContactBookGrid_viewer on User {
      contacts {
        totalCount
        edges {
          node {
            id,
            ...ContactBookSidebarItem_contact,
            ...Contact_contact,
          },
        },
      },
      id,
    }
  `,
});
