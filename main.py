import telebot
from telebot import types
import os
from user import User

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

# /plan
@bot.message_handler(commands = ['plan', 'Plan'])
def plan(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "What is your current bank balance?", reply_markup = markup)

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