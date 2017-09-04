import React from 'react';
import {
  createFragmentContainer,
  graphql,
} from 'react-relay';
import colorContrast from 'font-color-contrast';

class Contact extends React.Component {
  renderNames() {
    const { names } = this.props.contact;
    if (!names.length) {
      return null
    }
    if (names.length === 1) {
      return (
        <div className="names">
          Name: {names[0].name}
        </div>
      )
    }
    return (
      <div className="names">
        Names:
        <ol className="contact-names">
          {names.map(({ category, name }) => (
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
    const { emails } = this.props.contact;
    if (!emails.length) {
      return null
    }
    const displayEmail = (email) => (
      <a href={`mailto:${email}`}>{email}</a>
    )
    if (emails.length === 1) {
      return (
        <div className="emails">
          Email: {displayEmail(emails[0].email)}
        </div>
      )
    }
    return (
      <div className="emails">
        Emails:
        <ol className="contact-emails">
          {emails.map(({ category, email }) => (
            <li key={category}>
              <span className="category">{category}</span>
              :{" "}
              <span className="email">{displayEmail(email)}</span>
            </li>
          ))}
        </ol>
      </div>
    )
  }
  renderPronouns() {
    const { pronounsList } = this.props.contact;
    if (!pronounsList.length) {
      return null
    }
    const displayPronouns = ({ subject, object, possessiveDeterminer }) => (
      `${subject}/${object}/${possessiveDeterminer}`
    )
    if (pronounsList.length === 1) {
      return (
        <div className="pronouns">
          Pronouns: {displayPronouns(pronounsList[0])}
        </div>
      )
    }
    return (
      <div className="pronouns">
        Pronouns:
        <ol className="contact-pronouns">
          {pronounsList.map(pronouns => (
            <li key={pronouns.id}>{displayPronouns(pronouns)}</li>
          ))}
        </ol>
      </div>
    )
  }
  renderTags() {
    const { tags } = this.props.contact;
    if (!tags.length) {
      return null
    }
    return (
      <div className="tags">
        Tags:
        <ol className="contact-tags">
          {tags.map(({ name, color, note }) => {
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
    const { contact } = this.props;
    return (
      <li key={contact.id}>
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
        id
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
