import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands= ['start'])
def hello(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Здравствуйте, {message.from_user.first_name}! \n \
Чтобы начать работу введите команду боту в следующем формате: \n <имя валюты> \
<в какую валюту перевести> <количество переводимой валюты> \n \
Увидеть список всех доступных валют : /values ")

@bot.message_handler(commands= ['help'])
def start_help(message: telebot.types.Message):
    text = ('Чтобы начать работу введите команду боту в следующем формате: \n <имя валюты> \
<в какую валюту перевести> <количество переводимой валюты> \n \
Увидеть список всех доступных валют : /values ')
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands= ['values'])
def values(message: telebot.types.Message):
    text = "Валюты, доступные для конвертации:"
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types= ['text'])
def convert(message: telebot.types.Message):
    try:
        values = (message.text.lower()).split(" ")

        if len(values) > 3:
            raise APIException("Слишком много параметров.")

        elif len(values) == 1 or len(values) == 2:
            raise APIException("Слишком мало параметров.")

        elif values[2] < "0":
            raise APIException("Введено отрицательное число")

        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя. \n {e}")

    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду \n {e}")
    else:
        text = f"Цена {amount} {quote} в {base} = {total_base}"
        bot.send_message(message.chat.id, text)

bot.polling(none_stop= True)