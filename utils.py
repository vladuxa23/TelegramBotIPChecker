from telegram import ReplyKeyboardMarkup

IP_VALIDATION = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"


def getMainKeyboard():
    return ReplyKeyboardMarkup([["Проверить IP"], ["О боте"]], resize_keyboard=True)
