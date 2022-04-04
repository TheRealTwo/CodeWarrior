from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


menu = InlineKeyboardMarkup()
menu.add(InlineKeyboardButton('Рассылки', callback_data='subscriptions'))
menu.add(InlineKeyboardButton('Ближайшие контесты', callback_data='current_contests'))

subscriptions = InlineKeyboardMarkup()
subscriptions.add(InlineKeyboardButton('Блог', callback_data='blog'))
subscriptions.add(InlineKeyboardButton('Контесты', callback_data='contests'))

sub_blog = InlineKeyboardMarkup()
sub_blog.add(InlineKeyboardButton('Подписаться', callback_data='sub_blog'))

unsub_blog = InlineKeyboardMarkup()
unsub_blog.add(InlineKeyboardButton('Отписаться', callback_data='unsub_blog'))


sub_contests = InlineKeyboardMarkup()
sub_contests.add(InlineKeyboardButton('Подписаться', callback_data='sub_contests'))

unsub_contests = InlineKeyboardMarkup()
unsub_contests.add(InlineKeyboardButton('Отписаться', callback_data='unsub_contests'))


choose_contests = InlineKeyboardMarkup()
all_current_contests = InlineKeyboardButton('Все', callback_data='all_current_contests')
training_current_contests = InlineKeyboardButton('Только тренировочные', callback_data='training_current_contests')
choose_contests.row(all_current_contests, training_current_contests)