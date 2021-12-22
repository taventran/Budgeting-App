import sqlite3
from models import User

conn = sqlite3.connect('budget.db')
c = conn.cursor()
    

"""
c.execute('''CREATE TABLE users (
            username text,
            password text
            )''')
"""

# c.execute("INSERT INTO users VALUES (:username, :password)", {'username':emp_2.username, 'password':emp_2.password })

def create_user(User):
    username = User.username
    password = User.password
    c.execute("SELECT * FROM users where username=:username", {"username": username})
    check = c.fetchall()
    if len(check) == 0:
        with conn:
            c.execute("INSERT INTO users VALUES (:username, :password)", 
                    {'username':username, 'password':password })
        return True
    else:
        return False

def verify_login(User):
    username = User.username
    password = User.password
    compare = (username, password)
    c.execute("SELECT * FROM users where username=:username", {"username": username})
    check = c.fetchall()
    if check[0] == compare:
        return True
    else: 
        return False
    




