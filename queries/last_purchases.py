import requests
from datetime import datetime, timedelta

from queries.vars import JWT, grahpql_url


def get_purchase_info_for_offer(offer):
    slug = offer['card']['player']['slug']
    rarity = offer['card']['rarity']
    date = (datetime.utcnow() - timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S")
    query = '''
    query myQuery {
      player(slug:"%s") {
        cards(last:100, rarities: %s, owned: true, ownedSinceAfter: "%s") {
          nodes {
            slug
            owner {
              price
            }
            ownerSince
          }
        }
      }
    }
    ''' % (slug, rarity, date)

    r = requests.post(
        grahpql_url,
        headers={'Authorization': f'Bearer {JWT}', 'JWT-AUD': 'myappname'},
        json={'query': query})

    return r.json()['data']['player']['cards']['nodes']


def get_purchase_info_for_auction(auction):
    slug = auction['cards'][0]['player']['slug']
    rarity = auction['cards'][0]['rarity']
    date = (datetime.utcnow() - timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S")
    query = '''
    query myQuery {
      player(slug:"%s") {
        cards(last:100, rarities: %s, owned: true, ownedSinceAfter: "%s") {
          nodes {
            slug
            owner {
              price
            }
            ownerSince
          }
        }
      }
    }
    ''' % (slug, rarity, date)

    r = requests.post(
        grahpql_url,
        headers={'Authorization': f'Bearer {JWT}', 'JWT-AUD': 'myappname'},
        json={'query': query})

    return r.json()['data']['player']['cards']['nodes']
