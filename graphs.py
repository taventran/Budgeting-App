from  matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from database import info_for_spending_bar_chart, percentages_for_pie_chart

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
    
'''
def spending_chart(id):

    plt.style.use("fivethirtyeight")
    total_amount, item_info = info_for_spending_bar_chart(id)

    items = []
    spent_on_item = []

    for item in item_info:
        items.append(item[0])
        spent_on_item.append(item[2])

    
    plt.title("Spent on items")
    plt.ylim(0, total_amount[0])
    plt.bar(items, spent_on_item)
    plt.show()


spending_chart(1)
'''

def spending_chart(id, window):
    plt.style.use("fivethirtyeight")
    total_amount, item_info = info_for_spending_bar_chart(id)

    items = []
    spent_on_item = []

    for item in item_info:
        items.append(item[0])
        spent_on_item.append(item[2])


    fig = Figure(figsize=(5,5), dpi = 100)
    chart = fig.add_subplot(111)
    chart.title("Spent on items")
    chart.set_ylim(0, total_amount[0])
    chart.set_title("Spending on your items")

    chart.bar(items, spent_on_item)

    canvas = FigureCanvasTkAgg(fig, master = window)
    toolbar = NavigationToolbar2Tk(canvas, window, pack_toolbar=False)
    
    canvas.get_tk_widget().grid()
    toolbar.grid()
