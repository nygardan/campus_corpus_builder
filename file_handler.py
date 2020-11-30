import os
import json
from nltk import wordpunct_tokenize

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
