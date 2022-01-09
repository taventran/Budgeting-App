from  matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from database import percentages_for_pie_chart

def display_pie_chart(id, window):
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

    
    canvas = FigureCanvasTkAgg(fig, master = window)
    toolbar = NavigationToolbar2Tk(canvas, window, pack_toolbar=False)
    toolbar.update()
    canvas.get_tk_widget().grid()
    toolbar.grid()

    def clear_graph():
        canvas.get_tk_widget().grid_remove()
        toolbar.grid_remove()
    



