# Elasticsearch_Flask

Prerequisites
1. Elasticsearch 
pip install elasticsearch

2. Flask
pip install flask

3. Mysql
pip install MySQL-python

(server, username, password, databsename) ==> ("localhost", "root", "12345678", "test")

create table most_searched_values(
   ID INT NOT NULL AUTO_INCREMENT,
   search_term VARCHAR(100) NOT NULL,
   counts INT(40) NOT NULL,
   submission_date DATE,
   PRIMARY KEY ( ID )
);


How to run?
python movie.py

You can search the parameter in the box, and Searched item will displayed below



