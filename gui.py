'''
Budgeting app that shows how much a user can spend based on what percentage 
of their paycheck they allocate to that sector
'''
import tkinter as tk
from tkinter.constants import BOTTOM
from graphs import display_pie_chart
from models import User, MoneyAmount, BudgetItem
from database import create_user, show_budget_items, update_spending_budget_item, get_already_spent, info_for_spending_bar_chart
from database import verify_login, get_user_id, get_amount_of_money, display_money, get_budget_item, show_budget_items
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from database import percentages_for_pie_chart
from datetime import date

# Set current user to none and changes it once a valid login occurs
CURRENT_USER = None

LARGE_TEXT_FONT = ("Cambria", 50)
MEDIUM_TEXT_FONT = ("Cambria", 20)
BUTTON_FONT = ("Cambria", 15)
ENTRY_BOXES_WIDTH = 30
HOME_BUTTON_WIDTH = 40
REGISTER_BUTTON_WIDTH = 25


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
            command=get_user, font=("cambria", 15)).pack(pady=5)
        tk.Button(self, text="New User", width=REGISTER_BUTTON_WIDTH,
            command=lambda: parent.replace_frame(RegisterPage), font=("cambria", 15)).pack(pady=5)

class RegisterPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg='lightblue')
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

        tk.Button(self, text="Submit", command=get_info, width=REGISTER_BUTTON_WIDTH,
            font=("Cambria", 12)).pack()
        tk.Button(self, text="Login Page", width=REGISTER_BUTTON_WIDTH,
            command=lambda: parent.replace_frame(LoginPage), font=("Cambria", 12)).pack()
        

class HomePage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg='lightblue')
        tk.Label(self, text=date.today(), font=LARGE_TEXT_FONT, bg='lightblue').pack()
        tk.Label(self, text="Home Page", font=LARGE_TEXT_FONT, bg='lightblue').pack()
        tk.Label(self, text=f"{CURRENT_USER.username} welcome!", font=LARGE_TEXT_FONT, bg='lightblue').pack()
        id = get_user_id(CURRENT_USER.username)
        info = display_money(id)

        if len(info) > 0:
            monthly_allowance = [allowance[0] for allowance in info]
            savings = [save[1] for save in info]
            savings_in_dollars = [dollar_amount[2] for dollar_amount in info]
            information = tk.Label(self, text=f"Monthly Paycheck {monthly_allowance[0]:.2f}", bg='lightblue', font=MEDIUM_TEXT_FONT).pack()
            information3 = tk.Label(self, text=f"Saving {savings_in_dollars[0]:.2f}$ this month", bg='lightblue', font=MEDIUM_TEXT_FONT).pack()

            tk.Button(self, text="Budget Item", font=("Cambria", 15), width=HOME_BUTTON_WIDTH,
                relief="raised", command=lambda: parent.replace_frame(BudgetItemPage)).pack(pady=5)
            tk.Button(self, text="Update Item Spending", font=("Cambria", 15), width=HOME_BUTTON_WIDTH,
                relief="raised", command=lambda: parent.replace_frame(UpdateSpending)).pack(pady=5)
            tk.Button(self, text="Graphs", font=("Cambria", 15), width=HOME_BUTTON_WIDTH,
                relief="raised", command=lambda: parent.replace_frame(Charts)).pack(pady=5)

        tk.Button(self, text="Monthly Paycheck", font=("Cambria", 15), width=HOME_BUTTON_WIDTH,
            relief="raised", command=lambda: parent.replace_frame(MonthlyAllowancePage)).pack(pady=5)
        tk.Button(self, text="Signout", font=("Cambria", 15), width=HOME_BUTTON_WIDTH,
            relief="raised", command=lambda: parent.replace_frame(LoginPage)).pack(pady=5)
        
    

class MonthlyAllowancePage(tk.Frame):
    '''Gets how much user will make that month, and the percentage amount they want to save. '''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg='lightblue')
        tk.Label(self, text="Put monthly paycheck and savings", font=("Cambria", 26)).grid(pady=10)
        self.monthlyPay = tk.Entry(self, font=("Cambria", 12))
        self.monthlyPay.insert(0, 'Monthly Paycheck')
        self.monthlyPay.grid()
        self.savings = tk.Entry(self, font=("Cambria", 12))
        self.savings.insert(0, 'Percent you want to save')
        self.savings.grid()
        self.error = tk.Label(self, text="Monthly pay needs to be a number and savings need to be a positive whole number!", font=("Cambria", 12))
        def get_info():
            try:
                monthlyPay = float(self.monthlyPay.get())   
                savings = int(self.savings.get())
                if (savings < 0) or (savings > 100):
                    tk.Label(self, text="Savings needs to be a whole number between 0 and 100").grid(pady=10)
                else:
                    money = MoneyAmount(monthlyPay, savings, CURRENT_USER.username)
                    id = get_user_id(money.user)
                    print(id)
                    get_amount_of_money(money, id)
                    self.error.destroy()
                    return parent.replace_frame(HomePage)
            except ValueError:
                self.error.grid()

        tk.Label(text="Invalid Entry")
        tk.Button(self, text="Submit", command=get_info, font=("Cambria", 15)).grid()
        tk.Button(self, text="Home Page", font=("Cambria", 15),
            command=lambda: parent.replace_frame(HomePage)).grid()



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
            budget_class = BudgetItem(item, percent)
            get_budget_item(budget_class, id)
            return parent.replace_frame(HomePage)


        tk.Button(self, text="Submit",
            command=get_info).pack()
        tk.Button(self, text="Home Page",
            command= lambda: parent.replace_frame(HomePage)).pack()


class UpdateSpending(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg='lightblue')
        tk.Label(self, text="Update Spending for Budget Items").grid()
        self.spent = tk.Entry(self)
        self.spent.grid()
        self.spent.grid_remove()
        id = get_user_id(CURRENT_USER.username)
        items  = show_budget_items(id)
        self.error = tk.Label(self, text="Needs to be a number!")
        def get_spent(item):
            try:
                just_spent = float(self.spent.get())
                total_spent = just_spent + get_already_spent(item)
                update_spending_budget_item(total_spent, item)
                self.error.destroy()
                return parent.replace_frame(HomePage)
            except ValueError:
                self.error.grid()

        def get_item(item):
            tk.Label(text=f'How much did you spend on {item[0]} today?')
            self.spent.grid()
            tk.Button(self, text="submit", command = lambda: get_spent(item[0])).grid()
        
        for item in items:  
            button = tk.Button(self, text=f'{item}', command= get_item(item)).grid()

        tk.Button(self, text="Home", command=lambda: parent.replace_frame(HomePage)).grid()

class Charts(tk.Frame):
    '''All the stats for the budgeting app will be shown here'''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg='lightblue')
        tk.Label(self, text="Graphs and Charts of your Spending", bg="lightblue").pack()
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
            '''How much has the user spent and how much left they have to spend'''
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
            pass       

        tk.Button(self, text="percent budget graph", 
            command=percent_budget_graph).pack()

        tk.Button(self, text="Left To Spend", 
            command=spending_graph).pack()
        
        tk.Button(self, text="Amount Remaining",
            command=amount_left).pack()

        tk.Button(self, text="Home Page",
            command=clear_page).pack()
    

if __name__ == '__main__':
    window = BuildPage()
    window.geometry("750x500")
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.config(bg="lightblue")
    window.title("Budgeting App")
    window.mainloop()
    