'''
Handles most of the database logic for the application
'''
import sqlite3
from datetime import date

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
            month INTEGER,
            year INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(ID)
            );''')

c.execute('''CREATE TABLE IF NOT EXISTS items (
            item TEXT,
            percent INTEGER,
            spent REAL,
            user_id INTEGER,
            ID INTEGER PRIMARY KEY,
            FOREIGN KEY(user_id) REFERENCES users(ID)
        );''')

c.execute('''CREATE TABLE IF NOT EXISTS spending (
            month INTEGER,
            day INTEGER,
            year INTEGER,
            spending REAL,
            user_id INTEGER,
            items_id,
            FOREIGN KEY(items_id) REFERENCES items(ID)
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
    try:
        if no_id[0] == compare:
            return True
        else: 
            return False
    except IndexError:
        return False


def get_user_id(username):
    with conn:
        c.execute("SELECT * FROM users where username=:username", {"username": username})
        get_id = c.fetchall()
        id = [info[0] for info in get_id]
    return id[0]


def get_amount_of_money(MoneyAmount, id): 
    today = str(date.today())
    year = int(today[0:4])
    month = int(today[5:7])
    with conn:
        c.execute("SELECT * FROM moneyAmount where user_id=:user_id and month=month and year=year", {'user_id':id, 'month':month, 'year':year})
        check = c.fetchall()
        if len(check) == 1:
            c.execute("DELETE From moneyAmount where user_id=:user_id", {'user_id':id})
            c.execute("INSERT INTO moneyAmount('monthlyAmount', 'savings', 'savings_dollar_amount', 'user_id', 'month', 'year') VALUES (?, ?, ?, ?, ?, ?)",
                (MoneyAmount.monthly_check, MoneyAmount.savings, MoneyAmount.savings_dollar_amount, id, month, year))
        else:
            c.execute("INSERT INTO moneyAmount('monthlyAmount', 'savings', 'savings_dollar_amount', 'user_id', 'month', 'year') VALUES (?, ?, ?, ?, ?, ?)",
                (MoneyAmount.monthly_check, MoneyAmount.savings, MoneyAmount.savings_dollar_amount, id, month, year))
    with conn:
        c.execute("SELECT * FROM items where user_id=:user_id", {'user_id':id})
        check = c.fetchall()
        for item in check:
            pass
            
def display_money(id):
    today = str(date.today())
    year = int(today[0:4])
    month = int(today[5:7])

    with conn:
        c.execute("SELECT * FROM moneyAmount where user_id=:user_id and month=:month and year=:year", {'user_id':id, 'month':month, 'year':year})
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


def update_spending_budget_item(spent, item, just_spent, id):
    with conn:
        today = str(date.today())
        year = int(today[0:4])
        month = int(today[5:7])
        day = int(today[8:10])
        c.execute("UPDATE items set spent = ? where item = ?", (spent, item))
        check = c.fetchone()
        c.execute("select * FROM items where item=:item", {'item':item})
        get_item_id = c.fetchone()

        c.execute("INSERT into spending('month', 'day', 'year', 'spending', 'items_id', 'user_id') VALUES (?, ?, ?, ?, ?, ?)",
            (month, day, year, just_spent, get_item_id[4], id))

        c.execute("select * FROM spending where items_id=:items_id", {'items_id':get_item_id[4]})
        check = c.fetchall()



def delete_budget_item(item, id):
    with conn:
        c.execute("DELETE from items where item=:item and user_id=:user_id", {'item':item, 'user_id':id})

def get_already_spent(item, id):
    c.execute("SELECT * FROM items where item=:item and user_id=:user_id", {'item':item, 'user_id':id})
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

def spending_remaining_chart(id):
     with conn:
        c.execute("SELECT * FROM moneyAmount where user_id=:user_id", {'user_id':id})
        total_amount_to_spend = c.fetchone()
        c.execute("SELECT * FROM items where user_id=:user_id", {'user_id':id})
        spent_on_items = c.fetchall()
        amount_to_spend_left = []
        items = []
        for item in spent_on_items:
            items.append(item[0])
            total_amount_allowed_on_item = total_amount_to_spend[0] * item[1]/100
            amount_to_spend_left.append(total_amount_allowed_on_item - item[2])

        return items, amount_to_spend_left


