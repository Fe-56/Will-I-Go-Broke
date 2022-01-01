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

        else: # check whether the graduation date is after the current date
            from datetime import datetime
            current_month = datetime.now().month # gets the current month
            current_year = datetime.now().year # gets the current year

            if int(input[3:]) == current_year: # compares the graduation year to the current year
                if int(input[:2]) <= current_month: # compares the graduaton month to the current month
                    return False # reach here if the current year is the same as the graduation year and the current month is after the graduation month

            elif int(input[3:]) < current_year:
                return False

            return True

def is_valid_expense(input): # this function checks if input is a valid (monthly) expense in the format: Name: Amount
    if input.count(':') != 1:
        return False

    else:
        colon_index = input.index(':') # gets the index of the colon, :

        if input[colon_index + 1] != ' ': # if the character right after the colon : is not an empty space
            return False

        elif not is_valid_amount(input[colon_index + 2:]): # if the characters right after the space right after the colon: is not a valid amount of money
            return False

    return True

def get_expense(input):
    colon_index = input.index(':') # gets the index of the colon, :
    expense_name = input[:colon_index] # gets the name of the expense
    expense_amount = input[colon_index + 2:] # gets the amount of the expense
    return expense_name, float(expense_amount)

def is_valid_income(input): # this function is just the same as  the is_valid_exense() function, the only difference is in the name, where this function is used to check if it is a valid monthly income in the format: Name: Amount, to avoid confusion in main.py
    if input.count(':') != 1:
        return False

    else:
        colon_index = input.index(':') # gets the index of the colon, :

        if input[colon_index + 1] != ' ': # if the character right after the colon : is not an empty space
            return False

        elif not is_valid_amount(input[colon_index + 2:]): # if the characters right after the space right after the colon: is not a valid amount of money
            return False

    return True

def get_income(input):
    colon_index = input.index(':') # gets the index of the colon, :
    income_name = input[:colon_index] # gets the name of the income
    income_amount = input[colon_index + 2:] # gets the amount of the income
    return income_name, float(income_amount)