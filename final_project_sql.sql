CREATE TABLE college_info
(college_id INT, name VARCHAR(150), city VARCHAR(50), state CHAR(2), website VARCHAR(250),
highest_degree INT, control INT, locale INT, class INT, religion INT, admission FLOAT,
act_score FLOAT, sat_score FLOAT, enrollment INT, operating INT, in_state_tuition INT,
out_state_tuition INT, family_income FLOAT, level INT, PRIMARY KEY (college_id));


college_id, name, city, state, website, highest_degree, control, locale, class, religion, admission, act_score,
sat_score, enrollment, operating, in_state_tuition, out_state_tuition, family_income, level



CREATE TABLE scrape_info
( scrape_id SERIAL PRIMARY KEY,
college_id INT,
date_time TIMESTAMP WITH TIME ZONE,
file_name VARCHAR(100),
pages_count INT,
fault_count INT,
FOREIGN KEY (college_id) REFERENCES college_info ON DELETE CASCADE);


CREATE TABLE scrape_info (scrape_id SERIAL PRIMARY KEY, college_id INT,
date_time TIMESTAMP WITH TIME ZONE, file_name VARCHAR(100), pages_count INT,
fault_count INT, FOREIGN KEY (college_id) REFERENCES college_info ON DELETE CASCADE);

CREATE TABLE nlp_info
( nlp_file_id = SERIAL PRIMARY KEY,
scrape_id INT,
file_name VARCHAR(100),
token_count INT,
FOREIGN KEY (scrape_id) REFERENCES scrape_info ON DELETE CASCADE);
)

CREATE TABLE nlp_info ( nlp_file_id = SERIAL PRIMARY KEY, scrape_id INT,
file_name VARCHAR(100), token_count INT, FOREIGN KEY (scrape_id) REFERENCES scrape_info ON DELETE CASCADE);

