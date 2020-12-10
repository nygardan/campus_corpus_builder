# Code for running tkinter GUI and pulling in our scraper and file functions.
# Finalized for CSCI 765 12-9-2020, by Dan Nygard
# The tutorial I used for tkinter is:
# https://realpython.com/python-gui-tkinter/
# Very useful for understanding how this runs.

import tkinter as tk
from tkinter import ttk
import psycopg2
from scraper import web_scrape
from file_handler import *
from datetime import datetime

# Button functions for sorting our colleges and scrapes (each button does both)
# Currently can sort by state, family income of students, selectiveness, and ACT score.
# All are similar and re-use code (not Pythonic, I know...) - refactoring may be necessary
# I've commented only the first one.

def sort_by_state():
    # Queries to sort if a state has been selected, or (if no state) to sort all states.
    if state_combobox.get():
        state_query = """SELECT college_id, name, city, state, family_income
        FROM college_info WHERE operating = 1 AND state = '%s' %s
        ORDER BY name %s""" % (state_combobox.get().upper(), two_or_four_var.get(), asc_desc_var.get())
        state_scrape_query = """SELECT scrape_info.scrape_id, name, state, date(date_time), to_char(date_time, 'HH:MM'), token_count
        FROM college_info INNER JOIN scrape_info ON college_info.college_id=scrape_info.college_id
        INNER JOIN nlp_info ON scrape_info.scrape_id=nlp_info.scrape_id
        WHERE state = '%s' %s %s ORDER BY name %s
        """ % (state_combobox.get().upper(), two_or_four_var.get(), token_count_var.get(), asc_desc_var.get())
    else:
        state_query = """SELECT college_id, name, city, state, family_income
        FROM college_info WHERE operating = 1 %s ORDER BY name %s""" % (two_or_four_var.get(), asc_desc_var.get())
        state_scrape_query = """SELECT scrape_info.scrape_id, name, state, date(date_time), to_char(date_time, 'HH:MM'), token_count FROM college_info
        INNER JOIN scrape_info ON college_info.college_id=scrape_info.college_id
        INNER JOIN nlp_info ON scrape_info.scrape_id = nlp_info.scrape_id
        WHERE operating = 1 %s %s ORDER BY name %s""" % (two_or_four_var.get(), token_count_var.get(), asc_desc_var.get())
    cursor.execute(state_query)
    college_list = cursor.fetchall()

    # Tkinter uses list variables for its widgets.
    # You have to set them as below.
    college_list_var.set(college_list)

    # Gives the GUI a count of all items in the list.
    count_label_var.set(str(len(college_list)))

    # The colleges have been sorted, now we sort any scrapes available.
    cursor.execute(state_scrape_query)
    scrape_list = cursor.fetchall()
    scrape_list_var.set(scrape_list)
    scrape_count_label_var.set(str(len(scrape_list)))

def sort_by_income():
    if state_combobox.get():
        income_query = """SELECT college_id, name, city, state, family_income FROM college_info
        WHERE operating=1 AND family_income IS NOT NULL and state = '%s' and family_income > 0.0 %s
        ORDER BY family_income %s""" % (state_combobox.get().upper(), two_or_four_var.get(), asc_desc_var.get())
        income_scrape_query = """SELECT scrape_info.scrape_id, name, state, date(date_time), to_char(date_time, 'HH:MM'), token_count
        FROM college_info INNER JOIN scrape_info ON college_info.college_id=scrape_info.college_id
        INNER JOIN nlp_info ON scrape_info.scrape_id=nlp_info.scrape_id
        WHERE state = '%s' %s AND family_income > 0.0 %s ORDER BY family_income
        %s """ % (state_combobox.get().upper(), token_count_var.get(), two_or_four_var.get(), asc_desc_var.get())
    else:
        income_query = """SELECT college_id, name, city, state, family_income FROM college_info
        WHERE operating=1 AND family_income IS NOT NULL and family_income > 0.0 %s
        ORDER BY family_income %s""" % (two_or_four_var.get(), asc_desc_var.get())
        income_scrape_query = """ SELECT scrape_info.scrape_id, name, state, date(date_time), to_char(date_time, 'HH:MM'), token_count
        FROM college_info INNER JOIN scrape_info ON college_info.college_id=scrape_info.college_id
        INNER JOIN nlp_info ON scrape_info.scrape_id=nlp_info.scrape_id
        WHERE operating=1 %s and family_income > 0.0 %s
        ORDER BY family_income %s """ % (token_count_var.get(), two_or_four_var.get(), asc_desc_var.get())
    cursor.execute(income_query)
    college_list = cursor.fetchall()
    college_list_var.set(college_list)
    count_label_var.set(str(len(college_list)))

    cursor.execute(income_scrape_query)
    scrape_list = cursor.fetchall()
    scrape_list_var.set(scrape_list)
    scrape_count_label_var.set(str(len(scrape_list)))

