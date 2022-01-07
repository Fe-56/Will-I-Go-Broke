import telebot
from telebot import types
import os
from user import User # imports the User class from User.py
from plan import * # imports all the functions in the plan.py file

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
        markup = types.ForceReply(selective = False) # for a ForceReply
        sent_message = bot.reply_to(message, '<b>ERROR!</b>\n\nThe initial bank balance should only consist of digits and a maximum of one decmial point and be a positive value!', reply_markup = markup, parse_mode = 'HTML')
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
        markup = types.ForceReply(selective = False) # for a ForceReply
        sent_message = bot.reply_to(message, '<b>ERROR!</b>\n\nThe expected graduation date should only consists of digits in the format: MM/YYYY, and must be at least in the following month of the current month!', reply_markup = markup, parse_mode = 'HTML')
        bot.register_next_step_handler(sent_message, graduation_date_step)
        return

    user = users[chat_id] # gets the user object instance from the users dictionary
    user.graduation_date = user_input
    markup = types.ForceReply(selective = False) # for a ForceReply
    sent_message = bot.send_message(chat_id, 'How much are your school fees per term/semester/year? Include things like tuition fees, and any other compulsory school fees. Please omit the dollar sign.\n\nPlease input none if you do not need to pay anymore school fees.', reply_markup = markup) # ForceReply
    bot.register_next_step_handler(sent_message, school_fees_per_period_step)

def school_fees_per_period_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id

    if (is_valid_amount(user_input)) or (user_input.lower() == 'none'): # if the user input is a valid amount of money or none
        user = users[chat_id]

        if user_input.lower() == 'none': # move to the monthly expenses step since the user does not need to pay any school fees
            user.school_fees_per_period_step = float(0)
            user.number_of_periods_to_pay_school_fees = 0
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.send_message(chat_id, 'Please input, one by one, your expected monthly expenses in the format: Name: Amount (omit the dollar sign!)\n\n e.g. Food: 300\n\nPlease input none if you do not have/foresee any monthly expenses', reply_markup = markup) # ForceReply
            bot.register_next_step_handler(sent_message, monthly_expenses_step)

        else:
            user.school_fees_per_period = float(user_input)
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.send_message(chat_id, f'For how many more terms/semesters/years do you have to pay the school fees at ${user.school_fees_per_period} per term/semester/year?', reply_markup = markup) # ForceReply
            bot.register_next_step_handler(sent_message, number_of_periods_to_pay_school_fees_step)

    elif (not is_valid_amount(user_input)): # if the user input is not a valid amount of money
        markup = types.ForceReply(selective = False) # for a ForceReply
        sent_message = bot.reply_to(message, '<b>ERROR!</b>\n\nThe school fees should only consist of digits and a maximum of one decmial point and be a positive value!', reply_markup = markup, parse_mode = 'HTML')
        bot.register_next_step_handler(sent_message, school_fees_per_period_step)
        return

def number_of_periods_to_pay_school_fees_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id

    if not user_input.isdigit(): # if the user input is not an integer >= 0
        markup = types.ForceReply(selective = False) # for a ForceReply
        sent_message = bot.reply_to(message, '<b>ERROR!</b>\n\nThe number of terms/semesters/years should be a positive number with no decimal places!', reply_markup = markup, parse_mode = 'HTML')
        bot.register_next_step_handler(sent_message, number_of_periods_to_pay_school_fees_step)
        return

    user = users[chat_id]
    user.number_of_periods_to_pay_school_fees = int(user_input)
    markup = types.ForceReply(selective = False) # for a ForceReply
    sent_message = bot.send_message(chat_id, 'Please input, one by one, your expected monthly expenses in the format: Name: Amount (omit the dollar sign!)\n\n e.g. Food: 300\n\nPlease input none if you do not have/foresee any monthly expenses', reply_markup = markup) # ForceReply
    bot.register_next_step_handler(sent_message, monthly_expenses_step)

