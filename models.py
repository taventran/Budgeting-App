class User():
    '''User class'''
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f"{self.username}"

class BudgetItems():
    pass
