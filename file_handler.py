import os


def write_to_file(college_id, date, content):
    dir = os.path.dirname(__file__)
    # Put the last part in a separate string and return it so it can be put in the database.
    file_name = str(college_id) + '_' + str(date) + '.scrape'
    file_path = os.path.join(dir, 'scrapes', file_name)
    print(file_path)
    new_file = open(file_path, 'w')
    new_file.write(content)
    new_file.close()
    print("Write completed.")
    return file_name
    


