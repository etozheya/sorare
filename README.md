# sorare-bots

## What is Sorare?

Sorare is a fantasy sport video game.  Sorare operates on Ethereum's 
underlying blockchain network in order to secure the ownership and 
distribution of cards. Each player card is represented 
as a non-fungible token (NFT) using the ERC-721 token standard on Ethereum.

## What is this script for?

Sorare issues the new cards by the auctions. The first script parses
auctions that are about to end, checks if the price is lower than the market.
If that's the case it sends the message to the Telegram channel.
The second script parses offers by the managers.

## How to use it?

* Firstly you need a JWT token, which can be acquired by the script `get_jwt.py`
* Put your JWT token into the `queries/vars.py` function
* Create a Telegram bot and a channel with the help of [this article](https://help.nethunt.com/en/articles/6253243-how-to-make-an-api-call-to-the-telegram-channel)
* Put the token and the channel ID into the `tg_bot/vars.py` function
* Run the `auction_bot.py` or `offer_bot.py` script
