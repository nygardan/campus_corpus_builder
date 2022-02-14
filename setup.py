#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: danygard

Credit to
https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/
for help in understanding how to use the psycopg2 cursor's executemany() method
and for helping me understand how to pull rows out of a dataframe.
Finalized for CSCI 765 12-9-2020

"""


import pandas as pd
import psycopg2

# Set up dataframe (pull from csv) and set up the connection
df = pd.read_csv("college_info_2_13_2022.csv", encoding = "ISO-8859-1", engine='python', na_values='PrivacySuppressed')
try:
    conn = psycopg2.connect(
        dbname= "postgres",
        user = "postgres",
        password = "postgres",
        host = 'localhost',
        port = 5432)
    print("Connected to database.")

except:
    print("Failed to connect to database.")

# Credit for this line of code goes to the website given above
rows = [tuple(x) for x in df.to_numpy(na_value=None)]

cursor = conn.cursor()

# Our query to populate the college_info table
query = """INSERT INTO college_info(college_id, name, city, state, website,
highest_degree, control, locale, class, religion, admission, act_score, sat_score,
enrollment, operating, in_state_tuition, out_state_tuition, family_income, level)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# This clears anything out that may have been in any databases.
# setup.py should not be run again unless you want to reset your databases.
drop_college_table_query = """DROP TABLE IF EXISTS college_info CASCADE"""
drop_scrape_table_query = """DROP TABLE IF EXISTS scrape_info CASCADE"""
drop_nlp_table_query = """DROP TABLE IF EXISTS nlp_info"""

# Create the tables
create_college_table_query = """CREATE TABLE college_info
(college_id INT, name VARCHAR(150), city VARCHAR(50), state CHAR(2), website VARCHAR(250),
highest_degree INT, control INT, locale INT, class INT, religion INT, admission FLOAT,
act_score FLOAT, sat_score FLOAT, enrollment INT, operating INT, in_state_tuition INT,
out_state_tuition INT, family_income FLOAT, level INT, PRIMARY KEY (college_id));"""

create_scrape_table_query = """CREATE TABLE scrape_info (scrape_id SERIAL PRIMARY KEY, college_id INT,
date_time TIMESTAMP WITH TIME ZONE, file_name VARCHAR(100), pages_count INT,
fault_count INT, FOREIGN KEY (college_id) REFERENCES college_info ON DELETE CASCADE);"""

create_nlp_table_query = """CREATE TABLE nlp_info ( nlp_file_id SERIAL PRIMARY KEY, scrape_id INT,
file_name VARCHAR(100), token_count INT, nlp_type VARCHAR(30), FOREIGN KEY (scrape_id) REFERENCES scrape_info ON DELETE CASCADE);"""

try:
    cursor.execute(drop_college_table_query)
    cursor.execute(drop_scrape_table_query)
    cursor.execute(drop_nlp_table_query)
    cursor.execute(create_college_table_query)
    cursor.execute(create_scrape_table_query)
    cursor.execute(create_nlp_table_query)
    cursor.executemany(query, rows)
    conn.commit()
    print("Input completed.")
    loan_amt_query = "SELECT name, city, family_income FROM college_info WHERE state = 'ND'"
    cursor.execute(loan_amt_query)
    results = cursor.fetchall()
    # Our test run - list the schools of North Dakota to see if everything worked.
    for r in results:
        print(r)

except (Exception, psycopg2.DatabaseError) as error:
    print("Database Error {}".format(error))
    conn.rollback()
    cursor.close()

print("Complete.")
cursor.close()
