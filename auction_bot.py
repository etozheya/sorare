import time

from tg_bot.message import send_auction_message
from queries import eth, auctions, last_purchases, logs


def prices_from_purchases(latest_purchases):
    return [eth.wei_to_eth(float(p['owner']['price']))
            for p in latest_purchases
            if p != '0' and eth.wei_to_eth(float(p['owner']['price'])) != 0]


def run():
    cache = []
    while True:
        try:
            ending_auctions = auctions.get_ending_auctions(7)
            for ea in [e for e in ending_auctions if e['cards']]:
                print(logs.on_sale_auction(ea))
                best_bid = eth.wei_to_eth(float(ea['bestBid']['amount']))
                if 0.005 <= best_bid:
                    latest_purchases = \
                        last_purchases.get_purchase_info_for_auction(ea)
                    print(logs.previous_sales(latest_purchases))
                    if latest_purchases:
                        prices = prices_from_purchases(latest_purchases)
                        if prices:
                            avg_price = sum(prices) / len(prices)
                            print(logs.price(avg_price))
                            if (avg_price - best_bid) / best_bid > 0.05 and \
                                    (best_bid * 1.1) <= min(prices):
                                if logs.on_sale_auction(ea) not in cache:
                                    send_auction_message(
                                        logs.on_sale_auction_message(ea))
                                cache.append(logs.on_sale_auction(ea))
        except Exception:
            pass
        time.sleep(10)


run()
