import telebot
from telebot import types

# Replace 'YOUR_TOKEN' with your bot's API token
TOKEN = "6475871616:AAEF976_ZuaE_8g5h1fxK-4rbqhFXhb189A"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Please enter the value of x: ')
    bot.register_next_step_handler(message, get_x)

def get_x(message):
    try:
        x = int(message.text)
        bot.send_message(message.chat.id, 'Please enter the value of y: ')
        bot.register_next_step_handler(message, get_y, x)
    except ValueError:
        bot.send_message(message.chat.id, 'Invalid input. Please enter an integer value for x.')
        start(message)

def get_y(message, x):
    try:
        y = int(message.text)
        sum = x + y
        bot.send_message(message.chat.id, f'The sum of x and y is: {sum}')
    except ValueError:
        bot.send_message(message.chat.id, 'Invalid input. Please enter an integer value for y.')
        start(message)

bot.polling()


# # Store the values of x and y
# user_data = {}

# def get_sum(message):
#     chat_id = message.chat.id
#     x = user_data[chat_id]['x']
#     y = user_data[chat_id]['y']
#     return x + y

# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     bot.reply_to(message, "Hello! I will help you sum two numbers. Please send me a number after typing /x or /y")

# @bot.message_handler(commands=['x'])
# def x_handler(message):
#     msg = bot.reply_to(message, "Give me x:")
#     bot.register_next_step_handler(msg, process_x_step)

# def process_x_step(message):
#     try:
#         chat_id = message.chat.id
#         user_data[chat_id] = user_data.get(chat_id, {})
#         user_data[chat_id]['x'] = int(message.text)
#         bot.reply_to(message, "Got it! Now send me a number after typing /y")
#     except ValueError:
#         bot.reply_to(message, "That doesn't look like a number. Try again by typing /x")

# @bot.message_handler(commands=['y'])
# def y_handler(message):
#     msg = bot.reply_to(message, "Give me y:")
#     bot.register_next_step_handler(msg, process_y_step)

# def process_y_step(message):
#     try:
#         chat_id = message.chat.id
#         user_data[chat_id]['y'] = int(message.text)
#         bot.reply_to(message, "The sum of x and y is: {}".format(get_sum(message)))
#     except ValueError:
#         bot.reply_to(message, "That doesn't look like a number. Try again by typing /y")

# # Polling loop
# bot.polling(none_stop=True)