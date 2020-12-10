import os
import json
from nltk import wordpunct_tokenize


# Writes to a .scrape (flat text) file
def write_to_file(college_id, date, content):
    dir = os.path.dirname(__file__)
    # Put the last part in a separate string and return it so it can be put in the database.
    file_name = str(college_id) + '_' + str(date) + '.scrape'
    file_path = os.path.join(dir, 'scrapes', file_name)
    print(file_path)
    with open(file_path, 'w', encoding='utf-8') as new_file:
        new_file.write(content)
    print("Write completed.")
    return file_name

# Tokenizes our scrape content.
# Writes the tokenized list as a .json object to a .json file
def process_nlp_to_file(file_name, date, content):
    dir = os.path.dirname(__file__)
    new_file_name = file_name + '.json'
    file_path = os.path.join(dir, 'scrapes', new_file_name)

    # Use nltk to tokenize.
    processed_content = wordpunct_tokenize(content)

    with open(file_path, 'w', encoding='utf-8') as new_file:
        json.dump(processed_content, new_file, ensure_ascii=False)
    print('Processed NLP file completed')
    return (new_file_name, str(len(processed_content)))

# This reads our scrape files - used in the GUI text viewer.
def read_from_files(file_names):
    dir = os.path.dirname(__file__)
    file_output_list = []
    for file in file_names:
        file_path = os.path.join(dir, 'scrapes', file)
        with open(file_path, 'r', encoding='utf-8') as new_file:
            file_output_list.append(new_file.read())
            new_file.close()
    return file_output_list
