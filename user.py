# this file is to store the User class, where it stores all the information that the user enters via /plan

class User:
    def __init__(self, name):
        self._name = name
        self._graduation_date = None
        self._current_bank_balance = 0
        self._monthly_expenses = dict() # creates a dictionary to store the monthly expenses of the user, where the keys are the name of the expenses and the values are the amount of the expenses
        self._big_expenses = dict() # creates a dictionary to store the one-time big expenses of the user, similar concept as the monthly expenses
        self._monthly_income = dict() # creates a dictionary to store the monthly income/allowance of the user, same concept as the monthly expenses

    @property
    def name(self):
        return self._name

    @property
    def current_bank_balance(self):
        return self._current_bank_balance

    @current_bank_balance.setter
    def current_bank_balance(self, value):
        self._current_bank_balance = value

    @property
    def graduation_date(self):
        return self._graduation_date

    @graduation_date.setter
    def graduation_date(self, value):
        self._graduation_date = value

    @property
    def monthly_expenses(self):
        return self._monthly_expenses

    @monthly_expenses.setter
    def monthly_expenses(self, value):
        self._monthly_expenses = value

    @property
    def big_expenses(self):
        return self._big_expenses

    @big_expenses.setter
    def big_expenses(self, value):
        self._big_expenses = value

    @property
    def monthly_income(self):
        return self._monthly_income

    @monthly_income.setter
    def monthly_income(self, value):
        self._monthly_income = value

    @property
    def time_from_now_till_graduation(self): # calculates the amount of time in months between the current time and the graduation month and year
        from datetime import datetime
        current_month = datetime.now().month # gets the current month
        current_year = datetime.now().year # gets the current year

        if int(self.graduation_date[3:]) == current_year: # if the graduation year is the same as the current year
            return int(self.graduation_date[:2]) - current_month

        else: # if the graduation year is after the current year
                return (12 - current_month) + (12 * (int(self.graduation_date[3:]) - current_year - 1)) + int(self.graduation_date[:2])

    @property
    def expenses_total_school_fees_left_to_pay(self): # gets the total amount of school fees the user has to pay from now tll graduation
        return self.school_fees_per_period * self.number_of_periods_to_pay_school_fees

    