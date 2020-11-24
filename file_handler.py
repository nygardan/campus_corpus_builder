import os
import json
from nltk import wordpunct_tokenize


def write_to_file(college_id, date, content):
    dir = os.path.dirname(__file__)
    # Put the last part in a separate string and return it so it can be put in the database.
    file_name = str(college_id) + '_' + str(date) + '.scrape'
    file_path = os.path.join(dir, 'scrapes', file_name)
    print(file_path)
    new_file = open(file_path, 'w', encoding='utf-8')
    new_file.write(content)
    new_file.close()
    print("Write completed.")
    return file_name

def process_nlp_to_file(file_name, date, content):
    dir = os.path.dirname(__file__)
    new_file_name = file_name + '.json'
    file_path = os.path.join(dir, 'scrapes', new_file_name)

    # Use nltk to tokenize.
    processed_content = wordpunct_tokenize(content)

    # This is causing a Unicode Decode error in some instances (VMI, for instance) - keep searching for the solution!
    new_file = open(file_path, 'w', encoding='utf-8')
    json.dump(processed_content, new_file, ensure_ascii=False)
    new_file.close()
    print('Processed NLP file completed')
    return (new_file_name, str(len(processed_content)))
    