def sort_by_selectiveness():
    if state_combobox.get():
        selectiveness_query = """SELECT college_id, name, city, state, admission
        FROM college_info WHERE operating=1 AND state = '%s' AND admission > 0.0 %s
        ORDER BY admission %s""" % (state_combobox.get().upper(), two_or_four_var.get(), asc_desc_var.get())
        selectiveness_scrape_query = """SELECT scrape_info.scrape_id, name, state, date(date_time), to_char(date_time, 'HH:MM'), token_count
        FROM college_info INNER JOIN scrape_info ON college_info.college_id=scrape_info.college_id
        INNER JOIN nlp_info ON scrape_info.scrape_id=nlp_info.scrape_id
        WHERE state = '%s' %s AND admission > 0.0 %s ORDER BY admission
        %s """ % (state_combobox.get().upper(), token_count_var.get(), two_or_four_var.get(), asc_desc_var.get())
    else:
        selectiveness_query = """SELECT college_id, name, city, state, admission
        FROM college_info WHERE operating=1 AND admission > 0.0 %s
        ORDER BY admission %s""" % (two_or_four_var.get(), asc_desc_var.get())
        selectiveness_scrape_query = """ SELECT scrape_info.scrape_id, name, state, date(date_time), to_char(date_time, 'HH:MM'), token_count
        FROM college_info INNER JOIN scrape_info ON college_info.college_id=scrape_info.college_id
        INNER JOIN nlp_info ON scrape_info.scrape_id=nlp_info.scrape_id
        WHERE operating=1 %s and admission > 0.0 %s
        ORDER BY admission %s """ % (token_count_var.get(), two_or_four_var.get(), asc_desc_var.get())
    cursor.execute(selectiveness_query)
    college_list = cursor.fetchall()
    college_list_var.set(college_list)
    count_label_var.set(str(len(college_list)))

    cursor.execute(selectiveness_scrape_query)
    scrape_list = cursor.fetchall()
    scrape_list_var.set(scrape_list)
    scrape_count_label_var.set(str(len(scrape_list)))

def sort_by_act_score():
    if state_combobox.get():
        act_query = """SELECT college_id, name, city, state, act_score FROM college_info
        WHERE operating=1 AND state = '%s' and act_score IS NOT NULL %s
        ORDER BY act_score %s""" % (state_combobox.get().upper(), two_or_four_var.get(), asc_desc_var.get())
        act_scrape_query = """SELECT scrape_info.scrape_id, name, state, date(date_time), to_char(date_time, 'HH:MM'), token_count
        FROM college_info INNER JOIN scrape_info ON college_info.college_id=scrape_info.college_id
        INNER JOIN nlp_info ON scrape_info.scrape_id=nlp_info.scrape_id
        WHERE state = '%s' %s AND act_score IS NOT NULL %s ORDER BY act_score
        %s """ % (state_combobox.get().upper(), token_count_var.get(), two_or_four_var.get(), asc_desc_var.get())
    else:
        act_query = """SELECT college_id, name, city, state, act_score FROM college_info
        WHERE operating=1 AND act_score IS NOT NULL %s ORDER BY act_score %s
        """ % (two_or_four_var.get(), asc_desc_var.get())
        act_scrape_query = """ SELECT scrape_info.scrape_id, name, state, date(date_time), to_char(date_time, 'HH:MM'), token_count
        FROM college_info INNER JOIN scrape_info ON college_info.college_id=scrape_info.college_id
        INNER JOIN nlp_info ON scrape_info.scrape_id=nlp_info.scrape_id
        WHERE operating=1 %s and act_score IS NOT NULL %s
        ORDER BY act_score %s """ % (token_count_var.get(), two_or_four_var.get(), asc_desc_var.get())
    cursor.execute(act_query)
    college_list = cursor.fetchall()
    college_list_var.set(college_list)
    count_label_var.set(str(len(college_list)))

    cursor.execute(act_scrape_query)
    scrape_list = cursor.fetchall()
    scrape_list_var.set(scrape_list)
    scrape_count_label_var.set(str(len(scrape_list)))

