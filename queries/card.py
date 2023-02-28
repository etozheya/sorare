import requests

from vars import JWT, grahpql_url


def get_card_by_slug(slug):
    query = '''
    query myQuery {
      card(slug:"%s") {
        rarity
        latestEnglishAuction {
          bestBid {
            amount
          }
        }
        season {
          startYear
        }
        u23Eligible
        so5Scores(last:5) {
          score
        }
        player {
          firstName
          lastName
          averageScore(type: LAST_FIFTEEN_SO5_AVERAGE_SCORE)
        }
        positionTyped
        team {
          ... on Club {
            name
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


get_card_by_slug('ederson-santana-de-moraes-2022-unique-1')
