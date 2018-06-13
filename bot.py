#! /usr/bin/env python3

import argparse
import logging
import re

from telegram.ext import Updater, MessageHandler, Filters

import config


def resolve_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )


REDDIT_REGEX = re.compile(r'(?:[^/]\b|\B/)r/(\w+)')

REDDIT_URL = 'https://www.reddit.com/r/{}/'


def get_link(bot, update):
    found = REDDIT_REGEX.findall(update.message.text)

    urls = [REDDIT_URL.format(match) for match in found]

    if len(urls) > 0:
        update.message.reply_text('\n'.join(urls), quote=True)


if __name__ == '__main__':
    resolve_args()

    updater = Updater(token=config.BOT_TOKEN)

    dispatcher = updater.dispatcher

    print(updater.bot.get_me())

    dispatcher.add_handler(MessageHandler(Filters.all, get_link,
                                          edited_updates=True))

    updater.start_webhook(
        listen='0.0.0.0', port=config.PORT, url_path=config.BOT_TOKEN)

    updater.bot.set_webhook(config.WEBHOOK_URL)

    # updater.start_polling()

    updater.idle()
