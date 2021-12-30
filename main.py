import telebot
from telebot import types
import os
from user import User # imports the User class from User.py
from plan import is_valid_amount, is_valid_date # imports these functions in the plan.py file

dirname = os.path.dirname(__file__)
filename_api_key = os.path.join(dirname, 'Data/api_key.txt')

API_KEY = open(filename_api_key, 'r').read()
bot = telebot.TeleBot(API_KEY)

# /info
@bot.message_handler(commands = ['info'])
def info(message):
    bot.send_message(message.chat.id, "This bot is built by @FeMan1999, and it is intended to be a simple bot that helps you visualise and plan your finances over your university/school life.")

# /greet
@bot.message_handler(commands = ['greet'])
def greet(message):
    bot.send_message(message.chat.id, f"Hello {message.from_user.username}! How are you?")

# /help
@bot.message_handler(commands = ['help'])
def help(message):
    filename_commands_and_descriptions = os.path.join(dirname, 'Data/commands_and_descriptions.txt')

    with open(filename_commands_and_descriptions) as commands_and_descriptions: # opens the commands_and_description.txt file and reads the content, line by line
        lines = commands_and_descriptions.readlines()

    output = ''

    for line in lines:
        output += line

    bot.send_message(message.chat.id, output) # sends out the contents of the commands_and_descriptions.txt file

# /disclaimer
@bot.message_handler(commands = ['disclaimer'])
def disclaimer(message):
    bot.send_message(message.chat.id, "This bot does not:\n\n\n1. Collect your data or whatsoever\n\n2. This bot only serves to be a quick tool for you to input your finances over your university/school life so you can better visualise them and is not a full-fledged financial planner\n\n3. This bot only takes into account of controllable finances that you input yourself, and any market fluctuations in the economy will not be accounted for")

users = dict() # creates dictionary of users in a session with the bot?

# /plan
@bot.message_handler(commands = ['plan'])
def plan(message):
    user = User(message.from_user.username) # cretes a User class with the Telegram username as the name attribute
    users[message.chat.id] = user # stores the chat ID as the key and the User object as the value
    markup = types.ForceReply(selective = False) # for a ForceReply
    sent_message = bot.send_message(message.chat.id, "What is your current bank balance? (Please omit the dollar sign)", reply_markup = markup) # ForceReply
    bot.register_next_step_handler(sent_message, current_bank_balance_step) # calls the initial_bank balance_step(), and continues on from there

def current_bank_balance_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id

    if not is_valid_amount(user_input): # if the user input is not a valid amount of money
        sent_message = bot.reply_to(message, 'The initial bank balance should only consist of digits and a maximum of one decmial point and be a positive value!')
        bot.register_next_step_handler(sent_message, current_bank_balance_step)
        return

    user = users[chat_id] # gets the user object instance from the users dictionary
    user.current_bank_balance = float(user_input) # since the user_input at this point is a valid amount of money
    markup = types.ForceReply(selective = False) # for a ForceReply
    sent_message = bot.send_message(chat_id, 'When are you expected to graduate? Please input the month and year in this format: MM/YYYY, e.g. 01/2025 for January 2025', reply_markup = markup) # ForceReply
    bot.register_next_step_handler(sent_message, graduation_date_step)

def graduation_date_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id

    if not is_valid_date(user_input): # if the user input is not a valid date in the format: MM/YYYY
        sent_message = bot.reply_to(message, 'The expected graduation date should only consists of digits in the format: MM/YYYY, and must be at least in the following month of the current month!')
        bot.register_next_step_handler(sent_message, graduation_date_step)
        return

    user = users[chat_id] # gets the user object instance from the users dictionary
    user.graduation_date = user_input

    # bot.send_message(chat_id, f'Your username is {user.name}, your current bank balance is ${user.current_bank_balance} and your expected graduation date is {user.graduation_date} and you have {user.time_from_now_till_graduation} month(s) till graduation!')

    markup = types.ForceReply(selective = False) # for a ForceReply
    sent_message = bot.send_message(chat_id, 'How much are your school fees per term/semester/year? Include things like tuition fees, and any other compulsory school fees. Please omit the dollar sign.', reply_markup = markup) # ForceReply
    bot.register_next_step_handler(sent_message, school_fees_per_period_step)

def school_fees_per_period_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id

    if not is_valid_amount(user_input): # if the user input is not a valid amount of money
        sent_message = bot.reply_to(message, 'The school fees should only consist of digits and a maximum of one decmial point and be a positive value!')
        bot.register_next_step_handler(sent_message, school_fees_per_period_step)
        return

    user = users[chat_id]
    user.school_fees_per_period = float(user_input)
    markup = types.ForceReply(selective = False) # for a ForceReply
    sent_message = bot.send_message(chat_id, f'For how many more terms/semesters/years do you have to pay the school fees at ${user.school_fees_per_period} per term/semester/year? Please put 0 if you have finished paying all the school fees until graduation!', reply_markup = markup) # ForceReply
    bot.register_next_step_handler(sent_message, number_of_periods_to_pay_school_fees_step)

def number_of_periods_to_pay_school_fees_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id

    if not user_input.isdigit(): # if the user input is not an integer >= 0
        sent_message = bot.reply_to(message, 'The number of terms/semester should be a positive number with no decimal places!')
        bot.register_next_step_handler(sent_message, number_of_periods_to_pay_school_fees_step)
        return

    user = users[chat_id]
    user.number_of_periods_to_pay_school_fees = int(user_input)

    '''To commence with the next step in /plan'''

    bot.send_message(chat_id, f'You still have to pay ${user.expenses_total_school_fees_left_to_pay} at ${user.school_fees_per_period} per term/semester/year for {user.number_of_periods_to_pay_school_fees} term/semester/year (s)!')

# /feedback
@bot.message_handler(commands = ['feedback'])
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