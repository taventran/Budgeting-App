import sqlite3
from models import User, MoneyAmount

conn = sqlite3.connect(':memory:')
c = conn.cursor()
    
c.execute('''CREATE TABLE IF NOT EXISTS users (
            ID INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
            );''')

c.execute('''CREATE TABLE IF NOT EXISTS moneyAmount (
            monthlyAmount real,
            savings real,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(ID)
            );''')

def create_user(User):
    new_username = User.username
    new_password = User.password
    c.execute("SELECT * FROM users where username=:username", {"username": new_username})
    check = c.fetchall()
    if len(check) == 0:
        with conn:
            c.execute("INSERT INTO users('username', 'password') VALUES (?, ?)", 
                     (new_username, new_password))
        return True
    else:
        return False

def verify_login(User):
    username = User.username
    password = User.password
    compare = (username, password)
    c.execute("SELECT * FROM users where username=:username", {"username": username})
    check = c.fetchall()
    no_id = [info[1:3] for info in check]
    if no_id[0] == compare:
        return True
    else: 
        return False

def get_user_id(username):
    c.execute("SELECT * FROM users where username=:username", {"username": username})
    get_id = c.fetchall()
    id = [info[0] for info in get_id]
    return id[0]

def get_amount_of_money(MoneyAmount, id):
    with conn:
        c.execute("INSERT INTO moneyAmount('monthlyAmount', 'savings', 'user_id') VALUES (?, ?, ?)",
                (MoneyAmount.monthly_check, MoneyAmount.savings, id))
    c.execute("SELECT * FROM moneyAmount where user_id=:user_id", {'user_id':id})
    check = c.fetchall()
    print(check)

def display_money():
    pass
