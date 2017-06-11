#! /usr/bin/env python3

import argparse
import logging
import re

from telegram.ext import Updater, MessageHandler, Filters
from emoji import emojize

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


REDDIT_REGEX = re.compile(r'/r/([a-zA-Z0-9_]+)')

REDDIT_URL = 'https://www.reddit.com/r/{}/'


def get_link(bot, update):
    print(update.message.text)
    found = REDDIT_REGEX.findall(update.message.text)

    urls = (REDDIT_URL.format(match) for match in found)

    print(urls)

    update.message.reply_text('\n'.join(urls), quote=True)


def help(bot, update):
    return emojize('Turns "/r/subreddit" into'
                   '"https://www.reddit.com/r/subreddit/".\n\n'
                   'Made with :heart: by @caiopo')


if __name__ == '__main__':
    resolve_args()

    updater = Updater(token=config.BOT_TOKEN)

    dispatcher = updater.dispatcher
    job_queue = updater.job_queue

    print(updater.bot.getMe())

    dispatcher.add_handler(MessageHandler(Filters.all, get_link))

    updater.start_webhook(
        listen='0.0.0.0', port=config.PORT, url_path=config.BOT_TOKEN,
        webhook_url=config.WEBHOOK_URL)

    updater.idle()
