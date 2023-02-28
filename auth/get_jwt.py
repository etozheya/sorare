import bcrypt
import requests

email = 'n_zhdankin@yahoo.com'
password = 'Zaloopa228.'
path = f'https://api.sorare.com/api/v1/users/{email}'
grahpql_url = 'https://api.sorare.com/graphql'

salt = requests.get(path).json()['salt']
print(f'salt is {salt}')

hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8'))
print(f'hashed password is {hashed_password}')

query = """
mutation SignInMutation($input: signInInput!) {
  signIn(input: $input) {
    currentUser {
      slug
      jwtToken(aud: "myappname") {
        token
        expiredAt
      }
    }
    errors {
      message
    }
  }
}
"""

variables = {
    'input': {'email': email, 'password': hashed_password.decode('utf-8')}}
r = requests.post(grahpql_url, json={'query': query, 'variables': variables})
jwt = r.json()['data']['signIn']['currentUser']['jwtToken']['token']

print(f'JWT is {jwt}')
