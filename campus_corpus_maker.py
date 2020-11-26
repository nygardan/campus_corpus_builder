import tkinter as tk
from tkinter import ttk
import psycopg2
from scraper import web_scrape
from file_handler import *
from datetime import datetime

# Button functions (self-explanatory)
def sort_by_state():
    if state_combobox.get():
        state_query = """SELECT college_id, name, city, state, family_income
        FROM college_info WHERE operating = 1 AND state = '%s' %s ORDER BY name %s""" % (state_combobox.get(), two_or_four_var.get(), asc_desc_var.get())
    else:
        state_query = """SELECT college_id, name, city, state, family_income
        FROM college_info WHERE operating = 1 %s ORDER BY name %s""" % (two_or_four_var.get(), asc_desc_var.get())
    cursor.execute(state_query)
    college_list = cursor.fetchall()
    college_list_var.set(college_list)
    count_label_var.set(str(len(college_list)))

def sort_by_income():
    state_combobox.set('')
    income_query = """SELECT college_id, name, city, state, family_income FROM college_info
    WHERE operating=1 AND family_income IS NOT NULL and family_income > 0.0 %s ORDER BY family_income %s""" % (two_or_four_var.get(), asc_desc_var.get())
    cursor.execute(income_query)
    college_list = cursor.fetchall()
    college_list_var.set(college_list)
    count_label_var.set(str(len(college_list)))

def sort_by_selectiveness():
    state_combobox.set('')
    selectiveness_query = """SELECT college_id, name, city, state, admission FROM college_info
    WHERE operating=1 AND admission IS NOT NULL %s ORDER BY admission %s""" % (two_or_four_var.get(), asc_desc_var.get())
    cursor.execute(selectiveness_query)
    college_list = cursor.fetchall()
    college_list_var.set(college_list)
    count_label_var.set(str(len(college_list)))

def sort_by_act_score():
    state_combobox.set('')
    act_query = """SELECT college_id, name, city, state, act_score FROM college_info
    WHERE operating=1 AND act_score IS NOT NULL %s ORDER BY act_score %s""" % (two_or_four_var.get(), asc_desc_var.get())
    cursor.execute(act_query)
    college_list = cursor.fetchall()
    college_list_var.set(college_list)
    count_label_var.set(str(len(college_list)))

# Our most important (and most complicated) method.
def scrape():
    colleges = list(eval(college_list_var.get()))
    college_ids = []
    for number in results_listbox.curselection():
        college_ids.append(colleges[number][0])

    print(college_ids)
    for college_id in college_ids:
        url_query = """SELECT website, name FROM college_info WHERE college_id = %s""" % college_id
        cursor.execute(url_query)
        info = cursor.fetchone()
        url = info[0]
        college_name = info[1]
        dt = datetime.utcnow()
        info_string = "[## %s %s %s  ##]\n" % (college_name, dt.date(), dt.time())
        print(url)
        print(college_name)
        try:

            output, errors = web_scrape(url)
            output_string = "\n".join(output)
            error_string = "\n".join(errors)
            content = info_string + output_string + error_string
            #print(content)

            time_stamp = str(dt).replace(' ', '_').replace(':', '-')
            raw_file_name = write_to_file(college_id, time_stamp, content)
            processed_file_name, token_count = process_nlp_to_file(raw_file_name, time_stamp, output_string)
            # Get file name and add it to database
            print(processed_file_name + str(token_count))
            scrape_upload_query = """INSERT INTO scrape_info (college_id, date_time,
            file_name, pages_count, fault_count) VALUES (%s, %s, %s, %s, %s) RETURNING scrape_id;"""
            cursor.execute(scrape_upload_query, (str(college_id), str(dt), raw_file_name, len(output), len(errors)))
            id_of_scrape = cursor.fetchone()[0]
            nlp_type = 'word_tokenized'
            conn.commit()
            processed_file_query = """INSERT INTO nlp_info (scrape_id, file_name,
            token_count, nlp_type) VALUES (%s, %s, %s, %s)"""
            cursor.execute(processed_file_query, (id_of_scrape, processed_file_name, token_count, nlp_type))
            conn.commit()


        except Exception as e:
            print(type(e))
            print(e)

    print("\nScrape complete!")

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
        password = "postgres",
        host = 'localhost',
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
two_or_four_var = tk.StringVar()
asc_desc_var.set('ASC')
two_or_four_var.set('AND level IN (1, 2, 3)')
cursor.execute("SELECT college_id, name, city, state, family_income FROM college_info WHERE operating=1 ORDER BY name %s" % asc_desc_var.get())
college_list = cursor.fetchall()
college_list_var = tk.StringVar(value=college_list)
count_label_var = tk.StringVar()
count_label_var.set(str(len(college_list)))

# Make widgets
count_label = tk.Label(list_box_frame, textvariable=count_label_var)
results_listbox = tk.Listbox(list_box_frame, selectmode='extended', height=35, width=75, listvariable = college_list_var)
scrollbar = tk.Scrollbar(list_box_frame)
state_combobox = ttk.Combobox(control_frame, textvariable=state_var)
state_combobox['values']=get_state_list()
state_button = tk.Button(master=control_frame, text="Sort by State", command=sort_by_state)
income_button = tk.Button(master=control_frame, text = "Sort by Family Income", command=sort_by_income)
selectiveness_button = tk.Button(master=control_frame, text = "Sort by Selectiveness", command=sort_by_selectiveness)
scrape_button = tk.Button(master=scrape_frame, text="Scrape", command=scrape)
act_score_button = tk.Button(master=control_frame, text = "Sort by ACT Score", command=sort_by_act_score)
asc_radio = tk.Radiobutton(control_frame, text='Ascending', variable=asc_desc_var, value='ASC')
desc_radio = tk.Radiobutton(control_frame, text='Descending', variable=asc_desc_var, value='DESC')
two_year_radio = tk.Radiobutton(control_frame, text='Two-Year', variable=two_or_four_var, value='AND level IN (2,3)')
four_year_radio = tk.Radiobutton(control_frame, text='Four_Year', variable=two_or_four_var, value='AND level = 1')
all_years_radio = tk.Radiobutton(control_frame, text='All', variable=two_or_four_var, value='AND level IN (1, 2, 3)')

# Place the widgets onto the canvas
count_label.pack()
results_listbox.pack(side='left', fill='both')
scrollbar.pack(side='right', fill='both')
results_listbox.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = results_listbox.yview)
list_box_frame.grid(row=0, column=0)
state_combobox.pack()
state_button.pack()
income_button.pack()
selectiveness_button.pack()
act_score_button.pack()
asc_radio.pack()
desc_radio.pack()
two_year_radio.pack()
four_year_radio.pack()
all_years_radio.pack()
control_frame.grid(row=0, column=1)
scrape_frame.grid(row=0, column=2)
scrape_button.pack()

# Run the main loop and close the psycopg2 cursor once the GUI is closed
window.mainloop()
cursor.close()