# Our most important method - scrapes data from web and saves to both flat text file and (as tokenized text) to .json.
def scrape():
    # In the list you can select one or many colleges.
    # This gets the college ID of each item selected.
    colleges = list(eval(college_list_var.get()))
    college_ids = []
    for number in results_listbox.curselection():
        college_ids.append(colleges[number][0])
    # prints the ids of our selected schools to the terminal.
    print(college_ids)

    # Scrape the websites selected using our college ID list.
    for college_id in college_ids:
        url_query = """SELECT website, name FROM college_info WHERE college_id = %s""" % college_id
        cursor.execute(url_query)
        info = cursor.fetchone()
        url = info[0]
        college_name = info[1]
        dt = datetime.utcnow()

        # This goes at the top of each flat text file (so you can see that if you're just opening files.)
        info_string = "[## %s %s %s  ##]\n" % (college_name, dt.date(), dt.time())
        print(url)
        print(college_name)
        try:
            # First we run the scrape to get our output and errors lists.
            output, errors = web_scrape(url)
            output_string = "\n".join(output)
            error_string = "\n".join(errors)
            content = info_string + output_string + error_string

            # Make a time stamp for the scrape to put in the database.
            time_stamp = str(dt).replace(' ', '_').replace(':', '-')

            # Use a file_handler.py functions to write the .scrape (flat text) and .json files.
            raw_file_name = write_to_file(college_id, time_stamp, content)
            processed_file_name, token_count = process_nlp_to_file(raw_file_name, time_stamp, output_string)
            # Get file name and add it to scrape_info table, then print to terminal so we can see progress
            scrape_upload_query = """INSERT INTO scrape_info (college_id, date_time,
            file_name, pages_count, fault_count) VALUES (%s, %s, %s, %s, %s) RETURNING scrape_id;"""
            cursor.execute(scrape_upload_query, (str(college_id), str(dt), raw_file_name, len(output), len(errors)))
            print(processed_file_name + str(token_count))

            # This is psycopg2's odd way of getting the ID of the scrape we just added.
            # We use this ID to save our tokenized JSON file and put it into the nlp_info table.
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
    # This is our terminal telling us the scrape we started is now complete.
    print("\nScrape complete!")

# Used to get the statistics that appear in the rightmost side of the GUI.
def get_stats():
    # Set our label variables in preparation for the results.
    total_scrapes_label_var.set("Total scrapes: ")
    total_successful_scrapes_label_var.set("Successful scrapes: ")
    total_tokens_label_var.set("Total tokens: ")

    # You can select multiple scrapes. If none are selected it chooses all.
    if len(scrape_results_listbox.curselection()) == 0:
        scrapes = list(eval(scrape_list_var.get()))
        scrape_ids = []
        for scrape in scrapes:
            scrape_ids.append(scrape[0])
    else:
        scrapes = list(eval(scrape_list_var.get()))
        scrape_ids = []
        for number in scrape_results_listbox.curselection():
            scrape_ids.append(scrapes[number][0])

    # We take a tuple of scrape ids for the psycopg2 queries and set our labels to show our counts.
    scrape_tuple = tuple(scrape_ids)
    total_scrapes_label_var.set(total_scrapes_label_var.get() + str(len(scrape_ids)))
    successful_scrapes_query = """SELECT COUNT (token_count) FROM nlp_info
    WHERE scrape_id IN %s AND token_count > 0"""
    cursor.execute(successful_scrapes_query, (scrape_tuple,))
    total_successful_scrapes_label_var.set(total_successful_scrapes_label_var.get() + str(cursor.fetchall()[0][0]))
    token_count_query = """SELECT SUM (token_count) FROM nlp_info
    where scrape_id IN %s """
    cursor.execute(token_count_query, (scrape_tuple,))
    total_tokens_label_var.set(total_tokens_label_var.get() + str(cursor.fetchall()[0][0]))

