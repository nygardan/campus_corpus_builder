#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: danygard

Credit to 
https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/
for help in understanding how to use the psycopg2 cursor's executemany() method
and for helping me understand how to pull rows out of a dataframe. 

"""

import pandas as pd
import psycopg2

df = pd.read_csv("college_info.csv", encoding = "ISO-8859-1", engine='python', na_values='PrivacySuppressed')
try:    
    conn = psycopg2.connect(
        dbname= "postgres",
        user = "postgres",
        password = "All25star!",
        port = 5432)
    print("Connected to database.")

except:
    print("Failed to connect to database.")

# Credit for this line of code goes to the website given above    
rows = [tuple(x) for x in df.to_numpy(na_value=None)]

##column_list = ['loan_id', 'gender', 'married', 'dependents', 'education',
##       'self_employed', 'applicant_income', 'coapplicant_income', 'loan_amount',
##       'loan_amount_term', 'credit_history', 'property_area', 'loan_status']
##columns = ','.join(list(column_list))
cursor = conn.cursor()
query = """INSERT INTO college_info(college_id, name, city, state, website,
highest_degree, control, locale, class, religion, admission, act_score, sat_score,
enrollment, operating, in_state_tuition, out_state_tuition, family_income, level) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
drop_table_query = """DROP TABLE IF EXISTS college_info"""
create_table_query = """CREATE TABLE college_info
(college_id INT, name VARCHAR(150), city VARCHAR(50), state CHAR(2), website VARCHAR(250),
highest_degree INT, control INT, locale INT, class INT, religion INT, admission FLOAT,
act_score FLOAT, sat_score FLOAT, enrollment INT, operating INT, in_state_tuition INT,
out_state_tuition INT, family_income FLOAT, level INT, PRIMARY KEY (college_id));"""

try:
    cursor.execute(drop_table_query)
    cursor.execute(create_table_query)
    cursor.executemany(query, rows)
    conn.commit()
    print("Input completed.")
    loan_amt_query = "SELECT name, city, family_income FROM college_info WHERE state = 'ND'"
    cursor.execute(loan_amt_query)
    results = cursor.fetchall()
    for r in results:
        print(r)
    
except (Exception, psycopg2.DatabaseError) as error:
    print("Database Error {}".format(error))
    conn.rollback()
    cursor.close()
    
print("Complete.")
cursor.close()



