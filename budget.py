import tkinter as tk
window = tk.Tk()


entry = tk.Entry()
entry.pack()

def getEntry():
    getString = entry.get()
    print(getString)

button = tk.Button(text="Submit", command=getEntry)
button.pack()

window.mainloop()