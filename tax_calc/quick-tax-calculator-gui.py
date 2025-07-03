import tkinter as tk
from quick_tax_calculator_module import calculate_progressive_tax as calc_tax 


def calc_income_tax():
    #Calculate the total, federal, and state tax of an entered income.
    entered_income = int(entry.get())

    try:
        # Perform calculation
        result = calc_tax(entered_income)
        # Update the label with the result
        total = result["total"]
        fed = result["fed"]
        state = result["state"]
        result_str = "Total Tax Owed: ${:.2f}\nFederal Tax Owed: ${:.2f}\nCA Tax Owed: ${:.2f}" .format(total,fed,state) 
        result_label.config(text=result_str)
    except Exception as e:
        # Handle any errors that occur during the calculation
        result_label.config(text="Error: " + str(e))

#Create a new Tkinter window
window = tk.Tk()

# Set the window title
window.title("Income Tax Calculator")

# Set the window size
window.geometry("400x300")

# Add a label to the window
label = tk.Label(window, text="Hello, Tkinter!")
label.pack()

# Create an Entry widget for user input
entry = tk.Entry(window)
entry.pack()

# Create a button to get the entered value
button = tk.Button(window, text="Enter Income", command=calc_income_tax)
button.pack()

# Create a Label widget to display the result
result_label = tk.Label(window)
result_label.pack()

""" # Set up the layout using the .grid() geometry manager
entry.grid(row=0, column=0, padx=10)
button.grid(row=0, column=1, pady=10)
result_label.grid(row=0, column=2, padx=10) """

# Start the Tkinter event loop
window.mainloop()

# Main tax calculator code
