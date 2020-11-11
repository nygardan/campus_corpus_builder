import tkinter as tk
from tkinter import ttk
import psycopg2

# Button functions
def sort_by_state():
    state_query = "SELECT name, city, family_income FROM college_info WHERE state = '%s' ORDER BY name %s" % (state_combobox.get(), asc_desc_var.get())
    cursor.execute(state_query)
    college_list = cursor.fetchall()
    college_list_var.set(college_list)

def sort_by_income():
    state_combobox.set('')
    income_query = """SELECT name, city, state, family_income FROM college_info 
    WHERE operating=1 AND family_income IS NOT NULL and family_income > 0.0 ORDER BY family_income %s""" % asc_desc_var.get()
    cursor.execute(income_query)
    college_list = cursor.fetchall()
    college_list_var.set(college_list)

def sort_by_selectiveness():
    state_combobox.set('')
    selectiveness_query = """SELECT name, city, state, admission FROM college_info 
    WHERE operating=1 AND admission IS NOT NULL ORDER BY admission %s""" % asc_desc_var.get()
    cursor.execute(selectiveness_query)
    college_list = cursor.fetchall()
    college_list_var.set(college_list)

def get_state_list():
    state_list_query = "SELECT DISTINCT state FROM college_info ORDER BY state"
    cursor.execute(state_list_query)
    return cursor.fetchall()

# Connect to the database.
try:    
    conn = psycopg2.connect(
        dbname= "postgres",
        user = "postgres",
        password = "All25star!",
        port = 5432)
    print("Connected to database.")
    cursor = conn.cursor()

except:
    print("Failed to connect to database.")

# Set up the tkinter window and frames
window = tk.Tk()
window.title("Campus Corpus Builder")
list_box_frame = tk.Frame()
control_frame = tk.Frame()

# Get the list from the database and assign StringVars

state_var = tk.StringVar()
asc_desc_var = tk.StringVar()
cursor.execute("SELECT name, city, state, family_income FROM college_info ORDER BY name %s" % asc_desc_var.get())
college_list = cursor.fetchall()
college_list_var = tk.StringVar(value=college_list)

# Make widgets
results_listbox = tk.Listbox(list_box_frame, height=25, width=75, listvariable = college_list_var)

state_combobox = ttk.Combobox(control_frame, textvariable=state_var)
state_combobox['values']=get_state_list()
state_combobox.state(["readonly"])
state_button = tk.Button(master=control_frame, text="Sort by State", command=sort_by_state)
income_button = tk.Button(master=control_frame, text = "Sort by Family Income", command=sort_by_income)
selectiveness_button = tk.Button(master=control_frame, text = "Sort by Selectiveness", command=sort_by_selectiveness)
asc_radio = tk.Radiobutton(control_frame, text='Ascending', variable=asc_desc_var, value='ASC')
desc_radio = tk.Radiobutton(control_frame, text='Descending', variable=asc_desc_var, value='DESC')


# Place the widgets
results_listbox.pack()
list_box_frame.grid(row=0, column=0)
state_combobox.pack()
state_button.pack()
income_button.pack()
selectiveness_button.pack()
asc_radio.pack()
desc_radio.pack()
control_frame.grid(row=0, column=1)

window.mainloop()
cursor.close()