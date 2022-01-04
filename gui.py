'''
Budgeting app that shows how much a user can spend based on what percentage 
of their paycheck they allocate to that sector
'''
import tkinter as tk
from graphs import display_pie_chart
from models import User, MoneyAmount, BudgetItem
from database import create_user, show_budget_items, update_spending_budget_item, get_already_spent
from database import verify_login, get_user_id, get_amount_of_money, display_money, get_budget_item, show_budget_items


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
        self._frame.grid()

class LoginPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text='Login', font=("Cambria", 26)).grid(row=1, column=1)
        self.username = tk.Entry(self, font=("Cambria", 12))
        self.username.insert(0, 'Username')
        self.username.grid(row=2, column=1)
        self.password = tk.Entry(self, font=("Cambria", 12))
        self.password.insert(0, 'Password')
        self.password.grid(row=3, column=1)
        self.invalid = tk.Label(self, text="Information not valid", font=("Cambria", 12))
        self.invalid.grid(row=4, column=1)
        self.invalid.grid_remove()

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
                self.invalid.grid(row=5, column=1)
  
        tk.Button(self, text="Login", 
            command=get_user, font=("cambria", 15)).grid(row=6, column=1)
        tk.Button(self, text="New User", 
            command=lambda: parent.replace_frame(RegisterPage), font=("cambria", 15)).grid(row=7, column=1)

class RegisterPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Register page", font=("Cambria", 26)).pack()
        self.password = tk.Entry(self, font=("Cambria", 12))
        self.user = tk.Entry(self, font=("Cambria", 12))
        self.user.insert(0, 'New Username')
        self.password.insert(0, 'New Code 6 Numbers!')
        self.user.pack(pady=10)
        self.password.pack(pady=10)
        self.invalid = tk.Label(self, text="Username already taken", font=("Cambria", 12))
        self.invalid.pack()
        self.invalid.pack_forget()

        def get_info():
            username = self.user.get()
            password = self.password.get()
            user = User(username, password)
            value = create_user(user)
            if value == True:
                return parent.replace_frame(LoginPage)
            else:
                self.invalid.pack()

        tk.Button(self, text="Submit", command=get_info, font=("Cambria", 12)).pack()
        

class HomePage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Home Page", font=("Cambria", 26)).grid(row=1, column=10)
        tk.Label(self, text=f"{CURRENT_USER.username} welcome!", font=("Cambria", 15)).grid(row=2, column=10)
        id = get_user_id(CURRENT_USER.username)
        info = display_money(id)

        if len(info) > 0:
            monthly_allowance = [allowance[0] for allowance in info]
            savings = [save[1] for save in info]
            savings_in_dollars = [dollar_amount[2] for dollar_amount in info]
            information = tk.Label(self, text=f"Monthly Paycheck {monthly_allowance[0]:.2f}").grid(row=3, column=10)
            information2 = tk.Label(self, text=f"Saving {savings[0]}% this month").grid(row=3, column=10)
            information3 = tk.Label(self, text=f"Saving {savings_in_dollars[0]:.2f}$ this month").grid(row=4, column=10)
            display_pie_chart(id, window)
            tk.Button(self, text="Budget Item", font=("Cambria", 15),
                command=lambda: parent.replace_frame(BudgetItemPage)).grid(row=5, column=10)
            tk.Button(self, text="Update Item Spending", font=("Cambria", 15),
                command=lambda: parent.replace_frame(UpdateSpending)).grid(row=6, column=10)

        tk.Button(self, text="Monthly Paycheck", font=("Cambria", 15),
            command=lambda: parent.replace_frame(MonthlyAllowancePage)).grid(row=7, column=10)
        tk.Button(self, text="Signout", font=("Cambria", 15),
            command=lambda: parent.replace_frame(LoginPage)).grid(row=8, column=10)
    

class MonthlyAllowancePage(tk.Frame):
    '''Gets how much user will make that month, and the percentage amount they want to save. '''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(text= "Updating monthly allowance will delete all of your budget items for this month, and how much you spent!").pack()
        tk.Label(self, text="Put monthly paycheck and savings", font=("Cambria", 26)).grid(pady=10)
        self.monthlyPay = tk.Entry(self, font=("Cambria", 12))
        self.monthlyPay.insert(0, 'Monthly Paycheck')
        self.monthlyPay.pack(pady=10)
        self.savings = tk.Entry(self, font=("Cambria", 12))
        self.savings.insert(0, 'Percent you want to save')
        self.savings.pack(pady=10)
        self.error = tk.Label(self, text="Monthly pay needs to be a number and savings need to be a positive whole number!", font=("Cambria", 12))
        def get_info():
            try:
                monthlyPay = float(self.monthlyPay.get())   
                savings = int(self.savings.get())
                if (savings < 0) or (savings > 100):
                    tk.Label(self, text="Savings needs to be a whole number between 0 and 100").pack()
                else:
                    money = MoneyAmount(monthlyPay, savings, CURRENT_USER.username)
                    id = get_user_id(money.user)
                    print(id)
                    get_amount_of_money(money, id)
                    self.error.destroy()
                    return parent.replace_frame(HomePage)
            except ValueError:
                self.error.pack(pady=10)

        tk.Label(text="Invalid Entry")
        tk.Button(self, text="Submit", command=get_info, font=("Cambria", 15)).pack(pady=10)
        tk.Button(self, text="Home Page", font=("Cambria", 15),
            command=lambda: parent.replace_frame(HomePage)).pack(pady=10)


class BudgetItemPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Insert new budgeting item!", font=("Cambria", 25))
        self.item = tk.Entry(self, font=("Cambria", 12))
        self.item.insert(0, 'Budgeting item')
        self.item.pack()
        self.percent = tk.Entry(self, font=("Cambria", 12))
        self.percent.insert(0, 'Percent to spend on the item')
        self.percent.pack()
        id = get_user_id(CURRENT_USER.username)
        info = display_money(id)
        monthly_allowance = [allowance[0] for allowance in info]

        def get_info():
            item = self.item.get()
            percent = self.percent.get()
            allowed_to_spend = monthly_allowance[0] * (int(percent)/100)
            budget_class = BudgetItem(item, percent, allowed_to_spend)
            get_budget_item(budget_class, id)
            return parent.replace_frame(HomePage)


        tk.Button(self, text="Submit",
            command=get_info).pack()
        tk.Button(self, text="Home Page",
            command= lambda: parent.replace_frame(HomePage)).pack()


class UpdateSpending(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Update Spending for Budget Items").pack()
        self.spent = tk.Entry(self)
        self.spent.pack()
        self.spent.pack_forget()
        id = get_user_id(CURRENT_USER.username)
        items = show_budget_items(id)

        def get_spent(item):
            just_spent = float(self.spent.get())
            total_spent = just_spent + get_already_spent(item)
            update_spending_budget_item(total_spent, item)
            return parent.replace_frame(HomePage)

        def get_item(item):
            tk.Label(text=f'How much did you spend on {item[0]} today?')
            self.spent.pack()
            tk.Button(self, text="submit", command = lambda: get_spent(item[0])).pack()
        
        for item in items:  
            button = tk.Button(self, text=f'{item}', command= get_item(item)).pack() 

        tk.Button(self, text="Home", command=lambda: parent.replace_frame(HomePage)).pack()

class Chart(tk.Frame):
    pass



if __name__ == '__main__':
    window = BuildPage()
    window.geometry("750x500")
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.config(bg="lightblue")
    window.title("Budgeting App")
    window.mainloop()

    