#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from telegram.ext import Updater,  CommandHandler, MessageHandler, Filters
import urllib
import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Send mail via telegram')


def help(update, context):
    update.message.reply_text('Help')

# hardcode
def push(from_addr='from_addr', to_addr_list, message,
         login='login', password='password',
         smtpserver='[smtpserver]:[port]'):
    header = 'From: %s' % from_addr
    header += 'To: %s' % ','.join(to_addr_list)
    subjectmessage = header + message
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login, password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()


def query(update, context):
    update.message.reply_text("Email:")
    part1 = (update.message.text)
    update.message.reply_text("Text:")
    part2 = (update.message.text)
    push(to_addr_list=[part1], message=[part2])


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater("Token", use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, query))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    # CTRL - C
    updater.idle()


if __name__ == '__main__':
    main()
