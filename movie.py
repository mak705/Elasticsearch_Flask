from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import MySQLdb
import datetime

es = Elasticsearch()

q = {"size": 1000, "query": {"match_all": {}}}
search = es.search(index="movie_data", body=q)

app = Flask(__name__)

# {"query": {"range": {"IMDB Rating": {"gte": 6}}}}
# {"query": {"range": {"IMDB Rating": {"lte": 6}}}}
# {"from":0, "size":1000, "query": {"bool": {"must": {"query_string": { "query": variable, "fields": ["name^24"]}}}}}


@app.route('/', methods=["GET", "POST"])
def first_page():
    full_response_list = []
    search_count = []
    count = 0
    db = MySQLdb.connect("localhost", "root", "12345678", "test")
    cursor = db.cursor()
    if request.method == "POST":

        query = request.form.get("query")
        cursor.execute("select count(*) from most_searched_values where  search_term = %s", [query])
        count_exist = cursor.fetchone()
        if count_exist[0] == 0:
            cursor.execute("INSERT INTO most_searched_values (search_term, counts, submission_date ) "
                           "VALUES (%s, %s, %s)",
                           (query, '1', datetime.datetime.now().date()))
            db.commit()

        else:
            cursor.execute("select counts from most_searched_values where  search_term = %s", [query])
            count_exist = cursor.fetchone()[0]
            count_exist += 1
            print('count_exist', count_exist)
            cursor.execute("update most_searched_values set counts = %s  where search_term=  %s", (count_exist, query))
            db.commit()

        if query is not None and query != "":
            # search_response = es.search(index="movie_data", body=
            # {"from": 0, "size": 1000, "query": {"fuzzy": {"query": query}}})
            search_response = es.search(index="movie_data", body=
            {"from": 0, "size": 1000, "query": {"bool": {"must": {"query_string": {"query": query}}}}})
        else:
            search_response = es.search(index="movie_data", body={"from": 0, "size": 1000,
                                                                  "query": {"bool": {"must": {"match_all": {}}}}})

    else:
        search_response = es.search(index="movie_data", body={"from": 0, "size": 1000,
                                                              "query": {"bool": {"must": {"match_all": {}}}}})

        cursor.execute("select search_term, counts from most_searched_values order by counts desc limit 2")
        search_count = cursor.fetchall()
        print("search_count", search_count)

    for i in search_response['hits']['hits']:
        # for i in search['hits']['hits']:
        response = {'id': i['_source']['id'], 'Title': i['_source']['Title']}

        full_response_list.append(response)

    return render_template("movie1.html", data=full_response_list, data_count=search_count)


@app.route('/second')
def second():
    id_value = request.args.get('id')
    search_value = es.search(index="movie_data", body={"query": {"term": {"id": id_value}}})
    # print(search_value['hits']['hits'][0]['_source'])
    # elements = str(search_value['hits']['hits'][0]['_source'])
    # return elements
    elements = search_value['hits']['hits'][0]['_source']
    return render_template("movie_second.html", data=elements)


if __name__ == '__main__':
    app.run(debug=True)
