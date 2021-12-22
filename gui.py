'''
Budgeting app that shows how much a user can spend based on what percentage 
of their paycheck they allocate to that sector
'''
import tkinter as tk
from models import User, MoneyAmount
from database import create_user, verify_login

# Set current user to none and changes it once a valid login occurs
CURRENT_USER = None

class BuildPage(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.replace_frame(LoginPage)
    
    def replace_frame(self, frame_class):
        '''Destroys current frame and replaces it with a new one.'''
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class LoginPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text='test').pack()
        self.username = tk.Entry(self)
        self.username.insert(0, 'Username')
        self.username.pack()
        self.password = tk.Entry(self)
        self.password.insert(0, 'Password')
        self.password.pack()

        def get_user():
            username = self.username.get()
            password = self.password.get()
            user = User(username, password)
            value = verify_login(user)
            global CURRENT_USER
            CURRENT_USER = user
            if value == True:
                return parent.replace_frame(HomePage)
            else: 
                tk.Label(self, text="Invalid login information").pack()
  
        tk.Button(self, text="Login", 
            command=get_user).pack()
        tk.Button(self, text="New User", 
            command=lambda: parent.replace_frame(RegisterPage)).pack()


class RegisterPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Register page")
        self.password = tk.Entry(self)
        self.user = tk.Entry(self)
        self.user.insert(0, 'New Username')
        self.password.insert(0, 'New Code 6 Numbers!')
        self.user.pack()
        self.password.pack()

        def get_info():
            username = self.user.get()
            password = self.password.get()
            user = User(username, password)
            value = create_user(user)
            if value == True:
                return parent.replace_frame(LoginPage)
            else:
                tk.Label(self, text="Username might be taken").pack()

        tk.Button(self, text="Submit", command=get_info).pack()

        
class HomePage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Home Page").pack()
        tk.Label(self, text=f"{CURRENT_USER.username} welcome!").pack()
        tk.Button(self, text="Fresh Start", 
            command=lambda: parent.replace_frame(GetInfoPage)).pack()
        tk.Button(self, text="Signout", 
            command=lambda: parent.replace_frame(LoginPage)).pack()

class GetInfoPage(tk.Frame):
    '''Gets how much user will make that month, asks them how much they want to 
    spend on each sector,and the percentage amount they want to save. '''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Put monthly paycheck and savings").pack()
        self.monthlyPay = tk.Entry(self)
        self.monthlyPay.pack()
        self.savings = tk.Entry(self)
        self.savings.pack()

        try:
            def fresh_start():
                monthlyPay = self.monthlyPay.get()   
                savings = self.savings.get()
                money = MoneyAmount(monthlyPay, savings, CURRENT_USER) 
                print(money)
        except:
            pass

        tk.Label(text="Invalid Entry")
        tk.Button(self, text="Submit", command=fresh_start).pack()
        tk.Button(self, text="Home Page", 
            command=lambda: parent.replace_frame(HomePage)).pack()


if __name__ == '__main__':
    window = BuildPage()
    window.geometry("250x250")
    window.config(bg="lightblue")
    window.title("Budgeting App")
    window.mainloop()

    