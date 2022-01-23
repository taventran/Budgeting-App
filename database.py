'''
Handles most of the database logic for the application
'''
import sqlite3
from datetime import datetime

conn = sqlite3.connect('database.db')
c = conn.cursor()
    
c.execute('''CREATE TABLE IF NOT EXISTS users (
            ID INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
            );''')

c.execute('''CREATE TABLE IF NOT EXISTS moneyAmount (
            monthlyAmount real,
            savings INTEGER,
            savings_dollar_amount real,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(ID)
            );''')

c.execute('''CREATE TABLE IF NOT EXISTS items (
            item TEXT,
            percent INTEGER,
            spent REAL,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES USER(ID)
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
    try:
        if no_id[0] == compare:
            return True
        else: 
            return False
    except IndexError:
        return False


def get_user_id(username):
    c.execute("SELECT * FROM users where username=:username", {"username": username})
    get_id = c.fetchall()
    id = [info[0] for info in get_id]
    print(id)
    return id[0]


def get_amount_of_money(MoneyAmount, id):
    money = 0    
    with conn:
        c.execute("SELECT * FROM moneyAmount where user_id=:user_id", {'user_id':id})
        check = c.fetchall()
        if len(check) == 1:
            c.execute("DELETE From moneyAmount where user_id=:user_id", {'user_id':id})
            c.execute("INSERT INTO moneyAmount('monthlyAmount', 'savings', 'savings_dollar_amount', 'user_id') VALUES (?, ?, ?, ?)",
                (MoneyAmount.monthly_check, MoneyAmount.savings, MoneyAmount.savings_dollar_amount, id))
        else:
            c.execute("INSERT INTO moneyAmount('monthlyAmount', 'savings', 'savings_dollar_amount', 'user_id') VALUES (?, ?, ?, ?)",
                (MoneyAmount.monthly_check, MoneyAmount.savings, MoneyAmount.savings_dollar_amount, id))
    with conn:
        c.execute("SELECT * FROM items where user_id=:user_id", {'user_id':id})
        check = c.fetchall()
        for item in check:
            pass
            


def display_money(id):
    with conn:
        c.execute("SELECT * FROM moneyAmount where user_id=:user_id", {'user_id':id})
        check = c.fetchall()
    return(check)


def get_budget_item(BudgetItem, id):
    with conn:
        c.execute("INSERT INTO items('item', 'percent', 'spent', 'user_id') VALUES (?, ?, ?, ?)",
                    (BudgetItem.item, BudgetItem.percentages, BudgetItem.amount_spent, id))


def show_budget_items(id):
    c.execute("SELECT * FROM items where user_id=:user_id", {'user_id':id})
    check = c.fetchall()
    return check


def update_spending_budget_item(spent, item):
    with conn:
        c.execute("UPDATE items set spent = ? where item = ?", (spent, item))

    check = c.fetchall()
    return check


def delete_budget_item(item):
    with conn:
        c.execute("DELETE from items where item=:item", {'item':item})

def get_already_spent(item):
    c.execute("SELECT * FROM items where item=:item", {'item':item})
    check = c.fetchone()
    return check[2]

def percentages_for_pie_chart(id):
    c.execute("SELECT * FROM moneyAmount where user_id=:user_id", {'user_id':id})
    savings = c.fetchone()
    c.execute("SELECT * FROM items where user_id=:user_id", {'user_id':id})
    item_percents = c.fetchall()
    return savings, item_percents

def info_for_spending_bar_chart(id):
    with conn:
        c.execute("SELECT * FROM moneyAmount where user_id=:user_id", {'user_id':id})
        total_amount_to_spend = c.fetchone()
        c.execute("SELECT * FROM items where user_id=:user_id", {'user_id':id})
        spent_on_items = c.fetchall()
    return total_amount_to_spend, spent_on_items