def monthly_expenses_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id
    user = users[chat_id] 

    while (user_input.lower() != 'done'):
        if is_valid_expense(user_input):
            expense_name, expense_amount = get_expense(user_input)
            user.monthly_expenses[expense_name] = expense_amount # stores the name and the amount of the monthly expenses in the dictionary in the user object instance
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.send_message(chat_id, 'Please input your next monthly expense! If you are done, please input done', reply_markup = markup)
            bot.register_next_step_handler(sent_message, monthly_expenses_step)
            return

        elif user_input.lower() == 'none': # if the user has no monthly expenses, move on to big expenses step
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.send_message(chat_id, 'Please input, one by one, your expected one-time big expenses in the format: Name: Amount (omit the dollar sign!)\n\ne.g. Laptop: 2000\n\nPlease input none if you do not have/foresee any one-time big expenses', reply_markup = markup) # ForceReply
            bot.register_next_step_handler(sent_message, big_expenses_step)
            break

        else:
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.reply_to(message, '<b>ERROR!</b>\n\nPlease input a single monthly expense in the format: Name: Amount\n\n e.g. Spotify subscription: 4\n\n Where there is at most 1 number (positive) and 1 colon', reply_markup = markup, parse_mode = 'HTML')
            bot.register_next_step_handler(sent_message, monthly_expenses_step)
            return

    printed_monthly_expenses = ''

    for expense in user.monthly_expenses.keys():
        printed_monthly_expenses += f'{expense}: ${user.monthly_expenses[expense]}' + '\n'

    bot.send_message(chat_id, printed_monthly_expenses) # sends a message containing all the monthly expenses that the user inputted earlier on
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True) # multiple choice reply
    markup.add('Yes', 'No')
    sent_message = bot.send_message(chat_id, 'Does the message above correctly display all your monthly expenses?', reply_markup = markup)
    bot.register_next_step_handler(sent_message, check_monthly_expenses_step)

def check_monthly_expenses_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id
    user = users[chat_id] 

    if user_input == 'Yes': # if the user states that the monthly expenses are correct and all good
        markup = types.ForceReply(selective = False) # for a ForceReply
        sent_message = bot.send_message(chat_id, 'Please input, one by one, your expected one-time big expenses in the format: Name: Amount (omit the dollar sign!)\n\ne.g. Laptop: 2000\n\nPlease input none if you do not have/foresee any one-time big expenses', reply_markup = markup) # ForceReply
        bot.register_next_step_handler(sent_message, big_expenses_step)

    elif user_input == 'No': # if the user states that the monthly expenses are not correct
        user.monthly_expenses.clear() # resets the dictionary containing the monthly expenses
        markup = types.ForceReply(selective = False) # for a ForceReply
        sent_message = bot.reply_to(message, 'Please input your monthly expenses again, one by one, in the format: Name: Amount (omit the dollar sign!)', reply_markup = markup)
        bot.register_next_step_handler(sent_message, monthly_expenses_step)

