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
    print(response)
    flag_code = ""
    if response.get('countryCode') is None:
        flag_code == ":qu:"
    else:
        flag_code = f":{response.get('countryCode').lower()}:"

    msg = f"""Информация:\n
<b>Статус:</b> {response.get('status')}
<b>Страна:</b> {flag.flagize(flag_code, subregions=True)} {response.get('country')}
<b>Код страны:</b> {response.get('countryCode')}
<b>Регион:</b> {response.get('regionName')}
<b>Код региона:</b> {response.get('region')}
<b>Город:</b> {response.get('city')}
<b>Индекс:</b> {response.get('zip')}
<b>Широта:</b> {response.get('lat')}
<b>Долгота:</b> {response.get('lon')}
<b>Врем. пояс:</b> {response.get('timezone')}
<b>Провайдер:</b> {response.get('isp')}
<b>Организация:</b> {response.get('org')}
<b>Авт-ая система:</b> {response.get('as')}"""

    chatID = update.effective_chat.id
    print(msg)

    update.message.reply_text(msg, parse_mode="HTML")
    context.bot.send_location(chat_id=chatID, latitude=response.get('lat'), longitude=response.get('lon'))


if __name__ == "__main__":
    main()
