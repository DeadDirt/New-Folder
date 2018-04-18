from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import random, requests


def start(bot, update):
    update.message.reply_text("Приветствую! Я чат-бот. Вас что-то интересует?")


def time(bot, update):
    import time
    _ = time.asctime().split()
    update.message.reply_text(_[3])


def date(bot, update):
    import time
    _ = time.asctime().split()
    update.message.reply_text(_[2]+' of '+_[1]+', year '+_[4])


def help(bot, update):
    update.message.reply_text('''Не то, чтобы здесь было много функций...
/date - показывает дату\n/time - показывает точное время\n/adress - поможет найти точный адрес и координаты места по названию
А вообще, попытайся попросить меня о чем-то нормальным языком. Отвечу - значит умею.''')


def adress(bot, update):
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode="+' '.join(update.message.text.split()[1:])+"&format=json"
    try:
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()

            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            toponym_coodrinates = toponym["Point"]["pos"]
            update.message.reply_text('Полный адрес:', toponym_address, "\nКоординаты:", toponym_coodrinates)
        else:
            update.message.reply_text("Ошибка выполнения запроса:"+'\n'+geocoder_request+'\n'+"Http статус: "+response.status_code+" ("+response.reason+")")
    except Exception:
        update.message.reply_text("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")


def responce(bot, update):
    global inc, past
    temp = update.message.text
    inc.append(temp)
    if temp == 'showmewhatuwgot':
        update.message.reply_text(inc)
    # проверка, нужно ли задействовать базовые команды
    elif 'повтори' in temp.lower():
        update.message.reply_text(' '.join(update.message.text.split()[1:]))
    elif 'Где' in temp.lower():
        adress(bot, update)
    elif any(list(map(lambda x: x in temp.lower().replace('?', ''), ['который час', 'сколько времени', 'точное время', 'какое время']))):
        time(bot, update)
    elif any(list(map(lambda x: x in temp.lower().replace('?', ''), ['который день', 'какой день', 'точная дата', 'какая дата']))):
        date(bot, update)
    elif any(list(map(lambda x: x in temp.lower().replace('?', ','), ['нужна помощь', 'помощь', 'подсказка', 'подсказку', 'подскажи']))):
        help(bot, update)


    # если нет, задействовать модуль "дурачка" (dummy)
    else:
        humanlike(bot, update)


# dummy'ик
def humanlike(bot, update):
    temp = update.message.text
    # немного ответов на самый простой вопрос
    if 'как' in temp.lower().split() and 'дела' in temp.lower():
        if not past[0]:
            _ = random.choice(['Нормально', 'Неплохо', 'Хорошо', 'Прекрасно', 'Великолепно', 'Плохо'])
            past[0].append(_)
            past[0].append(1)
            update.message.reply_text(_)
        elif past[0][1] == 1:
            _ = update.message.reply_text('Я же говорил, '+past[0][0].lower())
            past[0][1] += 1
        elif past[0][1] == 2:
            _ = update.message.reply_text('В последний раз говорю, '+past[0][0].lower())
            past[0][1] += 1
        elif past[0][1] >= 3:
            _ = update.message.reply_text('Надоел. Никак')
    # заготовленные реакции
    elif 'как' in temp.lower().split():
        update.message.reply_text(random.choice(['Так', 'Неплохо', 'Образно', 'Буквально', 'Как рыба в воде', 'Как...тус.']))
    elif 'что' in temp.lower().split() and 'делаешь' in temp.lower():
        update.message.reply_text(random.choice(['Ем.', 'Прокрастинирую', 'Существую', 'Мыслю', 'Мечтаю об электроовцах']))
    elif any(list(map(lambda x: x in temp.lower().split(), ['привет', 'здоров', 'день добрый', 'добрый день', 'добрый вечер', 'доброе утро']))):
        update.message.reply_text(random.choice(['Доброго времени суток', 'Здравствуйте', 'Коничива', 'Привет']))
    elif any(list(map(lambda x: x in temp.lower().split(), ['да', 'хорошо', 'ок', 'угу', 'окей', 'ладно']))):
        update.message.reply_text(random.choice(['Вот и хорошо!', 'Отлично', 'Здорово', 'Я рад']))
    elif any(list(map(lambda x: x in temp.lower().split(), ['нет', 'неа', 'ответ отрицательный', 'откажусь']))):
        update.message.reply_text(random.choice(['Жаль', 'Ну ладно', 'Понял', 'Ладно']))
    # ответ на вопросы
    elif temp[-1] == '?' or temp[-2] == '?':
        if past[1]:
            if past[1][0] >= 3:
                update.message.reply_text(random.choice(['Слишком много вопросов!', 'Расскажи лучше о себе', 'Можно проигнорировать?', 'А зачем так много вопросов? Я же машина.']))
                past[1][0] = 0
            else:
                update.message.reply_text(random.choice(['Да', 'Нет', 'Возможно', '42', 'Правильный ответ - пудинг?', '50/50']))
        else:
            update.message.reply_text(random.choice(['Да', 'Нет', 'Возможно', '42', 'Правильный ответ - пудинг?', '50/50']))
            past[1].append(0)
        past[1][0] += 1
    # ответ на спам
    elif str(temp).isdigit():
        if past[2][0]:
            past[2][0] += 1
            if past[2][0] >= 3:
                update.message.reply_text('Хватит спамить')
                past[2][0] = 0
        else:
            past[2].append(1)
            update.message.reply_text(random.choice(['И что это?', 'Зачем?', 'Это шифр?', '1001010101101', temp]))

    # Ни один из сценариев не задействован, в ответ - случайная фраза или какое-то предложение
    else:
        update.message.reply_text(random.choice(['Вот оно как.', 'Интересно...', 'На этом можем и закончить', 'Как дела?', 'Любишь пингвинчиков?', 'Что такое?', 'Неп-неп-неп']))


def main():
    updater = Updater("564737056:AAGkBxSlnoSAZz8oazbC8onsdLUUBZrMYu4", request_kwargs={'proxy_url': 'socks5://118.139.178.67:29701'})
    dp = updater.dispatcher

    # подключение функций
    dp.add_handler(MessageHandler(Filters.text, responce))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("date", date))
    dp.add_handler(CommandHandler("time", time))
    dp.add_handler(CommandHandler("adress", adress))

    updater.start_polling()  # цикл приема и обработки сообщений
    updater.idle()  # ожидание завершения


if __name__ == '__main__':
    inc, past = [], [[] for i in range(3)]  # база принятых сообщений, для использования дальше
    main()
