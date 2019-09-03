from telegram import ParseMode, ReplyKeyboardMarkup, ChatAction, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler, \
    ConversationHandler, RegexHandler
import logging, os, sys, re
from functools import wraps

# logger
logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# global variable
mode = os.environ['mode']
TOKEN = os.environ['TOKEN']
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# options to run
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("Error, Ensure Environment Variable is set.")
    sys.exit(1)


def get_name(user):
    try:
        name = user.first_name
    except (NameError, AttributeError):
        try:
            name = user.username
        except (NameError, AttributeError):
            logger.info("No Username? Not possible.")
            return ""
    return name


def shut_up(update, context):
    chat_id = update.message.chat_id
    name = get_name(update.message.from_user)
    name = name.upper()
    reply = "SHUT THE FUCK UP LA " + name + "!"
    update.message.reply_text(reply)


def sorry(update, context):
    reply = "You sure you sorry anot? Or is it cause you stupid?"
    update.message.reply_text(reply)


def yeet(update, context):
    reply = "I'll YEET your Milo"
    update.message.reply_text(reply)


def main():
    dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'say.*real', re.IGNORECASE)), shut_up))
    dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'sorry', re.IGNORECASE)), sorry))
    dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'yeet', re.IGNORECASE)), yeet))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
