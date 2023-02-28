import requests

from queries.vars import JWT, grahpql_url


def get_latest_offers(offers_count):
    query = '''
    query myQuery {
      transferMarket {
        singleSaleOffers(first:%s) {
          nodes {
            blockchainId
            createdAt
            card {
              rarity
              season {
                startYear
              }
              player {
                slug
                firstName
                lastName
              }
            }
            price
          }
        }
      }
    }
    ''' % offers_count

    r = requests.post(
        grahpql_url,
        headers={'Authorization': f'Bearer {JWT}', 'JWT-AUD': 'myappname'},
        json={'query': query})

    return r.json()['data']['transferMarket']['singleSaleOffers']['nodes']
