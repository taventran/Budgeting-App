'''
Budgeting app that shows how much a user can spend based on what percentage
of their paycheck they allocate to that sector
'''
import tkinter as tk
from tkinter.constants import BOTTOM
from models import User, MoneyAmount, BudgetItem
from database import create_user, show_budget_items, update_spending_budget_item, get_already_spent, info_for_spending_bar_chart
from database import verify_login, get_user_id, get_amount_of_money, display_money, get_budget_item, show_budget_items, delete_budget_item
from database import spending_remaining_chart
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from database import percentages_for_pie_chart
from datetime import date

# Set current user to none and changes it once a valid login occurs
CURRENT_USER = None

# Set fonts and sizes to be used in the gui
LARGE_TEXT_FONT = ("Cambria", 50)
MEDIUM_TEXT_FONT = ("Cambria", 20)
BUTTON_FONT = ("Cambria", 15)
ENTRY_BOXES_WIDTH = 30
HOME_BUTTON_WIDTH = 40
REGISTER_BUTTON_WIDTH = 25
ITEM_BUTTON_WIDTH = 30

class BuildPage(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.replace_frame(LoginPage)
    
    def replace_frame(self, frame_class):
        # Destroys current frame and replaces it with a new one.
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class LoginPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg='lightblue')
        tk.Label(self, text='Login', font=("Cambria", 26), bg='lightblue').pack(pady=5)
        self.username = tk.Entry(self, font=MEDIUM_TEXT_FONT, width=ENTRY_BOXES_WIDTH)
        self.username.insert(0, 'Username')
        self.username.pack(pady=2)
        self.password = tk.Entry(self, font=MEDIUM_TEXT_FONT, width=ENTRY_BOXES_WIDTH)
        self.password.insert(0, 'Password')
        self.password.config(show="*")
        self.password.pack(pady=2)
        self.invalid = tk.Label(self, text="Information not valid", font=("Cambria", 12))
        self.invalid.pack(pady=5)
        self.invalid.pack_forget()

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
                self.invalid.pack()
  
        tk.Button(self, text="Login", width=REGISTER_BUTTON_WIDTH,
            command=get_user, font=BUTTON_FONT).pack(pady=5)
        tk.Button(self, text="New User", width=REGISTER_BUTTON_WIDTH,
            command=lambda: parent.replace_frame(RegisterPage), font=BUTTON_FONT).pack(pady=5)

class RegisterPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg='lightblue')
        tk.Label(self, text="Register page", font=("Cambria", 26), bg="lightblue").pack()
        self.password = tk.Entry(self, font=MEDIUM_TEXT_FONT)
        self.user = tk.Entry(self, font=MEDIUM_TEXT_FONT)
        self.user.insert(0, 'New Username')
        self.password.insert(0, 'New Password')
        self.user.pack(pady=10)
        self.password.pack(pady=10)
        self.invalid = tk.Label(self, text="Username already taken", font=MEDIUM_TEXT_FONT)
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

        tk.Button(self, text="Submit", command=get_info, width=REGISTER_BUTTON_WIDTH,
            font=BUTTON_FONT).pack(pady=5)
        tk.Button(self, text="Login Page", width=REGISTER_BUTTON_WIDTH,
            command=lambda: parent.replace_frame(LoginPage), font=BUTTON_FONT).pack(pady=5)
        

class HomePage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg='lightblue')
        tk.Label(self, text="Home Page", font=LARGE_TEXT_FONT, bg='lightblue').pack()
        tk.Label(self, text=f"{CURRENT_USER.username} welcome!", font=LARGE_TEXT_FONT, bg='lightblue').pack()
        tk.Label(self, text=date.today(), font=MEDIUM_TEXT_FONT, bg='lightblue').pack()
        id = get_user_id(CURRENT_USER.username)
        info = display_money(id)

        if len(info) > 0:
            monthly_allowance = [allowance[0] for allowance in info]
            savings = [save[1] for save in info]
            savings_in_dollars = [dollar_amount[2] for dollar_amount in info]
            information = tk.Label(self, text=f"Monthly Paycheck {monthly_allowance[0]:.2f}", 
                bg='lightblue', font=MEDIUM_TEXT_FONT).pack()
            information3 = tk.Label(self, text=f"Saving {savings_in_dollars[0]:.2f}$ this month", 
                bg='lightblue', font=MEDIUM_TEXT_FONT).pack()

            tk.Button(self, text="Add Budget Item", font=("Cambria", 15), width=HOME_BUTTON_WIDTH,
                relief="raised", command=lambda: parent.replace_frame(BudgetItemPage)).pack(pady=5)
            tk.Button(self, text="Update Item Spending", font=("Cambria", 15), width=HOME_BUTTON_WIDTH,
                relief="raised", command=lambda: parent.replace_frame(UpdateSpending)).pack(pady=5)
            tk.Button(self, text="Graphs", font=("Cambria", 15), width=HOME_BUTTON_WIDTH,
                relief="raised", command=lambda: parent.replace_frame(Charts)).pack(pady=5)

        tk.Button(self, text="Allotted amount to spend this month", font=("Cambria", 15), width=HOME_BUTTON_WIDTH,
            relief="raised", command=lambda: parent.replace_frame(MonthlyAllowancePage)).pack(pady=5)
        tk.Button(self, text="Signout", font=("Cambria", 15), width=HOME_BUTTON_WIDTH,
            relief="raised", command=lambda: parent.replace_frame(LoginPage)).pack(pady=5)
        
    

