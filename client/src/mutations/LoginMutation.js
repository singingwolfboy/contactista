/* eslint-env browser */
import {
  commitMutation,
  graphql,
} from 'react-relay';

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

const mutation = graphql`
  mutation LoginMutation(
    $input: LoginInput!
  ) {
    login(input:$input) {
      token
      viewer {
        id
        username
      }
    }
  }
`;

let tempID = 0;

function commit(
  environment,
  username,
  password
) {
  return commitMutation(
    environment,
    {
      mutation,
      variables: {
        input: {
          username,
          password,
          clientMutationId: tempID++,
        },
      },
      onCompleted: (response) => {
        sessionStorage.setItem('token', response.login.token)
        // need a way to reload the environment...
      }
    }
  );
}

export default {commit};