# This allows us to open up our selected scrapes in a new text window for review.
def read_files():
    # Build our new window (a tk.Toplevel), text box, and a scroll bar.
    new_window = tk.Toplevel(window)
    new_window.title("View Scrape Output")
    new_window.geometry("900x500")
    text_display = tk.Text(new_window)
    ys = ttk.Scrollbar(new_window, orient = 'vertical', command = text_display.yview)
    text_display['yscrollcommand'] = ys.set
    text_display.config(wrap='word')
    text_display.pack(side='left', expand=True, fill='both')
    ys.pack(side='right', fill='both')

    # I have it set so that you have to select one or multiple
    # You can't just open them all by not selecting any.
    if len(scrape_results_listbox.curselection()) == 0:
        scrapes = list(eval(scrape_list_var.get()))
        scrape_ids = []
        for scrape in scrapes:
            scrape_ids.append(scrape[0])

    else:
        scrapes = list(eval(scrape_list_var.get()))
        scrape_ids = []
        for number in scrape_results_listbox.curselection():
            scrape_ids.append(scrapes[number][0])

    # Run our query to get the file names.
    scrape_tuple = tuple(scrape_ids)
    file_ids_query = """SELECT file_name FROM scrape_info
    WHERE scrape_id IN %s """
    cursor.execute(file_ids_query, (scrape_tuple,))
    file_ids = cursor.fetchall()
    file_ids = [file[0] for file in file_ids]
    # This reads our text using file_handler.py's read_from_files function.
    # tkinter has a known bug that prevents it from writing certain unicode characters
    # (emojis) to the tkinter text box. fixTkBMP is a function that evaluates each character
    # in the string and replaces it with a <?> if necessary.
    # It makes our file reader VERY SLOW if there is large input. Works like a charm
    # if you don't try to open 300 scrapes at the same time.

    text_list = read_from_files(file_ids)
    for text in text_list:
        text = fixTkBMP(text)
        text_display.insert('end', text + '\n\n')

# Taken from https://learning-python.com/cgi/showcode.py?name=pymailgui-products%2Funzipped%2FPyMailGui-PP4E%2FfixTkBMP.py&rawmode=view
# Used to display text in the TKinter text box.
def fixTkBMP(text):
    text = ''.join((ch if ord(ch) <= 0xFFFF else '\uFFFD') for ch in text)
    return text

# These methods get the number of items selected in each listbox.
# It's nice to have them when you need to select a certain number of items.
def get_scrape_selectcount(*args):
    selected = scrape_results_listbox.curselection()
    scrape_selectcount_label_var.set(str(len(selected)))

def get_college_selectcount(*args):
    selected = results_listbox.curselection()
    college_selectcount_label_var.set(str(len(selected)))

# This is used to populate the state selection box.
def get_state_list():
    state_list_query = "SELECT DISTINCT state FROM college_info ORDER BY state"
    cursor.execute(state_list_query)
    return cursor.fetchall()


# We have finished our function definitions! Here we start the program.

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


# Tkinter code below - it is a mess

# Set up the tkinter window and frames
window = tk.Tk()
window.title("Campus Corpus Builder")
list_box_frame = tk.Frame()
control_frame = tk.Frame()
scrape_list_box_frame = tk.Frame()
scrape_control_frame = tk.Frame()

# Get the list from the database and assign StringVars (necessary for many tkinter functions)
# We also pull college info and scrape info from the tables if it is there.
state_var = tk.StringVar()
asc_desc_var = tk.StringVar()
two_or_four_var = tk.StringVar()
asc_desc_var.set('ASC')
two_or_four_var.set('AND level IN (1, 2, 3)')
cursor.execute("""SELECT college_id, name, city, state, family_income FROM
college_info WHERE operating=1 ORDER BY name %s""" % asc_desc_var.get())
college_list = cursor.fetchall()
college_list_var = tk.StringVar(value=college_list)
count_label_var = tk.StringVar()
count_label_var.set(str(len(college_list)))
token_count_var = tk.StringVar()
token_count_var.set('AND token_count >= 0')
cursor.execute("""SELECT scrape_info.scrape_id, name, state, date(date_time), to_char(date_time, 'HH:MM'), token_count
FROM college_info INNER JOIN scrape_info ON college_info.college_id=scrape_info.college_id
INNER JOIN nlp_info ON scrape_info.scrape_id=nlp_info.scrape_id
WHERE operating=1 %s ORDER BY name %s""" % (token_count_var.get(), asc_desc_var.get()))
scrape_list = cursor.fetchall()
scrape_list_var = tk.StringVar(value=scrape_list)
scrape_count_label_var = tk.StringVar()
scrape_count_label_var.set(str(len(scrape_list)))
total_scrapes_label_var = tk.StringVar()
total_successful_scrapes_label_var = tk.StringVar()
total_tokens_label_var = tk.StringVar()
scrape_selectcount_label_var = tk.StringVar()
scrape_selectcount_label_var.set('0')
college_selectcount_label_var = tk.StringVar()
college_selectcount_label_var.set('0')