class MonthlyAllowancePage(tk.Frame):
    '''Gets how much user will make that month, and the percentage amount they want to save. '''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg='lightblue')
        tk.Label(self, text="Allotted amount to spend this month and savings", font=("Cambria", 26), bg='lightblue').pack(pady=10)
        self.monthlyPay = tk.Entry(self, width=ENTRY_BOXES_WIDTH, font=MEDIUM_TEXT_FONT)
        self.monthlyPay.insert(0, 'Monthly Paycheck')
        self.monthlyPay.pack(pady=10)
        self.savings = tk.Entry(self, font=MEDIUM_TEXT_FONT, width=ENTRY_BOXES_WIDTH)
        self.savings.insert(0, 'Percent you want to save')
        self.savings.pack(pady=10)
        self.error = tk.Label(self, text="Monthly pay needs to be a number and savings need to be a positive whole number!", font=("Cambria", 12))
        def get_info():
            try:
                monthlyPay = float(self.monthlyPay.get())   
                savings = int(self.savings.get())
                if (savings < 0) or (savings > 100):
                    tk.Label(self, text="Savings needs to be a whole number between 0 and 100").pack(pady=10)
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
        tk.Button(self, text="Submit", command=get_info, font=BUTTON_FONT).pack(pady=10)
        tk.Button(self, text="Home Page", font=BUTTON_FONT,
            command=lambda: parent.replace_frame(HomePage)).pack(pady=10)



class BudgetItemPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg='lightblue')
        tk.Label(self, text="Insert new budgeting item!", font=("Cambria", 25), bg='lightblue').pack(pady=10)
        self.item = tk.Entry(self, width=ENTRY_BOXES_WIDTH, font=("Cambria", 20))
        self.item.insert(0, 'Budgeting item')
        self.item.pack(pady=10)
        self.percent = tk.Entry(self, width=ENTRY_BOXES_WIDTH, font=("Cambria", 20))
        self.percent.insert(0, 'Percent to spend on the item')
        self.percent.pack(pady=10)
        id = get_user_id(CURRENT_USER.username)
        info = display_money(id)
        monthly_allowance = [allowance[0] for allowance in info]

        def get_info():
            item = self.item.get()
            percent = self.percent.get()
            budget_class = BudgetItem(item, percent)
            get_budget_item(budget_class, id)
            return parent.replace_frame(HomePage)


        tk.Button(self, text="Submit",
            command=get_info, width=ITEM_BUTTON_WIDTH).pack(pady=10)
        tk.Button(self, text="Home Page",
            command= lambda: parent.replace_frame(HomePage), width=ITEM_BUTTON_WIDTH).pack(pady=10)


class UpdateSpending(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg='lightblue')
        tk.Label(self, text="Update Spending for Budget Items", bg='lightblue', font = MEDIUM_TEXT_FONT).pack(pady=10)
        self.spent = tk.Entry(self, width = ENTRY_BOXES_WIDTH)
        self.spent.pack()
        self.spent.pack_forget()
        id = get_user_id(CURRENT_USER.username)
        items  = show_budget_items(id)
        self.error = tk.Label(self, text="Needs to be a number!")
        def get_spent(item):
            try:
                just_spent = float(self.spent.get())
                total_spent = just_spent + get_already_spent(item, id)
                update_spending_budget_item(total_spent, item, just_spent, id)
                self.error.destroy()
                return parent.replace_frame(HomePage)
            except ValueError:
                self.error.pack()

        def get_item(item):
            tk.Button(self, font =  BUTTON_FONT, width = ITEM_BUTTON_WIDTH, text=f"update spending {item[0]}", command = lambda: update_item(item[0])).pack(pady=10)
            tk.Button(self, font =  BUTTON_FONT, width = ITEM_BUTTON_WIDTH, text=f"delete {item[0]}", command = lambda: delete_item(item[0])).pack(pady=10)
            return item

        def delete_item(item):
            tk.Button(self, font =  BUTTON_FONT, width = ITEM_BUTTON_WIDTH,  text=f"delete {item} item?", command = lambda: [delete_budget_item(item, id), parent.replace_frame(UpdateSpending)]).pack(pady=10)

        def update_item(item):
            self.spent.config(width = 40, font=('cambria', 15))
            self.spent.insert(0, f'How much did you spend on {item} today?')
            self.spent.pack(pady=10)
            tk.Button(self, font =  BUTTON_FONT, width = ITEM_BUTTON_WIDTH,  text="submit", command = lambda: [get_spent(item), parent.replace_frame(UpdateSpending)]).pack(pady=10)

        for item in items:  
            get_item(item)

        tk.Button(self, font =  BUTTON_FONT, width = ITEM_BUTTON_WIDTH,  text="Home", command=lambda: parent.replace_frame(HomePage)).pack(pady=10)

