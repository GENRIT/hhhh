import telebot
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play

# Создаем экземпляр бота
bot = telebot.TeleBot('7208468509:AAEdWRPRQ3iA-rXo5P9AylhVo89ziS5N02c')

# Настройка pyttsx3
engine = pyttsx3.init()

# Функция для настройки голоса
def setup_voice(engine):
    voices = engine.getProperty('voices')
    # Ищем мужской голос (настраиваем по вашему усмотрению)
    for voice in voices:
        if 'male' in voice.name:
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 150)  # Скорость речи
    engine.setProperty('volume', 1)  # Громкость

setup_voice(engine)

# Обработчик сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text
    if len(text) > 500:  # Ограничиваем длину текста
        bot.send_message(message.chat.id, "Текст слишком длинный, сократите его.")
        return

    # Сгенерировать голосовое сообщение
    engine.save_to_file(text, 'voice.mp3')
    engine.runAndWait()

    # Отправка голосового сообщения пользователю
    voice = AudioSegment.from_file('voice.mp3', format='mp3')
    voice.export('voice.ogg', format='ogg', codec='libopus')
    with open('voice.ogg', 'rb') as voice_file:
        bot.send_voice(message.chat.id, voice_file)

# Запуск бота
bot.polling(none_stop=True)
