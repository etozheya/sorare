import requests

from queries.vars import JWT, grahpql_url


def get_ending_auctions(auctions_count):
    query = """
    query myQuery {
      transferMarket {
        englishAuctions(first:%s) {
          nodes {
            bestBid {
              amount
            }
            endDate
            cards {
              rarity
              season {
                startYear
              }
              player {
                firstName
                lastName
                slug
              }
            }
          }
        }
      }
    }
    """ % auctions_count

    r = requests.post(
        grahpql_url,
        headers={'Authorization': f'Bearer {JWT}', 'JWT-AUD': 'myappname'},
        json={'query': query})

    return r.json()['data']['transferMarket']['englishAuctions']['nodes']
