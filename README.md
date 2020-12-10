# Campus Corpus Builder
A python application that scrapes college websites for text related to Covid-19.
Please read the instructions before running!

# Dependencies
You will have to have Postgres installed on your system.  
The connections for the program are for the default database:  
dbname= "postgres",  
user = "postgres",  
password = "postgres",  
host = 'localhost',  
port = 5432  
  
The program depends on these external python libraries:  
pandas = "*"  
psycopg2-binary = "*"  
requests = "*"  
beautifulsoup4 = "*"  
lxml = "*"  
nltk = "*"  
  
While you can install each directly using pip install _____, it is much more
recommended to use pipenv for this. Pipenv creates a virtual environment
and installs the dependencies in that environment, so your computer
does not become full of extraneous modules installed globally.

## To use pipenv:
Once you have cloned the repository:  
Install pipenv with $ pip install pipenv  
cd into campus-corpus-builder with $ cd campus-corpus-builder  
initiate environment and dependencies: $ pipenv install  
start up the environment: $ pipenv shell  
  
You'll know the environment is created and running when "(campus-corpus-builder)"
appears to the left of the terminal prompt.  
To exit your pipenv environment, type exit into the terminal.

## Add the scrapes folder:
While you're still in the project folder, add the scrapes folder:  
$ mkdir scrapes  
  
This holds the scrape files and .json files the program produces.  

# Running the application
The first time you run the application you'll have to set it up:  
$ python setup.py  
  
This should only be run ONCE per installation or it will reset your scrape and nlp tables
(review the code in setup.py to see how).
  
setup.py runs everything to get set up.
You'll know it worked when you see a list of North Dakota colleges.
  
Once you're set up, run the below to get started:  
$ python campus_corpus_maker.py  
