# this file is to store the User class, where it stores all the information that the user enters via /plan

class User:
    def __init__(self, name):
        self._name = name
        self._current_bank_balance = 0
        self._graduation_date = None
        self._school_fees_per_period = 0
        self._number_of_periods_to_pay_school_fees = 0
        self._monthly_expenses = dict() # creates a dictionary to store the monthly expenses of the user, where the keys are the name of the expenses and the values are the amount of the expenses
        self._big_expenses = dict() # creates a dictionary to store the one-time big expenses of the user, similar concept as the monthly expenses
        self._monthly_income = dict() # creates a dictionary to store the monthly income/allowance of the user, same concept as the monthly expenses
        self._number_of_months_of_internships_and_vacations = 0
        self._internship_vacation_income = dict() # creates a dictionary to store the monthly income of the user only during the internship/vacation periods

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

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
    def school_fees_per_period(self):
        return self._school_fees_per_period

    @school_fees_per_period.setter
    def school_fees_per_period(self, value):
        self._school_fees_per_period = value

    @property
    def number_of_periods_to_pay_school_fees(self):
        return self._number_of_periods_to_pay_school_fees

    @number_of_periods_to_pay_school_fees.setter
    def number_of_periods_to_pay_school_fees(self, value):
        self._number_of_periods_to_pay_school_fees = value

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
    def number_of_months_of_internships_and_vacations(self):
        return self._number_of_months_of_internships_and_vacations

    @number_of_months_of_internships_and_vacations.setter
    def number_of_months_of_internships_and_vacations(self, value):
        self._number_of_months_of_internships_and_vacations = value

    @property
    def internship_vacation_income(self):
        return self._internship_vacation_income

    @internship_vacation_income.setter
    def internship_vacation_income(self, value):
        self._internship_vacation_income = value

    @property
    def months_till_graduation(self): # calculates the amount of time in months between the current time and the graduation month and year
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

    @property
    def expenses_total(self): # gets the total monthly expenses and big one-time expenses from now till graduation
        total_expenses_per_month = sum(self.monthly_expenses.values())
        total_monthly_expenses = total_expenses_per_month * self.months_till_graduation
        total_big_expenses = sum(self.big_expenses.values())
        return total_monthly_expenses + total_big_expenses + self.expenses_total_school_fees_left_to_pay

    @property
    def income_total(self): # gets the total monthly income and internship/vacation income from now till graduation
        total_income_per_month = sum(self.monthly_income.values())
        total_monthly_income = total_income_per_month * self.months_till_graduation
        total_internship_vacation_income_per_month = sum(self.internship_vacation_income.values())
        total_internship_vacation_income = total_internship_vacation_income_per_month * self.number_of_months_of_internships_and_vacations
        return total_monthly_income + total_internship_vacation_income

    @property
    def i_will_go_broke(self): # gets a boolean on whether this User object will go broke or not by the time he graduates, based on his total expenses and income
        change_in_bank_balance = self.income_total - self.expenses_total
        return (self.current_bank_balance + change_in_bank_balance) <= 0 # returns a boolean

    @property
    def bank_balance_remaining(self): # returns the bank balance remaining if the user will not go broke
        change_in_bank_balance = self.income_total - self.expenses_total
        return self.current_bank_balance + change_in_bank_balance

    @property
    def amount_of_expense_to_cut_down(self): # returns the amount of expenses to be cut down in order not to go broke given the current income; the formula is the same as bank_balance_remaining, only difference is in the name of the computed property to avoid confusion
        change_in_bank_balance = self.income_total - self.expenses_total
        return self.current_bank_balance + change_in_bank_balance