def big_expenses_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id
    user = users[chat_id] 

    while (user_input.lower() != 'done'):
        if is_valid_expense(user_input):
            expense_name, expense_amount = get_expense(user_input)
            user.big_expenses[expense_name] = expense_amount # stores the name and the amount of the big expenses in the dictionary in the user object instance
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.send_message(chat_id, 'Please input your next big expense! If you are done, please input done', reply_markup = markup)
            bot.register_next_step_handler(sent_message, big_expenses_step)
            return

        elif user_input.lower() == 'none': # if the user has no one-time big expenses, move on to the other expenses step
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.send_message(chat_id, 'Please input, one by one, your expected other expenses in the following format: Name: Amount for x [period]\n\nWhere name should be a single word with no spaces, where amount is the amount to be paid in a single [period], where a [period] can be a month, semester, term, etc., just need to write down a single word in place of the [period], x is a number and omit the dollar sign. E.g. Hostel: 1000 for 3 terms\n\nOther expenses are basically expenses that are not big one-time expeses, and are are also not expenses that you have to pay every month till graduation. Other expenses are expenses that you may have to pay for a certain number of months/periods during your university life.\n\nPlease input none if you have no other expenses.', reply_markup = markup) # ForceReply
            bot.register_next_step_handler(sent_message, other_expenses_step)
            break

        else:
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.reply_to(message, '<b>ERROR!</b>\n\nPlease input a single big expense in the format: Name: Amount\n\n e.g. iPad: 1000\n\n Where there is at most 1 number (positive) and 1 colon', reply_markup = markup, parse_mode = 'HTML')
            bot.register_next_step_handler(sent_message, big_expenses_step)
            return

    printed_big_expenses = ''

    for expense in user.big_expenses.keys():
        printed_big_expenses += f'{expense}: ${user.big_expenses[expense]}' + '\n'

    bot.send_message(chat_id, printed_big_expenses) # sends a message containing all the big one-time expenses that the user inputted earlier on
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True) # multiple choice reply
    markup.add('Yes', 'No')
    sent_message = bot.send_message(chat_id, 'Does the message above correctly display all your one-time big expenses?', reply_markup = markup)
    bot.register_next_step_handler(sent_message, check_big_expenses_step)

def check_big_expenses_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id
    user = users[chat_id] 

    if user_input == 'Yes': # if the user states that the big expenses are correct and all good
        markup = types.ForceReply(selective = False) # for a ForceReply
        sent_message = bot.send_message(chat_id, 'Please input, one by one, your expected other expenses in the following format: Name: Amount for x [period]\n\nWhere name should be a single word with no spaces, where amount is the amount to be paid in a single [period], where a [period] can be a month, semester, term, etc., just need to write down a single word in place of the [period], x is a number and omit the dollar sign. E.g. Hostel: 1000 for 3 terms\n\nOther expenses are basically expenses that are not big one-time expeses, and are are also not expenses that you have to pay every month till graduation. Other expenses are expenses that you may have to pay for a certain number of months/periods during your university life.\n\nPlease input none if you have no other expenses.', reply_markup = markup) # ForceReply
        bot.register_next_step_handler(sent_message, other_expenses_step)

    elif user_input == 'No': # if the user states that the monthly expenses are not correct
        user.big_expenses.clear() # resets the dictionary containing the big expenses
        markup = types.ForceReply(selective = False) # for a ForceReply
        sent_message = bot.reply_to(message, 'Please input your big expenses again, one by one, in the format: Name: Amount (omit the dollar sign!)', reply_markup = markup)
        bot.register_next_step_handler(sent_message, big_expenses_step)

def other_expenses_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id
    user = users[chat_id] 

    while user_input.lower() != 'done':
        if is_valid_other_expense(user_input):
            expense_name, expense_amount_number_of_periods = get_other_expense(user_input) # where expense_amount_number_of_periods is a list [Amount, for , x, [period]]
            user.other_expenses[expense_name] = expense_amount_number_of_periods # stores the name and the amount of the other expenses in the dictionary in the user object instance
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.send_message(chat_id, 'Please input your next other expense! If you are done, please input done', reply_markup = markup)
            bot.register_next_step_handler(sent_message, other_expenses_step)
            return

        elif user_input.lower() == 'none': # if the user has no other expenses, move on to the monthly income step
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.send_message(chat_id, 'Please input, one by one, your expected monthly income/allowance in the format: Name: Amount (omit the dollar sign!)\n\n e.g. Allowance from parents: 200\n\n NOTE: Whatever you input here should be the income/allowance that you are EXPECTED TO GET EVERY SINGLE MONTH till graduation and does not depend on whether it is during any vacation or internship or not!\n\nPlease input none if you do not have any monthly income/allowance.', reply_markup = markup) # ForceReply
            bot.register_next_step_handler(sent_message, monthly_income_step)
            break

        else:
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.reply_to(message, '<b>ERROR!</b>\n\nPlease input a single other expense in the format: Name: Amount for x [period]\n\n e.g. Gym_Membership: 200 for 6 months\n\n Where there is no spaces in the name of the other expense, there should be 2 numbers', reply_markup = markup, parse_mode = 'HTML')
            bot.register_next_step_handler(sent_message, other_expenses_step)
            return

    printed_other_expenses = ''

    for expense in user.other_expenses.keys():
        printed_other_expenses += f'{expense}: ${user.other_expenses[expense][0]} for {user.other_expenses[expense][2]} {user.other_expenses[expense][3]}' + '\n' # where {user.other_expenses[expense][0]} is the amount per period, {user.other_expenses[expense][1]} is the number of periods and {user.other_expenses[expense][2]} is the unit of the period

    bot.send_message(chat_id, printed_other_expenses) # sends a message containing all the other expenses that the user inputted earlier on
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True) # multiple choice reply
    markup.add('Yes', 'No')
    sent_message = bot.send_message(chat_id, 'Does the message above correctly display all your other expenses? Please double check and confirm the amount, as well as the number of periods that this amount will be paid during/multiplied by!', reply_markup = markup)
    bot.register_next_step_handler(sent_message, check_other_expenses_step)

