import logging
import pprint

import emoji
import flag

from utils import getMainKeyboard
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from emoji import emojize
import requests
import settings


# import handlers

# BOT_NAME = BudgetFinancialMoney_Bot

logging.basicConfig(filename="bot.log", level=logging.INFO)


# PROXY = {"proxy_url": settings.PROXY_URL,
#          "urllib3_proxy_kwargs": {"username": settings.PROXY_USERNAME, "password": settings.PROXY_PASSWORD}}
#

# http://ip-api.com/json/24.48.0.1

def main():
    mybot = Updater(settings.API_KEY, use_context=True)  # , request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", hello))
    dp.add_handler(MessageHandler(Filters.regex('^(Проверить IP)$'), checkIP))
    dp.add_handler(MessageHandler(Filters.regex(settings.IP_VALIDATION), getIPinfo))
    logging.info("Bot successfully started")

    mybot.start_polling()
    mybot.idle()


def hello(update, context):
    userName = update.effective_user.first_name
    update.message.reply_text(f"Здарвствуй, {userName}!", reply_markup=getMainKeyboard())


def checkIP(update, context):
    update.message.reply_text(f"Введите IP для проверки!")


def getIPinfo(update, context):
    text = update.message.text
    update.message.reply_text(f"Запрос IP: {text}!")

    response = requests.get(f"http://ip-api.com/json/{text}")
    response = response.json()
    # print(response)
    flag_code = f":{response.get('countryCode').lower()}:"

    # flag_emoji = emoji.emojize(flag_code, variant="emoji_type")

    msg = f"""Информация:\n
*Статус:* {response.get('status')}
*Страна:* {flag.flagize(flag_code, subregions=True)}{response.get('country')}
*Код страны:* {response.get('countryCode')}
*Регион:* {response.get('regionName')}
*Код региона:* {response.get('region')}
*Город:* {response.get('city')}
*Индекс:* {response.get('zip')}
*Широта:* {response.get('lat')}
*Долгота:* {response.get('lon')}
*Врем. пояс:* {response.get('timezone')}
*Провайдер:* {response.get('isp')}
*Организация:* {response.get('org')}
*Авт-ая система:* {response.get('as')}"""

    update.message.reply_text(msg, parse_mode="Markdown")


if __name__ == "__main__":
    main()
