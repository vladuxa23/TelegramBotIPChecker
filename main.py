import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings
# import handlers

# BOT_NAME = BudgetFinancialMoney_Bot

logging.basicConfig(filename="bot.log", level=logging.INFO)

# PROXY = {"proxy_url": settings.PROXY_URL,
#          "urllib3_proxy_kwargs": {"username": settings.PROXY_USERNAME, "password": settings.PROXY_PASSWORD}}
#

# http://ip-api.com/json/24.48.0.1

def main():
    mybot = Updater(settings.API_KEY, use_context=True)#, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", hello))

    logging.info("Bot successfully started")

    mybot.start_polling()
    mybot.idle()


def hello(update, context):
    userName = update.effective_user.first_name
    update.message.reply_text(f"Здарвствуй, {userName}!")

if __name__ == "__main__":
    main()
