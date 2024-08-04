import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Инициализация модели и токенизатора
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForCausalLM.from_pretrained("OuteAI/Lite-Oute-1-65M-Instruct").to(device)
tokenizer = AutoTokenizer.from_pretrained("OuteAI/Lite-Oute-1-65M-Instruct")

def generate_response(message: str, temperature: float = 0.4, repetition_penalty: float = 1.12) -> str:
    # Apply the chat template and convert to PyTorch tensors
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message}
    ]
    input_ids = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt"
    ).to(device)
    # Generate the response
    output = model.generate(
        input_ids,
        max_length=512,
        temperature=temperature,
        repetition_penalty=repetition_penalty,
        do_sample=True
    ) 
    # Decode the generated output
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Обработчик команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! I am your text generation bot. Send me a message and I will respond.')

# Обработчик текстовых сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    response = generate_response(user_message)
    update.message.reply_text(response)

def main():
    # Вставьте сюда ваш токен, который вы получили от BotFather
    token = 'YOUR_TELEGRAM_BOT_TOKEN_HERE'

    updater = Updater(token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
