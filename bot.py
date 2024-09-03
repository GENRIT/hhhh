import telebot
from telebot import types
import os

API_TOKEN = '7240803057:AAG7xMLwBKljEiRpjN7EYEVfANX9BGthUCI'
OWNER_CHAT_ID = 1420106372

bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения статуса прочтения сообщений
read_status = {}

# Обработка команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Создаем инлайн-кнопку
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("HoTing", url="https://t.me/HoTing_bot")
    markup.add(button)
    
    # Отправляем изображение с кнопкой
    bot.send_photo(message.chat.id, 
                   "https://picsum.photos/800/600",  # Замените на вашу ссылку на изображение
                   caption="Здравствуйте! Я ваш помощник бот. Чем могу помочь?",
                   reply_markup=markup)

# Обработка документов и видео
@bot.message_handler(content_types=['document', 'video'])
def handle_docs_and_videos(message):
    if message.chat.id == OWNER_CHAT_ID:
        bot.reply_to(message, "Получен документ или видео от администратора.")
    else:
        # Пересылка документа или видео администратору
        forwarded = bot.forward_message(OWNER_CHAT_ID, message.chat.id, message.message_id)
        read_status[forwarded.message_id] = False
        
        # Создание инлайн кнопки
        markup = types.InlineKeyboardMarkup()
        status_button = types.InlineKeyboardButton("Не прочитано", callback_data=f"status_{forwarded.message_id}")
        markup.add(status_button)
        
        bot.reply_to(message, "Ваш документ или видео отправлены администратору. Ожидайте ответа.", reply_markup=markup)

# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.chat.id == OWNER_CHAT_ID:
        if message.reply_to_message:
            original_message = message.reply_to_message
            if original_message.forward_from:
                # Отправка ответа администратора оригинальному пользователю
                bot.send_message(original_message.forward_from.id, message.text)
                # Обновление статуса прочтения
                read_status[original_message.message_id] = True
                update_read_status(original_message.forward_from.id, original_message.message_id)
            else:
                bot.reply_to(message, "Невозможно найти оригинальное сообщение пользователя.")
        else:
            bot.reply_to(message, "Пожалуйста, используйте функцию ответа на сообщение для ответа пользователю.")
    else:
        # Пересылка текстового сообщения администратору
        forwarded = bot.forward_message(OWNER_CHAT_ID, message.chat.id, message.message_id)
        read_status[forwarded.message_id] = False
        
        # Создание инлайн кнопки
        markup = types.InlineKeyboardMarkup()
        status_button = types.InlineKeyboardButton("Не прочитано", callback_data=f"status_{forwarded.message_id}")
        markup.add(status_button)
        
        bot.reply_to(message, "Ваше сообщение отправлено администратору. Ожидайте ответа.", reply_markup=markup)

# Обработка фото
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.chat.id == OWNER_CHAT_ID:
        # Обработка фото от администратора
        if message.reply_to_message and message.reply_to_message.forward_from:
            # Отправка фото оригинальному пользователю
            bot.send_photo(message.reply_to_message.forward_from.id, message.photo[-1].file_id, caption=message.caption)
            # Обновление статуса прочтения
            read_status[message.reply_to_message.message_id] = True
            update_read_status(message.reply_to_message.forward_from.id, message.reply_to_message.message_id)
        else:
            bot.reply_to(message, "Пожалуйста, отправляйте фото в ответ на сообщение пользователя.")
    else:
        # Пересылка фото администратору
        forwarded = bot.forward_message(OWNER_CHAT_ID, message.chat.id, message.message_id)
        read_status[forwarded.message_id] = False
        
        # Создание инлайн кнопки
        markup = types.InlineKeyboardMarkup()
        status_button = types.InlineKeyboardButton("Не прочитано", callback_data=f"status_{forwarded.message_id}")
        markup.add(status_button)
        
        bot.reply_to(message, "Ваше фото отправлено администратору. Ожидайте ответа.", reply_markup=markup)

# Обработка стикеров
@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    if message.chat.id == OWNER_CHAT_ID:
        # Обработка стикера от администратора
        if message.reply_to_message and message.reply_to_message.forward_from:
            # Отправка стикера оригинальному пользователю
            bot.send_sticker(message.reply_to_message.forward_from.id, message.sticker.file_id)
            # Обновление статуса прочтения
            read_status[message.reply_to_message.message_id] = True
            update_read_status(message.reply_to_message.forward_from.id, message.reply_to_message.message_id)
        else:
            bot.reply_to(message, "Пожалуйста, отправляйте стикеры в ответ на сообщение пользователя.")
    else:
        # Пересылка стикера администратору
        forwarded = bot.forward_message(OWNER_CHAT_ID, message.chat.id, message.message_id)
        read_status[forwarded.message_id] = False
        
        # Создание инлайн кнопки
        markup = types.InlineKeyboardMarkup()
        status_button = types.InlineKeyboardButton("Не прочитано", callback_data=f"status_{forwarded.message_id}")
        markup.add(status_button)
        
        bot.reply_to(message, "Ваш стикер отправлен администратору. Ожидайте ответа.", reply_markup=markup)

# Обработка голосовых сообщений
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    if message.chat.id == OWNER_CHAT_ID:
        # Обработка голосового сообщения от администратора
        if message.reply_to_message and message.reply_to_message.forward_from:
            # Отправка голосового сообщения оригинальному пользователю
            bot.send_voice(message.reply_to_message.forward_from.id, message.voice.file_id)
            # Обновление статуса прочтения
            read_status[message.reply_to_message.message_id] = True
            update_read_status(message.reply_to_message.forward_from.id, message.reply_to_message.message_id)
        else:
            bot.reply_to(message, "Пожалуйста, отправляйте голосовые сообщения в ответ на сообщение пользователя.")
    else:
        # Пересылка голосового сообщения администратору
        forwarded = bot.forward_message(OWNER_CHAT_ID, message.chat.id, message.message_id)
        read_status[forwarded.message_id] = False
        
        # Создание инлайн кнопки
        markup = types.InlineKeyboardMarkup()
        status_button = types.InlineKeyboardButton("Не прочитано", callback_data=f"status_{forwarded.message_id}")
        markup.add(status_button)
        
        bot.reply_to(message, "Ваше голосовое сообщение отправлено администратору. Ожидайте ответа.", reply_markup=markup)

# Обработка нажатий на инлайн кнопки
@bot.callback_query_handler(func=lambda call: call.data.startswith('status_'))
def callback_query(call):
    message_id = int(call.data.split('_')[1])
    if read_status.get(message_id, False):
        bot.answer_callback_query(call.id, "Сообщение уже прочитано администратором")
    else:
        bot.answer_callback_query(call.id, "Сообщение еще не прочитано администратором")

# Функция для обновления статуса прочтения
def update_read_status(chat_id, message_id):
    try:
        bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("Прочитано", callback_data=f"status_{message_id}")
            )
        )
    except Exception as e:
        print(f"Ошибка при обновлении статуса: {e}")

# Запуск бота
bot.polling()