# Make widgets
count_label = tk.Label(list_box_frame, textvariable=count_label_var)
scrape_count_label = tk.Label(scrape_list_box_frame, textvariable=scrape_count_label_var)
scrape_selectcount_label = tk.Label(scrape_list_box_frame, textvariable=scrape_selectcount_label_var)
college_selectcount_label = tk.Label(list_box_frame, textvariable=college_selectcount_label_var)
results_listbox = tk.Listbox(list_box_frame, selectmode='extended',
height=40, width=65, font='Arial 9', listvariable = college_list_var)
results_listbox.bind('<<ListboxSelect>>', get_college_selectcount)
scrape_results_listbox = tk.Listbox(scrape_list_box_frame, selectmode='extended',
height=40, width=65, font='Arial 9', listvariable = scrape_list_var)
scrape_results_listbox.bind('<<ListboxSelect>>', get_scrape_selectcount)
scrollbar = tk.Scrollbar(list_box_frame)
scrape_scrollbar = tk.Scrollbar(scrape_list_box_frame)
state_combobox = ttk.Combobox(control_frame, textvariable=state_var)
state_combobox['values']=get_state_list()
state_button = tk.Button(master=control_frame, text="Sort by State", command=sort_by_state)
income_button = tk.Button(master=control_frame, text = "Sort by Family Income", command=sort_by_income)
selectiveness_button = tk.Button(master=control_frame, text = "Sort by Selectiveness", command=sort_by_selectiveness)
scrape_button = tk.Button(master=control_frame, text="Scrape", command=scrape)
act_score_button = tk.Button(master=control_frame, text = "Sort by ACT Score", command=sort_by_act_score)
asc_radio = tk.Radiobutton(control_frame, text='Ascending', variable=asc_desc_var, value='ASC')
desc_radio = tk.Radiobutton(control_frame, text='Descending', variable=asc_desc_var, value='DESC')
two_year_radio = tk.Radiobutton(control_frame, text='Two-Year', variable=two_or_four_var, value='AND level IN (2, 3)')
four_year_radio = tk.Radiobutton(control_frame, text='Four_Year', variable=two_or_four_var, value='AND level = 1')
all_years_radio = tk.Radiobutton(control_frame, text='All', variable=two_or_four_var, value='AND level IN (1, 2, 3)')
token_radio = tk.Radiobutton(scrape_control_frame, text='Tokens > 0', variable=token_count_var, value='AND token_count > 0')
no_token_radio = tk.Radiobutton(scrape_control_frame, text='Tokens = 0', variable=token_count_var, value='AND token_count = 0')
all_token_radio = tk.Radiobutton(scrape_control_frame, text='All tokens', variable=token_count_var, value='AND token_count >= 0')
total_scrapes_label = tk.Label(scrape_control_frame, textvariable=total_scrapes_label_var)
total_successful_scrapes_label = tk.Label(scrape_control_frame, textvariable=total_successful_scrapes_label_var)
total_tokens_label = tk.Label(scrape_control_frame, textvariable=total_tokens_label_var)
get_stats_button = tk.Button(master=scrape_control_frame, text = "Update Stats", command=get_stats)
display_text_button = tk.Button(master=scrape_control_frame, text = "View Scrapes", command=read_files)

# Place the widgets onto the canvas
college_selectcount_label.pack()
count_label.pack()
scrape_selectcount_label.pack()
scrape_count_label.pack()
results_listbox.pack(side='left', fill='both')
scrollbar.pack(side='right', fill='both')
scrape_results_listbox.pack(side='left', fill='both')
scrape_scrollbar.pack(side='right', fill='both')
results_listbox.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = results_listbox.yview)
scrape_results_listbox.config(yscrollcommand = scrape_scrollbar.set)
scrape_scrollbar.config(command = scrape_results_listbox.yview)
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
scrape_list_box_frame.grid(row=0, column=2)
scrape_button.pack()
scrape_control_frame.grid(row=0, column=3)
token_radio.pack()
no_token_radio.pack()
all_token_radio.pack()
total_scrapes_label.pack()
total_successful_scrapes_label.pack()
total_tokens_label.pack()
get_stats_button.pack()
display_text_button.pack()

# Run the main loop and close the psycopg2 cursor once the GUI is closed
window.mainloop()
cursor.close()
