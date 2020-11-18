import tkinter as tk
from tkinter import ttk
import psycopg2
from scraper import web_scrape
from file_handler import write_to_file
from datetime import datetime

# Button functions (self-explanatory)
def sort_by_state():
    if state_combobox.get():
        state_query = "SELECT college_id, name, city, state, family_income FROM college_info WHERE state = '%s' ORDER BY name %s" % (state_combobox.get(), asc_desc_var.get())
    else:
        state_query = "SELECT college_id, name, city, state, family_income FROM college_info ORDER BY name %s" % asc_desc_var.get()
    cursor.execute(state_query)
    college_list = cursor.fetchall()
    college_list_var.set(college_list)

def sort_by_income():
    state_combobox.set('')
    income_query = """SELECT college_id, name, city, state, family_income FROM college_info 
    WHERE operating=1 AND family_income IS NOT NULL and family_income > 0.0 ORDER BY family_income %s""" % asc_desc_var.get()
    cursor.execute(income_query)
    college_list = cursor.fetchall()
    college_list_var.set(college_list)

def sort_by_selectiveness():
    state_combobox.set('')
    selectiveness_query = """SELECT college_id, name, city, state, admission FROM college_info 
    WHERE operating=1 AND admission IS NOT NULL ORDER BY admission %s""" % asc_desc_var.get()
    cursor.execute(selectiveness_query)
    college_list = cursor.fetchall()
    college_list_var.set(college_list)

def sort_by_act_score():
    state_combobox.set('')
    act_query = """SELECT college_id, name, city, state, act_score FROM college_info 
    WHERE operating=1 AND act_score IS NOT NULL ORDER BY act_score %s""" % asc_desc_var.get()
    cursor.execute(act_query)
    college_list = cursor.fetchall()
    college_list_var.set(college_list)

def scrape():
    colleges = list(eval(college_list_var.get()))
    college_id = colleges[results_listbox.curselection()[0]][0]
    print(college_id)
    url_query = """SELECT website FROM college_info WHERE college_id = %s""" % college_id 
    cursor.execute(url_query)
    url = cursor.fetchone()[0]
    print(url)
    try:
        content = "\n".join(web_scrape(url))
        print(content)
        dt = datetime.utcnow()
        time_stamp = str(dt).replace(' ', '_').replace(':', '-')
        write_to_file(college_id, time_stamp, content)
        # Get file name and add it to database
        
        
    except Exception as e:
        print(type(e))
        print(e)

# This one is not tied to a button but used to populate the state selection box.
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
scrape_frame = tk.Frame()

# Get the list from the database and assign StringVars (necessary for many tkinter functions)
state_var = tk.StringVar()
asc_desc_var = tk.StringVar()
asc_desc_var.set('ASC')
cursor.execute("SELECT college_id, name, city, state, family_income FROM college_info WHERE operating=1 ORDER BY name %s" % asc_desc_var.get())
college_list = cursor.fetchall()
college_list_var = tk.StringVar(value=college_list)

# Make widgets
results_listbox = tk.Listbox(list_box_frame, height=25, width=75, listvariable = college_list_var)
state_combobox = ttk.Combobox(control_frame, textvariable=state_var)
state_combobox['values']=get_state_list()
state_button = tk.Button(master=control_frame, text="Sort by State", command=sort_by_state)
income_button = tk.Button(master=control_frame, text = "Sort by Family Income", command=sort_by_income)
selectiveness_button = tk.Button(master=control_frame, text = "Sort by Selectiveness", command=sort_by_selectiveness)
scrape_button = tk.Button(master=scrape_frame, text="Scrape", command=scrape)
act_score_button = tk.Button(master=control_frame, text = "Sort by ACT Score", command=sort_by_act_score)
asc_radio = tk.Radiobutton(control_frame, text='Ascending', variable=asc_desc_var, value='ASC')
desc_radio = tk.Radiobutton(control_frame, text='Descending', variable=asc_desc_var, value='DESC')

# Place the widgets onto the canvas
results_listbox.pack()
list_box_frame.grid(row=0, column=0)
state_combobox.pack()
state_button.pack()
income_button.pack()
selectiveness_button.pack()
act_score_button.pack()
asc_radio.pack()
desc_radio.pack()
control_frame.grid(row=0, column=1)
scrape_frame.grid(row=0, column=2)
scrape_button.pack()

# Run the main loop and close the psycopg2 cursor once the GUI is closed
window.mainloop()
cursor.close()