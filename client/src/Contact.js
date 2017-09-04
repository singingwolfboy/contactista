import React from 'react';
import {
  createFragmentContainer,
  graphql,
} from 'react-relay';
import colorContrast from 'font-color-contrast';

class Contact extends React.Component {
  renderNames() {
    const { contact } = this.props;
    if (!contact.names.length) {
      return null
    }
    return (
      <div className="names">
        Names:
        <ol className="contact-names">
          {contact.names.map(({ category, name }) => (
            <li key={category}>
              <span className="category">{category}</span>
              :{" "}
              <span className="name">{name}</span>
            </li>
          ))}
        </ol>
      </div>
    )
  }
  renderEmails() {
    const { contact } = this.props;
    if (!contact.emails.length) {
      return null
    }
    return (
      <div className="emails">
        Emails:
        <ol className="contact-emails">
          {contact.emails.map(({ category, email }) => (
            <li key={category}>
              <span className="category">{category}</span>
              :{" "}
              <span className="email">{email}</span>
            </li>
          ))}
        </ol>
      </div>
    )
  }
  renderPronouns() {
    const { contact } = this.props;
    if (!contact.pronounsList.length) {
      return null
    }
    const pronounsListItem = ({ subject, object, possessiveDeterminer }) => (
      <li key={subject}>{subject}/{object}/{possessiveDeterminer}</li>
    )
    return (
      <div className="pronouns">
        Pronouns:
        <ol className="contact-pronouns">
          {contact.pronounsList.map(pronounsListItem)}
        </ol>
      </div>
    )
  }
  renderTags() {
    const { contact } = this.props;
    if (!contact.tags.length) {
      return null
    }
    return (
      <div className="tags">
        Tags:
        <ol className="contact-tags">
          {contact.tags.map(({ name, color, note }) => {
            const style = {
              backgroundColor: color,
              color: colorContrast(color)
            }
            let noteEl = null
            if (note) {
              noteEl = <span className="note">{note}</span>
            }
            return (
              <li key={name}>
                <span className="name" style={style}>{name}</span>
                {noteEl}
              </li>
            )
          })}
        </ol>
      </div>
    )
  }
  renderNote() {
    const { note, noteFormat } = this.props.contact;
    if (!note) {
      return null
    }
    if (noteFormat === "markdown") {
      const Remarkable = require('remarkable')
      const md = new Remarkable('commonmark');
      const html = {__html: md.render(note)}
      return (
        <div className="note" dangerouslySetInnerHTML={html} />
      )
    }
    return (
      <div className="note">{note}</div>
    )
  }
  render() {
    return (
      <li>
        {this.renderNames()}
        {this.renderPronouns()}
        {this.renderEmails()}
        {this.renderTags()}
        {this.renderNote()}
      </li>
    );
  }
}

export default createFragmentContainer(Contact, {
  contact: graphql`
    fragment Contact_contact on Contact {
      names {
        category
        name
      }
      emails {
        category
        email
      }
      tags {
        name
        color
        note
      }
      pronounsList {
        subject
        object
        possessiveDeterminer
      }
      note
      noteFormat
    }
  `,
  viewer: graphql`
    fragment Contact_viewer on User {
      id
      username
    }
  `,
});
