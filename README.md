## Elasticsearch_Flask

Prerequisites
1. Elasticsearch  >
pip install elasticsearch

2. Flask > 
pip install flask

3. Mysql >
pip install MySQL-python

`Start the elasticsearch` 
C:\Users\user\Downloads\bigdata\elasticsearch-7.8.0\bin>elasticsearch

(server, username, password, databsename) ==> ("localhost", "root", "12345678", "test")

How to create a table > 
create table most_searched_values(
   ID INT NOT NULL AUTO_INCREMENT,
   search_term VARCHAR(100) NOT NULL,
   counts INT(40) NOT NULL,
   submission_date DATE,
   PRIMARY KEY ( ID )
);

How to save the data in the index >

"movie_data.json" is present in the static folder. 

using the below command insert in to the Es index

data is the content inside the movie_data.json

```
data = []
for e in data:
    es.index(index="movie_data", body=e, id=e['id'])
```
How to run? > 
python movie.py

You can search the parameter in the box, and Searched item will displayed below, It will be search in the entire index



