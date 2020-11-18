import os


def write_to_file(college_id, date, content):
    dir = os.path.dirname(__file__)
    # Put the last part in a separate string and return it so it can be put in the database.
    filename = os.path.join(dir, 'scrapes', (str(college_id) + '_' + str(date) + '.scrape'))
    print(filename)
    new_file = open(filename, 'w')
    new_file.write(content)
    new_file.close()
    print("Write completed.")
    


