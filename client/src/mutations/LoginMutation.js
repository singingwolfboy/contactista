/* eslint-env browser */
import {
  commitMutation,
  graphql,
} from 'react-relay';

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
  password,
  refreshEnvironment
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
        const records = {
          "client:root": {
            viewer: {
              __id: response.login.viewer.id,
              username: response.login.viewer.username,
            }
          }
        }
        refreshEnvironment(records)
      }
    }
  );
}

export default {commit};
