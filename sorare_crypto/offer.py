import requests

from queries.vars import starkware_private_key, grahpql_url, JWT


def creating_offer(blockchain_id):
    prepare_accept_offer_input = {'dealId': blockchain_id}
    query = """
    mutation PrepareAcceptOffer($input: prepareAcceptOfferInput!) {
      prepareAcceptOffer(input: $input) {
        limitOrders {
          amountBuy
          amountSell
          expirationTimestamp
          feeInfo {
            feeLimit
            tokenId
            sourceVaultId
          }
          id
          nonce
          tokenBuy
          tokenSell
          vaultIdBuy
          vaultIdSell
        }
        errors {
          message
        }
      }
    }
    """
    variables = {'input': prepare_accept_offer_input}
    r = requests.post(
        grahpql_url, json={'query': query, 'variables': variables},
        headers={'Authorization': f'Bearer {JWT}', 'JWT-AUD': 'myappname'})

    return r.json()


print(creating_offer('3125034716246859191015702151633528522032'))