def check_other_expenses_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id
    user = users[chat_id] 

    if user_input == 'Yes': # if the user states that the big expenses are correct and all good
        markup = types.ForceReply(selective = False) # for a ForceReply
        sent_message = bot.send_message(chat_id, 'Please input, one by one, your expected monthly income/allowance in the format: Name: Amount (omit the dollar sign!)\n\n e.g. Allowance from parents: 200\n\n NOTE: Whatever you input here should be the income/allowance that you are EXPECTED TO GET EVERY SINGLE MONTH till graduation and does not depend on whether it is during any vacation or internship or not!\n\nPlease input none if you do not have any monthly income/allowance.', reply_markup = markup) # ForceReply
        bot.register_next_step_handler(sent_message, monthly_income_step)

    elif user_input == 'No': # if the user states that the monthly expenses are not correct
        user.other_expenses.clear() # resets the dictionary containing the big expenses
        markup = types.ForceReply(selective = False) # for a ForceReply
        sent_message = bot.reply_to(message, 'Please input your other expenses again, one by one, in the format: Name: Amount for x [period]', reply_markup = markup)
        bot.register_next_step_handler(sent_message, other_expenses_step)

def monthly_income_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id
    user = users[chat_id] 

    while user_input.lower() != 'done':
        if is_valid_income(user_input):
            income_name, income_amount = get_income(user_input)
            user.monthly_income[income_name] = income_amount # stores the name and the amount of the monthly incomes in the dictionary in the user object instance
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.send_message(chat_id, 'Please input your next monthly income/allowance source! If you are done, please input done', reply_markup = markup)
            bot.register_next_step_handler(sent_message, monthly_income_step)
            return

        elif user_input.lower() == 'none': # if the user has no monthly income, move on to the number of months of internship/vacation step
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.send_message(chat_id, 'Please input the total number of months of internships/vacations that you have from now till graduation\n\nPlease input none if you are not expecting to have any internships/vacations at all', reply_markup = markup) # ForceReply
            bot.register_next_step_handler(sent_message, number_of_months_of_internships_and_vacations_step)
            break

        else:
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.reply_to(message, '<b>ERROR!</b>\n\nPlease input a single source of monthly income/allowance in the format: Name: Amount\n\n e.g. Salary from freelance design job: 1000\n\n Where there is at most 1 number (positive)and 1 colon', reply_markup = markup, parse_mode = 'HTML')
            bot.register_next_step_handler(sent_message, monthly_income_step)
            return

    printed_monthly_income = ''

    for income in user.monthly_income.keys():
        printed_monthly_income += f'{income}: ${user.monthly_income[income]}' + '\n'

    bot.send_message(chat_id, printed_monthly_income) # sends a message containing all the monthly income that the user inputted earlier on
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True) # multiple choice reply
    markup.add('Yes', 'No')
    sent_message = bot.send_message(chat_id, 'Does the message above correctly display all your monthly income/allowance sources?', reply_markup = markup)
    bot.register_next_step_handler(sent_message, check_monthly_income_step)

