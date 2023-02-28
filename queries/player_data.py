import requests

from queries.vars import JWT, grahpql_url


def get_player_data_by_slug(slug):
    query = '''
    query myQuery {
      player(slug:"%s") {
        activeInjuries {
          active
        }
        gameStats(last:20) {
          minsPlayed
          so5Score {
            score
          }
        }
      }
    }
    ''' % slug

    r = requests.post(
        grahpql_url,
        headers={'Authorization': f'Bearer {JWT}', 'JWT-AUD': 'myappname'},
        json={'query': query})

    return r.json()
