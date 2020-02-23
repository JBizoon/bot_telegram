#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from telegram.ext import Updater,  CommandHandler, MessageHandler, Filters
import urllib
import json
# Log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text(
        'Usage: text [crypto_name] to return data from coinmarketcap.com')


def help(update, context):
    update.message.reply_text('Help')


def query(update, context):
    path = (update.message.text)
    urlData = "https://api.coinmarketcap.com/v1/ticker/" + path.lower()
    data, data2 = getResponse(urlData)
    update.message.reply_text(data + data2)


def getResponse(url):
    try:
        response = urllib.urlopen(url)
        jsonData = json.loads(response.read())
        data = jsonData[0]["name"] + '\n' + 'USD Price:' + '$' + jsonData[0]["price_usd"] + '\n' + \
            'Volume USD (24h):' + '$' + jsonData[0]["24h_volume_usd"] + '\n' + \
            'Percent change (1h):' + \
            jsonData[0]["percent_change_1h"] + '%' + '\n'
        data2 = 'Percent change (24):' + jsonData[0]["percent_change_24h"] + '%' + \
            '\n' + 'Percent change (7d):' + \
            jsonData[0]["percent_change_7d"] + '%'
    except:
        data = 'Wrong name or currency not supported'
        data2 = ' '
    return data, data2


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Token
    updater = Updater("TOKEN", use_context=True)
    dp = updater.dispatcher
    # commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, query))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    updater.idle()