def check_monthly_income_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id
    user = users[chat_id] 

    if user_input == 'Yes': # if the user states that the monthly income are correct and all good
        markup = types.ForceReply(selective = False) # for a ForceReply
        sent_message = bot.send_message(chat_id, 'Please input the total number of months of internships/vacations that you have from now till graduation\n\nPlease input none if you are not expecting to have any internships/vacations at all', reply_markup = markup) # ForceReply
        bot.register_next_step_handler(sent_message, number_of_months_of_internships_and_vacations_step)

    elif user_input == 'No': # if the user states that the monthly income are not correct
        user.monthly_income.clear() # resets the dictionary containing the monthly income
        markup = types.ForceReply(selective = False) # for a ForceReply
        sent_message = bot.reply_to(message, 'Please input your monthly income/allowance again, one by one, in the format: Name: Amount (omit the dollar sign!)', reply_markup = markup)
        bot.register_next_step_handler(sent_message, monthly_income_step)

def number_of_months_of_internships_and_vacations_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id
    user = users[chat_id]

    if user_input.lower() == 'none': # if the user input is none, move on to the other income step
        user.number_of_months_of_internships_and_vacations = 0
        markup = types.ForceReply(selective = False) # for a ForceReply
        sent_message = bot.send_message(chat_id, 'Please input, one by one, your expected other income in the following format: Name: Amount for x [period]\n\nWhere name should be a single word with no spaces, where amount is the amount of income in a single [period], where a [period] can be a month, semester, term, etc., just need to write down a single word in place of the [period], x is a number and omit the dollar sign. E.g. GrabFood_Salary: 1500 for 3 months\n\nOther income are basically income that are not monthly income/allowance that you will receive every month, and are also not the income that you will receive only during internship/vacation period. Other income refer to income that you will receive for a certain number of months/periods during your university life.\n\nPlease input none if you are not expecting to have other income at all', reply_markup = markup) # ForceReply
        bot.register_next_step_handler(sent_message, other_income_step)

    elif not user_input.isdigit(): # if the user input is not an integer >= 0
        markup = types.ForceReply(selective = False) # for a ForceReply
        sent_message = bot.reply_to(message, '<b>ERORR!</b>\n\nThe number of months of internships/vacations should be a positive number with no decimal places!', reply_markup = markup, parse_mode = 'HTML')
        bot.register_next_step_handler(sent_message, number_of_months_of_internships_and_vacations_step)
        return

    user.number_of_months_of_internships_and_vacations = int(user_input)
    markup = types.ForceReply(selective = False) # for a ForceReply
    sent_message = bot.send_message(chat_id, 'Please input, one by one, your expected monthly income during internship/vacation period in the format: Name: Amount (omit the dollar sign!)\n\n e.g. Internship salary: 1500', reply_markup = markup) # ForceReply
    bot.register_next_step_handler(sent_message, internship_vacation_income_step)

def internship_vacation_income_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id
    user = users[chat_id] 

    while user_input.lower() != 'done':
        if is_valid_income(user_input):
            income_name, income_amount = get_income(user_input)
            user.internship_vacation_income[income_name] = income_amount # stores the name and the amount of the internship/vacation incomes in the dictionary in the user object instance
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.send_message(chat_id, 'Please input your next monthly internship/vacation income source! If you are done, please input done', reply_markup = markup)
            bot.register_next_step_handler(sent_message, internship_vacation_income_step)
            return

        else:
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.reply_to(message, '<b>ERROR!</b>\n\nPlease input a single source of monthly internship/vacation income in the format: Name: Amount\n\n e.g. Waiter part time vacation job: 1800\n\n Where there is at most 1 number (positive) and 1 colon', reply_markup = markup, parse_mode = 'HTML')
            bot.register_next_step_handler(sent_message, internship_vacation_income_step)
            return

    printed_internship_vacation_income = ''

    for income in user.internship_vacation_income.keys():
        printed_internship_vacation_income += f'{income}: ${user.internship_vacation_income[income]}' + '\n'

    bot.send_message(chat_id, printed_internship_vacation_income) # sends a message containing all the internship/vacation income that the user inputted earlier on
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True) # multiple choice reply
    markup.add('Yes', 'No')
    sent_message = bot.send_message(chat_id, 'Does the message above correctly display all your internship/vacation income sources?', reply_markup = markup)
    bot.register_next_step_handler(sent_message, check_internship_vacation_income_step)

