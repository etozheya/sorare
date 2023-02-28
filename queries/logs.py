from queries import eth


def on_sale_offer(offer):
    return f'{offer["card"]["rarity"]}' \
           f' {offer["card"]["season"]["startYear"]} card of' \
           f' {offer["card"]["player"]["firstName"]}' \
           f' {offer["card"]["player"]["lastName"]} is on sale for the price' \
           f' of {eth.wei_to_eth(float(offer["price"]))} ETH.'


def on_sale_offer_message(offer):
    return f'{offer["card"]["rarity"]} ' \
           f' {offer["card"]["season"]["startYear"]} card of' \
           f' {offer["card"]["player"]["firstName"]}' \
           f' {offer["card"]["player"]["lastName"]} is on sale for the price' \
           f' of {eth.wei_to_eth(float(offer["price"]))} ETH.' \
           f'\nLink to offers: https://sorare.com/market/transfers'.title()


def on_sale_auction(auction):
    return f'{auction["cards"][0]["rarity"]} card of' \
           f' {auction["cards"][0]["player"]["firstName"]}' \
           f' {auction["cards"][0]["player"]["lastName"]}' \
           ' is on auction for the price of' \
           f' {eth.wei_to_eth(float(auction["bestBid"]["amount"]))} ETH.'


def on_sale_auction_message(auction):
    return f'{auction["cards"][0]["rarity"]}' \
           f' {auction["cards"][0]["season"]["startYear"]} card of' \
           f' {auction["cards"][0]["player"]["firstName"]}' \
           f' {auction["cards"][0]["player"]["lastName"]}' \
           ' is on auction for the price of' \
           f' {eth.wei_to_eth(float(auction["bestBid"]["amount"]))} ETH.' \
           f'\nLink to auctions: https://sorare.com/market/new-signings'.title()


def previous_sales(purchases):
    if not purchases:
        return 'This card has not been bought in the last 72 hours.'
    if len(purchases) == 1:
        return 'This card has been bought once in the last 72 hours.'
    return f'This card has been bought {len(purchases)} time(s) ' \
        'in the last 72 hours.'


def price(avg_price):
    return f'With the average price of {avg_price}.'
