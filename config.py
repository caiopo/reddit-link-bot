from os import environ

# the token you get from botfather
BOT_TOKEN = environ['BOT_TOKEN']

APP_NAME = environ['APP_NAME']

PORT = int(environ.get('PORT', 5000))

WEBHOOK_URL = 'https://' + APP_NAME + '.herokuapp.com/' + BOT_TOKEN