def check_internship_vacation_income_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id
    user = users[chat_id] 

    if user_input == 'Yes': # if the user states that the monthly internship/vacation income are correct and all good
        markup = types.ForceReply(selective = False) # for a ForceReply
        sent_message = bot.send_message(chat_id, 'Please input, one by one, your expected other income in the following format: Name: Amount for x [period]\n\nWhere name should be a single word with no spaces, where amount is the amount of income in a single [period], where a [period] can be a month, semester, term, etc., just need to write down a single word in place of the [period], x is a number and omit the dollar sign. E.g. GrabFood_Salary: 1500 for 3 months\n\nOther income are basically income that are not monthly income/allowance that you will receive every month, and are also not the income that you will receive only during internship/vacation period. Other income refer to income that you will receive for a certain number of months/periods during your university life.\n\nPlease input none if you are not expecting to have other income at all', reply_markup = markup) # ForceReply
        bot.register_next_step_handler(sent_message, other_income_step)

    elif user_input == 'No': # if the user states that the monthly income are not correct
        user.internship_vacation_income.clear() # resets the dictionary containing the internship/vacation monthly income
        markup = types.ForceReply(selective = False) # for a ForceReply
        sent_message = bot.reply_to(message, 'Please input your expected monthly internship/vacation income again, one by one, in the format: Name: Amount (omit the dollar sign!)', reply_markup = markup)
        bot.register_next_step_handler(sent_message, internship_vacation_income_step)

def other_income_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id
    user = users[chat_id] 

    while user_input.lower() != 'done':
        if is_valid_other_income(user_input):
            income_name, income_amount_number_of_periods = get_other_income(user_input) # where income_amount_number_of_periods is a list [Amount, for , x, [period]]
            user.other_income[income_name] = income_amount_number_of_periods # stores the name and the amount of the other income in the dictionary in the user object instance
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.send_message(chat_id, 'Please input your next other income! If you are done, please input done', reply_markup = markup)
            bot.register_next_step_handler(sent_message, other_income_step)
            return

        elif user_input.lower() == 'none': # if the user has no other income, show the summary message
            if user.i_will_go_broke: # if the user will go broke
            # to create a string such that the bot will send a message that shows the summary of the user's income and expense during his university life
                printed_summary = print_summary(user)
                bot.send_message(chat_id, printed_summary, parse_mode = 'HTML')
                bot.send_message(chat_id, f'<b>OH NO!</b>\n\nYou will go broke by the time you graduate in {user.graduation_date}!\n\nYou will need to cut down your total expenses by ${abs(user.amount_of_expense_to_cut_down)} to not go broke!', parse_mode = 'HTML')

            else: # if the user will not go broke
            # to create a string such that the bot will send a message that shows the summary of the user's income and expense during his university life
                printed_summary = print_summary(user)
                bot.send_message(chat_id, printed_summary, parse_mode = 'HTML')
                bot.send_message(chat_id, f'<b>CONGRATULATIONS!</b>\n\nYou will not go broke by the time you graduate in {user.graduation_date}!\n\nYou will even have ${user.bank_balance_remaining} to spare!', parse_mode = 'HTML')

            break

        else:
            markup = types.ForceReply(selective = False) # for a ForceReply
            sent_message = bot.reply_to(message, '<b>ERROR!</b>\n\nPlease input a single other income in the format: Name: Amount for x [period]\n\n e.g. Tuition_Salary: 400 for 6 months\n\n Where there is no spaces in the name of the other income, there should be 2 numbers', reply_markup = markup, parse_mode = 'HTML')
            bot.register_next_step_handler(sent_message, other_income_step)
            return

    printed_other_income = ''

    for income in user.other_income.keys():
        printed_other_income += f'{income}: ${user.other_income[income][0]} for {user.other_income[income][2]} {user.other_income[income][3]}' + '\n' # where {user.other_income[income][0]} is the amount per period, {user.other_income[income][1]} is the number of periods and {user.other_expenses[income][2]} is the unit of the period

    bot.send_message(chat_id, printed_other_income) # sends a message containing all the other income that the user inputted earlier on
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True) # multiple choice reply
    markup.add('Yes', 'No')
    sent_message = bot.send_message(chat_id, 'Does the message above correctly display all your other income? Please double check and confirm the amount, as well as the number of periods that this amount will be paid during/multiplied by!', reply_markup = markup)
    bot.register_next_step_handler(sent_message, check_other_income_step)

