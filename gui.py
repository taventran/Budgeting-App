'''
Budgeting app that shows how much a user can spend based on what percentage 
of their paycheck they allocate to that sector
'''
import tkinter as tk


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
        tk.Button(self, text="Login", 
            command=lambda: parent.replace_frame(HomePage)).pack()
        tk.Button(self, text="New User", 
            command=lambda: parent.replace_frame(RegisterPage)).pack()
                   
class RegisterPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Register page")
        self.entry = tk.Entry(self)
        self.entry.insert(0, 'New Id Code')
        self.entry.pack()
        
class HomePage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Home Page").pack()
        tk.Button(self, text="New Information", 
            command=lambda: parent.replace_frame(GetInfoPage)).pack()
        tk.Button(self, text="Signout", 
            command=lambda: parent.replace_frame(LoginPage)).pack()


class GetInfoPage(tk.Frame):
    '''Gets how much user will make that month, asks them how much they want to 
    spend on each sector,and the percentage amount they want to save. '''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Put New Information").pack()
        self.entry = tk.Entry(self)
        self.entry.pack()
        tk.Button(self, text="Submit", command=self.get_numbers).pack()
        tk.Button(self, text="Home Page", 
            command=lambda: parent.replace_frame(HomePage)).pack()
    try:
        def get_numbers(self):
            getEntry = self.entry.get()
            print(getEntry)
            with open('info.txt', 'w') as file:
                file.write(getEntry)
    except: 
        tk.Label(text="Invalid Entry")


if __name__ == '__main__':
    window = BuildPage()
    window.geometry("500x500")
    window.mainloop()
