import React from 'react';
import {
  createFragmentContainer,
  graphql,
} from 'react-relay';

class ContactBookSidebarItem extends React.Component {
  render() {
    const { contact } = this.props
    return <li>{contact.name}</li>
  }
}

export default createFragmentContainer(ContactBookSidebarItem, {
  contact: graphql`
    fragment ContactBookSidebarItem_contact on Contact {
      name
    }
  `,
});
