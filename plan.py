# This file contains all the specific functions necessary for the /plan command

def is_valid_amount(input): # this function checks if input is a valid amount of money or not
    decimal_count = 0

    for character in input:
        if character not in '0123456789.': # '0123456789.' are the only valid characters in a valid amount of money
            return False

        else:
            if character == '.':
                decimal_count += 1 # counts the number of decimal dots

    if decimal_count <= 1:
        if input[0] == '.' or input[-1] == '.':
            return False # last or first character must not be a decimal point

        else:
            return True

    else:
        return False # since a valid amount of money should only have at most 1 decimal point

def is_valid_date(input): # this function checks if input is a valid date in the format: MM/YYYY
    slash_count = 0

    if len(input) != 7: # since the valid date is in the format: MM/YYYYYY, which has 7 characters
        return False 

    for character in input:
        if character not in '0123456789/': # '0123456789/' are the only valid characters in a valid date
            return False

        else:
            if character == '/':
                slash_count += 1 # counts the number of slashes

    if slash_count != 1:
        return False

    else:
        if input[0] == '/' or input[-1] == '/':
            return False # the first or last character must not be a slash

        else:
            return True

# def current_bank_balance_step(message):
#     user_input = message.text # gets the user input

#     if not is_valid_amount(user_input): # if the user input is not a valid amount of money
#         sent_message = bot.reply_to(message, 'The initial bank balance should only consist of digits and a maxumum of one decmial point')
#         bot.register_next_step_handler(sent_message, current_bank_balance_step)
#         return

#     user = users[message.chat.id] # gets the user object instance from the users dictionary
#     user.current_bank_balance = user_input # since the user_input at this point is a valid amount of money
#     markup = types.ForceReply(selective = False) # for a ForceReply
#     sent_message = bot.send_message(message, 'When are you expected to graduate? Please input the month and year in this format: MM/YYYY, e.g. 01/2025 for January 2025', reply_markup = markup) # ForceReply
#     bot.register_next_step_handler(sent_message, graduation_date_step)

# def graduation_date_step(message):
#     user_input = message.text # gets the user input

#     if not is_valid_date(user_input): # if the user input is not a valid date in the format: MM/YYYY
#         sent_message = bot.reply_to(message, 'The expected graduation date should only consists of digits in the format: MM/YYYY')
#         bot.register_next_step_handler(sent_message, graduation_date_step)
#         return

#     user = user[message.chat.id] # gets the user object instance from the users dictionary
#     user.graduation_date = user_input

#     '''Code for calculating the amount of time in weeks/months between the current time and the user's graduation date'''

#     bot.send_message(message.chat.id, f'Your username is {user.name}, your current bank balance is {user.current_bank_balance} and your expected graduation date is {user.graduation_date}')