class Charts(tk.Frame):
    '''All the stats for the budgeting app will be shown here'''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg='lightblue')
        tk.Label(self, text="Graphs and Charts of your Spending", bg="lightblue", font=MEDIUM_TEXT_FONT).pack()
        id = get_user_id(CURRENT_USER.username)
        '''Create Percent Budget Graph'''
        saving, item_percents = percentages_for_pie_chart(id)
        item_percentages = [saving[1]]
        labels = ['Savings']
        for item in item_percents:
            item_percentages.append(item[1])
            labels.append(item[0])
        empty = 0
        for item in item_percentages:
            empty += item
        if empty != 100:
            unassigned = 100 - empty
            item_percentages.append(unassigned)
            labels.append('Unassigned')
        fig = Figure(figsize=(5,5), dpi = 100)
        plot1 = fig.add_subplot(111)
        plot1.pie(item_percentages, labels=labels, wedgeprops={'edgecolor': 'black'}, 
            shadow=True, autopct='%1.1f%%')

        
        self.canvas = FigureCanvasTkAgg(fig, master = window)
        self.toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=False)
        self.canvas.get_tk_widget().pack(side = BOTTOM)
        self.toolbar.update()
        self.toolbar.pack(side=BOTTOM)

        def percent_budget_graph():
            '''Create Percent Budget Graph'''
            self.canvas.get_tk_widget().pack_forget()
            self.toolbar.pack_forget()
            saving, item_percents = percentages_for_pie_chart(id)
            item_percentages = [saving[1]]
            labels = ['Savings']
            for item in item_percents:
                item_percentages.append(item[1])
                labels.append(item[0])
            empty = 0
            for item in item_percentages:
                empty += item
            if empty != 100:
                unassigned = 100 - empty
                item_percentages.append(unassigned)
                labels.append('Unassigned')
            fig = Figure(figsize=(5,5), dpi = 100)
            plot1 = fig.add_subplot(111)
            plot1.pie(item_percentages, labels=labels, wedgeprops={'edgecolor': 'black'}, 
                shadow=True, autopct='%1.1f%%')
            self.canvas = FigureCanvasTkAgg(fig, master = window)
            self.toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=False)
            self.toolbar.update()
            self.canvas.get_tk_widget().pack()
            self.toolbar.pack()

        def clear_page():
            '''Get rid of graph and changes the page'''
            self.canvas.get_tk_widget().pack_forget()
            self.toolbar.pack_forget()
            return parent.replace_frame(HomePage)

        def spending_graph():
            '''How much has the user spent'''
            self.canvas.get_tk_widget().pack_forget()
            self.toolbar.pack_forget()
            total_amount, item_info = info_for_spending_bar_chart(id)
            total_spent = 0
            items = []
            spent_on_item = []
            for item in item_info:
                items.append(item[0])
                spent_on_item.append(item[2])
                total_spent += item[2]
            
            spent_on_item.append(total_spent)
            items.append('Total spent')

            fig = Figure(figsize=(5,5), dpi = 100)
            chart = fig.add_subplot(111)
            chart.set_title("Spending on your items")
            chart.bar(items, spent_on_item)
            chart.set_ylim(0, total_amount[0])
            self.canvas = FigureCanvasTkAgg(fig, master = window)
            self.toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=False)
            self.toolbar.update()
            self.canvas.get_tk_widget().pack()
            self.toolbar.pack()

        def amount_left():
            '''How much has the user spent and how much left to spend on an item'''
            self.canvas.get_tk_widget().pack_forget()
            self.toolbar.pack_forget()
            total_amount, item_info = info_for_spending_bar_chart(id)
            items, amount_left = spending_remaining_chart(id)
            fig = Figure(figsize=(5,5), dpi = 100)
            chart = fig.add_subplot(111)
            chart.set_title("Amount left to spend")
            chart.bar(items, amount_left)
            chart.set_ylim(0, total_amount[0])
            self.canvas = FigureCanvasTkAgg(fig, master = window)
            self.toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=False)
            self.toolbar.update()
            self.canvas.get_tk_widget().pack()
            self.toolbar.pack()


        tk.Button(self, text="percent budget graph", 
            command=percent_budget_graph, width=ITEM_BUTTON_WIDTH).pack(pady=5)

        tk.Button(self, text="Amount Spent", 
            command=spending_graph, width=ITEM_BUTTON_WIDTH).pack(pady=5)
        
        tk.Button(self, text="Amount Remaining",
            command=amount_left, width=ITEM_BUTTON_WIDTH).pack(pady=5)

        tk.Button(self, text="Home Page",
            command=clear_page, width=ITEM_BUTTON_WIDTH).pack(pady=5)
    

if __name__ == '__main__':
    window = BuildPage()
    window.geometry("1000x800")
    window.config(bg="lightblue")
    window.title("Budgeting App")
    window.mainloop()
    