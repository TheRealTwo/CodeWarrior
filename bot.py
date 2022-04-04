# files
import database as db
import blog_parse
import buttons as btn
import config
# libs
from aiogram import Bot, Dispatcher, executor, types
import logging
import requests
import time
import aioschedule
import asyncio

USER_ID = -1

# уровень логирования
logging.basicConfig(filename='example.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s',
                    level=logging.INFO)

# инициализация бота
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    asyncio.create_task(news())

# стартовое сообщение
@dp.message_handler(commands="start")
async def start(message: types.Message):
    global USER_ID
    USER_ID = message.from_user.id
    print(USER_ID)
    await message.answer("Приветствую! Я - покорный слуга такого создания, как Codeforces."
                         " Я умею уведомлять таких же смиренных, как и я, о грядущих контестах,"
                         " соревнованиях, а так же работать с api этого сайта. Желаю Вам удачи!", reply_markup=btn.menu)


# Главное меню
@dp.message_handler(commands="menu")
async def menu(message: types.Message):
    await message.answer('Выберите дальнейшее действие:', reply_markup=btn.menu)

# Выбор рассылки
@dp.callback_query_handler(lambda c: c.data == 'subscriptions')
async def choose_subscriptions(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Выберите тип рассылки:', reply_markup=btn.subscriptions)

# Рассылка блога
@dp.callback_query_handler(lambda c: c.data == 'blog')
async def blog_subscriptions(callback_query: types.CallbackQuery):
    if db.get_subs(USER_ID)['blog']:
        text = 'Вы уже подписаны на рассылку блога'
        await bot.send_message(callback_query.from_user.id, text, reply_markup=btn.unsub_blog)
    else:
        text = 'Вы не подписаны на рассылку блога.'
        await bot.send_message(callback_query.from_user.id, text, reply_markup=btn.sub_blog)

# Подписаться на блог
@dp.callback_query_handler(lambda c: c.data == 'sub_blog')
async def subscribe_blog(callback_query: types.CallbackQuery):
    db.change_subscription(USER_ID, blog=True)
    await bot.send_message(callback_query.from_user.id, 'Вы успешно подписались!😀', reply_markup=btn.menu)

# Отписаться от блога
@dp.callback_query_handler(lambda c: c.data == 'unsub_blog')
async def subscribe_blog(callback_query: types.CallbackQuery):
    db.change_subscription(USER_ID, blog=False)
    await bot.send_message(callback_query.from_user.id, 'Вы отписались. Как жаль😥', reply_markup=btn.menu)

# Рассылка контестов
@dp.callback_query_handler(lambda c: c.data == 'contests')
async def contest_subscriptions(callback_query: types.CallbackQuery):
    if db.get_subs(USER_ID)['contests']:
        text = 'Вы уже подписаны на рассылку контестов'
        await bot.send_message(callback_query.from_user.id, text, reply_markup=btn.unsub_contests)
    else:
        text = 'Вы не подписаны на рассылку контестов.'
        await bot.send_message(callback_query.from_user.id, text, reply_markup=btn.sub_contests)

# Подписаться на контесты
@dp.callback_query_handler(lambda c: c.data == 'sub_contests')
async def subscribe_contests(callback_query: types.CallbackQuery):
    db.change_subscription(USER_ID, contests=True)
    await bot.send_message(callback_query.from_user.id, 'Вы успешно подписались!😀', reply_markup=btn.menu)

# Отписаться от контестов
@dp.callback_query_handler(lambda c: c.data == 'unsub_contests')
async def unsubscribe_contests(callback_query: types.CallbackQuery):
    db.change_subscription(USER_ID, contests=False)
    await bot.send_message(callback_query.from_user.id, 'Вы отписались. Как жаль😥', reply_markup=btn.menu)



# Ближайшие контесты
@dp.callback_query_handler(lambda c: c.data == 'current_contests')
async def current_contests(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Какие контесты Вас интересуют?', reply_markup=btn.choose_contests)


# Все ближайшие контесты
@dp.callback_query_handler(lambda c: c.data == 'all_current_contests')
async def current_contests(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Секундочку...')
    contests = get_contests(False)
    text = 'Вот ближайшие контесты:\n'
    for el in contests:
        text += f'*Ссылка:* https://codeforces.com/contest/{el[0]}\n'
        text += f'*Название:* {el[1]}\n'
        duration_time = int(el[2] / 60)
        duration_time = str(duration_time // 60) + ' ч. ' + str(duration_time % 60) + ' мин.' if duration_time % 60 != 0 else str(duration_time // 60) + ' ч.'
        text += f'*Продолжительность:* ' + duration_time + '\n'
        if el[3] == 'BEFORE':
            status = 'не начался'
        elif el[3] == 'FINISHED':
            status = 'закончен'
        else:
            status = 'продолжается'
        text += f'*Статус:* {status}\n'
        if el[4] and el[3] == 'BEFORE':
            rem_time = abs(el[4] - time.time())
            days = abs(int(rem_time // 86400))
            hours = abs(int((rem_time % 86400) // 3600))
            mins = abs(int(((rem_time % 86400) % 3600) // 60))
            text += f'*Оставшееся время:* {days} д. {hours} ч. {mins} мин.\n'
        text += '\n'
    await bot.send_message(callback_query.from_user.id, text, reply_markup=btn.menu, parse_mode='Markdown', disable_web_page_preview=True)


# Только тренировочные ближайшие контесты
@dp.callback_query_handler(lambda c: c.data == 'training_current_contests')
async def current_contests(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Секундочку...')
    contests = get_contests(True)
    text = 'Вот ближайшие тренировочные контесты:\n'
    for el in contests:
        text += f'*Ссылка:* https://codeforces.com/contest/{el[0]}\n'
        text += f'*Название:* {el[1]}\n'
        duration_time = int(el[2] / 60)
        duration_time = str(duration_time // 60) + ' ч. ' + str(duration_time % 60) + ' мин.' if duration_time % 60 != 0 else str(duration_time // 60) + ' ч.'
        text += f'*Продолжительность:* ' + duration_time + '\n'
        if el[3] == 'BEFORE':
            status = 'не начался'
        elif el[3] == 'FINISHED':
            status = 'закончен'
        else:
            status = 'продолжается'
        text += f'*Статус:* {status}\n'
        if el[4] and el[3] == 'BEFORE':
            rem_time = abs(el[4] - time.time())
            days = abs(int(rem_time // 86400))
            hours = abs(int((rem_time % 86400) // 3600))
            mins = abs(int(((rem_time % 86400) % 3600) // 60))
            text += f'*Оставшееся время:* {days} д. {hours} ч. {mins} мин.\n'
        text += '\n'
    await bot.send_message(callback_query.from_user.id, text, reply_markup=btn.menu, parse_mode='Markdown', disable_web_page_preview=True)








async def check_for_new_posts(id=db.get_last_rus_post() + 1):
    rus_id = id
    start_rus_id = rus_id
    while True:
        response = requests.get(f'https://codeforces.com/api/blogEntry.view?blogEntryId={id}')
        if response.ok:
            logging.warning('API is not working now. Skipping...')
            return
        try:
            response = response.json()
        except Exception as e:
            logging.warning('API is not working now. Skipping...')
            return
        if response['status'] == 'FAILED':
            break
        if response['result']['oroginalLocale'] == 'ru':
            rus_id = id
        id += 1
    if start_rus_id != rus_id:
        db.change_post(rus_id)
        text = blog_parse.post_content(rus_id)
        if db.get_subs(USER_ID)['blog']:
            await post_new_blog(text)


# Поиск контестов часовой и дневной доступности
async def check_for_nearest_contests():
    contests = get_contests(False)
    contests = list(filter(lambda x: abs(time.time() - x[-1]) // 86400 <= 1, contests))
    for el in contests:
        if 3300 < abs(time.time() - el[-1]) < 3900:
            await post_nearest_contest(('часа', el))
            return
        elif 86100 < abs(time.time() - el[-1]) < 86700:
            if db.get_subs(USER_ID)['contests']:
                await post_nearest_contest(('дня', el))
            return

async def news():
    aioschedule.every(5).minutes.do(check_for_nearest_contests)
    aioschedule.every(5).minutes.do(check_for_new_posts)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

def get_contests(gym, token=None):
    response = requests.get(f'https://codeforces.com/api/contest.list?gym={gym}').json()['result']
    response = list(filter(lambda x: 'startTimeSeconds' in list(x.keys()), response))
    response = list(filter(lambda x: abs(time.time() - x['startTimeSeconds']) // 86400 <= 14, response))
    ans = []
    for el in response:
        row = (el['id'], el['name'], el['durationSeconds'], el['phase'], el['startTimeSeconds'])
        ans.append(row)
    return ans
    





async def post_nearest_contest(msg, callback_query=types.CallbackQuery):
    text = '*ВНИМАНИЕ!!*\n'
    text += f"До контеста *{msg[1][1]}* отсалось около {msg[0]}!\nСсылка: https://codeforces.com/contest/{msg[1][0]}\nУдачи!"
    await bot.send_message(USER_ID, text, reply_markup=btn.menu, parse_mode='Markdown', disable_web_page_preview=True)



async def post_new_blog(msg, callback_query=types.CallbackQuery):
    await bot.send_message(USER_ID, msg, reply_markup=btn.menu, parse_mode='HTML', disable_web_page_preview=True)
    
# запуск "лонг-поллинг" (апдейты пропускаются)
if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
        except Exception as e:
            logging.error(e)
            print(e)
            continue
