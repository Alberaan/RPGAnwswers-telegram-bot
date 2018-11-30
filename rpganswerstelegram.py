import os
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import argparse
from configparser import SafeConfigParser
from flask import Flask, request
from botlogic import *


def sendData(msg, bot, data):
    if bot != None:
        content_type, chat_type, chat_id = telepot.glance(msg)
        bot.sendMessage(chat_id, data)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

#def handle(msg):
def on_chat_message(msg):

    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'text' :
        response = processCommand(msg["text"])

    else:
        response = "error"

    sendData(msg, bot, response)

def on_callback_query(msg):
    pass

def on_inline_query(msg):
    pass

def on_chosen_inline_result(msg):
    pass

# Main starts here
token = str(os.environ["telegram_token"])
bot = telepot.Bot(token) # Bot is created from the telepot class
app = Flask(__name__)
webhook = OrderedWebhook(bot, {'chat': on_chat_message,
                               'callback_query': on_callback_query,
                               'inline_query': on_inline_query,
                               'chosen_inline_result': on_chosen_inline_result})

@app.route('/', methods=['GET', 'POST'])
def pass_update():
    webhook.feed(request.data)
    return 'OK'

if __name__ == '__main__':
    app.run()
    printf("Executed the run")
    
if __name__ != '__main__':
    print("Executing the stuff")
    print("After running app")
    try:
        print("Inside try")
        bot.setWebhook(URL)
        print("After setting webhook")
    # Sometimes it would raise this error, but webhook still set successfully.
    except telepot.exception.TooManyRequestsError:
        pass

webhook.run_as_thread()
