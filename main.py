import telebot
from telebot import types
import os
from user import User # imports the User class from User.py
import plan # imports the plan.py file


dirname = os.path.dirname(__file__)
filename_api_key = os.path.join(dirname, 'Data/api_key.txt')

API_KEY = open(filename_api_key, 'r').read()
bot = telebot.TeleBot(API_KEY)

# /info
@bot.message_handler(commands = ['info', 'Info'])
def info(message):
    bot.send_message(message.chat.id, "This bot is built by @FeMan1999, and it is intended to be a simple bot that helps you visualise and plan your finances over your university/school life.")

# /greet
@bot.message_handler(commands = ['Greet', 'greet'])
def greet(message):
    bot.send_message(message.chat.id, f"Hello {message.from_user.username}! How are you?")

# /help
@bot.message_handler(commands = ['help', 'Help'])
def help(message):
    filename_commands_and_descriptions = os.path.join(dirname, 'Data/commands_and_descriptions.txt')

    with open(filename_commands_and_descriptions) as commands_and_descriptions: # opens the commands_and_description.txt file and reads the content, line by line
        lines = commands_and_descriptions.readlines()

    output = ''

    for line in lines:
        output += line

    bot.send_message(message.chat.id, output) # sends out the contents of the commands_and_descriptions.txt file

# /disclaimer
@bot.message_handler(commands = ['disclaimer', 'Disclaimer'])
def disclaimer(message):
    bot.send_message(message.chat.id, "This bot does not:\n\n\n1. Collect your data or whatsoever\n\n2. This bot only serves to be a quick tool for you to input your finances over your university/school life so you can better visualise them and is not a full-fledged financial planner\n\n3. This bot only takes into account of controllable finances that you input yourself, and any market fluctuations in the economy will not be accounted for")

'''The following is just to understand how the register_next_step_handler works'''
user_dict = {}

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hi there, I am Example bot.
What's your name?
""")
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'How old are you?')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'Age should be a number. How old are you?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Male', 'Female')
        msg = bot.reply_to(message, 'What is your gender', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Male') or (sex == u'Female'):
            user.sex = sex
        else:
            raise Exception("Unknown sex")
        bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex)
    except Exception as e:
        bot.reply_to(message, 'oooops')

'''End of the register_next_step_handler'''

# # /plan
# @bot.message_handler(commands = ['plan', 'Plan'])
# def plan(message):
#     user = User(message.from_user.username) # cretes a User class with the Telegram username as the name attribute
#     markup = types.ForceReply(selective = False) # for a ForceReply
#     sent_message = bot.send_message(message.chat.id, "What is your current bank balance?", reply_markup = markup) # ForceReply
#     bot.register_next_step_handler(sent_message, plan.)

# @bot.message_handler(content_types=['text'])
# def welcome(pm):
#     sent_msg = bot.send_message(pm.chat.id, "Welcome to bot. what's your name?")
#     bot.register_next_step_handler(sent_msg, name_handler) #Next message will call the name_handler function
    
# def name_handler(pm):
#     name = pm.text
#     sent_msg = bot.send_message(pm.chat.id, f"Your name is {name}. how old are you?")
#     bot.register_next_step_handler(sent_msg, age_handler, name) #Next message will call the age_handler function

# def age_handler(pm, name):
#     age = pm.text
#     bot.send_message(pm.chat.id, f"Your name is {name}, and your age is {age}.")

# /feedback
@bot.message_handler(commands = ['feedback', 'Feedback'])
def feedback(message):
    bot.send_message(message.chat.id, 'Please send your feedback/suggestions to: https://forms.gle/LZJALSrDiBuqibN79')

# for any unknwon or unrecognised commands/inputs
@bot.message_handler(content_types = ['text', 'pinned_message'])
def unknown_text(message):
    bot.reply_to(message, "I'm sorry, I do not recognise this command. Would you like to use /help to see all available commands instead?")

# for any media sent to the bot
@bot.message_handler(content_types = ['sticker', 'photo', 'audio', 'document', 'video', 'video_note', 'voice', 'location', 'contact'])
def unknown_media(message):
    bot.send_document(message.chat.id, 'https://i.pinimg.com/originals/b8/83/c2/b883c2fa99c1aa9c2f7c4268fbffde75.gif') # sends a gif of a confused Naruto

bot.infinity_polling()