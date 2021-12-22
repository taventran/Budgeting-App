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
        self.user = user
    
    def __repr__(self):
        return f"{self.user}"


class Spending():
    def __init__(self, amount_spent):
        self.amount_spent

