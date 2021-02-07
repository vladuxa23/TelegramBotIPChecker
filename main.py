import flag
import utils
import emoji
import logging
import requests
import settings
# import handlers

from emoji import emojize
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# BOT_NAME = @IPchecker23Bot

logging.basicConfig(filename="bot.log", level=logging.INFO)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", hello))
    dp.add_handler(MessageHandler(Filters.regex('^(Проверить IP)$'), checkIP))
    dp.add_handler(MessageHandler(Filters.regex('^(О боте)$'), aboutBot))
    dp.add_handler(MessageHandler(Filters.regex(utils.IP_VALIDATION), getIPinfo))
    dp.add_handler(MessageHandler(Filters.text, brokenIP))
    logging.info("Bot successfully started")

    mybot.start_polling()
    mybot.idle()


def brokenIP(update, context):
    update.message.reply_text(f"IP-адрес не определён")


def hello(update, context):
    userName = update.effective_user.first_name
    update.message.reply_text(f"Здарвствуй, {userName}!", reply_markup=utils.getMainKeyboard())


def aboutBot(update, context):
    update.message.reply_text(f"Бот предназначен для проверки IP-адреса. Всё что нужно для активации, "
                              f"это ввести интересующий IP-адрес")


def checkIP(update, context):
    update.message.reply_text(f"Введите IP для проверки!")


def getIPinfo(update, context):
    text = update.message.text
    update.message.reply_text(f"Запрос IP: {text}!")

    response = requests.get(f"http://ip-api.com/json/{text}")
    response = response.json()
    flag_code = ""
    if response.get('countryCode') is None:
        flag_code == ":qu:"
    else:
        flag_code = f":{response.get('countryCode').lower()}:"

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

    chatID = update.effective_chat.id

    update.message.reply_text(msg, parse_mode="Markdown")
    context.bot.send_location(chat_id=chatID, latitude=response.get('lat'), longitude=response.get('lon'))


if __name__ == "__main__":
    main()
