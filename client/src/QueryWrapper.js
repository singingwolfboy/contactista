import React from 'react'
import {
  QueryRenderer,
  graphql,
} from 'react-relay';
import {
  Environment,
  Network,
  RecordSource,
  Store,
} from 'relay-runtime';
import App from './App'


const fetchQuery = (operation, variables) => {
  const headers = {
    'Content-Type': 'application/json',
  }
  const token = sessionStorage.getItem('token')
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  return fetch('/graphql', {
    method: 'POST',
    headers,
    body: JSON.stringify({
      query: operation.text,
      variables,
    }),
  }).then(response => {
    return response.json();
  });
}

const makeEnvironment = (records = undefined) => (
  new Environment({
    network: Network.create(fetchQuery),
    store: new Store(new RecordSource(records)),
  })
)

export default class QueryWrapper extends React.Component {
  state = {
    environment: makeEnvironment()
  }
  refreshEnvironment = () => {
    this.setState({environment: makeEnvironment()})
  }
  render() {
    return (
      <QueryRenderer
        environment={this.state.environment}
        query={graphql`
          query QueryWrapperQuery {
            viewer {
              ...App_viewer
            }
          }
        `}
        variables={{}}
        render={({error, props}) => {
          if (props) {
            return <App viewer={props.viewer}
                        refreshEnvironment={this.refreshEnvironment}
                   />;
          } else {
            return <div>Loading</div>;
          }
        }}
      />
    )
  }
}