def check_other_income_step(message):
    user_input = message.text # gets the user input
    chat_id = message.chat.id
    user = users[chat_id] 

    if user_input == 'Yes': # if the user states that the other income are correct and all good
        if user.i_will_go_broke: # if the user will go broke
            # to create a string such that the bot will send a message that shows the summary of the user's income and expense during his university life
            printed_summary = print_summary(user)
            bot.send_message(chat_id, printed_summary, parse_mode = 'HTML')
            bot.send_message(chat_id, f'<b>OH NO!</b>\n\nYou will go broke by the time you graduate in {user.graduation_date}!\n\nYou will need to cut down your total expenses by ${abs(user.amount_of_expense_to_cut_down)} to not go broke!', parse_mode = 'HTML')

        else: # if the user will not go broke
            # to create a string such that the bot will send a message that shows the summary of the user's income and expense during his university life
            printed_summary = print_summary(user)
            bot.send_message(chat_id, printed_summary, parse_mode = 'HTML')
            bot.send_message(chat_id, f'<b>CONGRATULATIONS!</b>\n\nYou will not go broke by the time you graduate in {user.graduation_date}!\n\nYou will even have ${user.bank_balance_remaining} to spare!', parse_mode = 'HTML')

    elif user_input == 'No': # if the user states that the monthly income are not correct
        user.other_income.clear() # resets the dictionary containing the other income
        markup = types.ForceReply(selective = False) # for a ForceReply
        sent_message = bot.reply_to(message, 'Please input your other income again, one by one, in the format: Name: Amount for x [period]', reply_markup = markup)
        bot.register_next_step_handler(sent_message, other_income_step)

# /feedback
@bot.message_handler(commands = ['feedback'])
def feedback(message):
    bot.send_message(message.chat.id, 'Please send your feedback/suggestions to: https://forms.gle/LZJALSrDiBuqibN79')

# /githubrepo
@bot.message_handler(commands = ['githubrepo'])
def feedback(message):
    bot.send_message(message.chat.id, 'The GitHub repository of this bot is: https://github.com/Fe-56/Will-I-Go-Broke')

# for any unknwon or unrecognised commands/inputs
@bot.message_handler(content_types = ['text', 'pinned_message'])
def unknown_text(message):
    bot.reply_to(message, "I'm sorry, I do not recognise this command. Would you like to use /help to see all available commands instead?")

# for any media sent to the bot
@bot.message_handler(content_types = ['sticker', 'photo', 'audio', 'document', 'video', 'video_note', 'voice', 'location', 'contact'])
def unknown_media(message):
    bot.send_document(message.chat.id, 'https://i.pinimg.com/originals/b8/83/c2/b883c2fa99c1aa9c2f7c4268fbffde75.gif') # sends a gif of a confused Naruto

bot.infinity_polling()