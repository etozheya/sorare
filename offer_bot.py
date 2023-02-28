import time

from tg_bot.message import send_offer_message
from queries import eth, offers, last_purchases, logs


def prices_from_purchases(latest_purchases):
    return [eth.wei_to_eth(float(p['owner']['price']))
            for p in latest_purchases
            if p != '0' and eth.wei_to_eth(float(p['owner']['price'])) != 0]


def run():
    cache = []
    while True:
        try:
            latest_offers = offers.get_latest_offers(7)
            for lo in [lo for lo in latest_offers if lo['card']]:
                print(logs.on_sale_offer(lo))
                price = eth.wei_to_eth(float(lo['price']))
                if 0.005 <= price:
                    latest_purchases = \
                        last_purchases.get_purchase_info_for_offer(lo)
                    print(logs.previous_sales(latest_purchases))
                    prices = prices_from_purchases(latest_purchases)
                    if prices:
                        avg_price = sum(prices) / len(prices)
                        print(logs.price(avg_price))
                        if (avg_price - price) / price > 0.05 \
                                and price <= min(prices):
                            if logs.on_sale_offer(lo) not in cache:
                                send_offer_message(
                                    logs.on_sale_offer_message(lo))
                            cache.append(logs.on_sale_offer(lo))
        except Exception:
            pass
        time.sleep(10)


run()
