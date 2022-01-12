'''
Create class models that will be used by gui.py to organize how the information will be created by the database
'''
from datetime import date

class User():
    '''User class'''
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f"{self.username}"


class MoneyAmount():
    def __init__(self, monthly_check, savings, user):
        self.monthly_check = monthly_check
        self.savings = savings
        self.savings_dollar_amount =  monthly_check * (self.savings/100)
        self.user = user
    
    def __repr__(self):
        return f"{self.user}"



class BudgetItem():
    def __init__(self, item, percentages, amount_spent=0):
        self.item = item
        self.percentages = percentages
        self.amount_spent = amount_spent



class Date():
    pass

