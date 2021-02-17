from flask import Flask, url_for, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch()

resp = {}



@app.route('/', methods=["GET", "POST"])
def index():
    global resp
    q = request.args.get("q")
    # q = request.form.get("q")
    if q is not None and q != "":
        # resp = es.search(index="data_new", body={"query": {"function_score": {"query": {
        #     "multi_match": {"query": q, "fields": ["name^24", "professor^8"],
        #                     "operator": "OR", "type": "cross_fields"}}}}})
        # resp = es.search(index="data_new", body={"from":0, "size":1000,
        #                                          "query": {"bool": {"must":
        #                             {"query_string": { "query":q +'*', "fields": ["name^24"]}}}}})

        # resp = es.search(index="data_new", body={"from": 0, "size": 1000,
        #                                          "query": {"bool": {"must":
        #                                                                 {"query_string": {"query": q + '*',
        #                                                                                   "fields": ["name^24"]}}}},
        #                                          "highlight": {
        #                                              "fields": {
        #                                                  "*": {}}}
        #
        #                                          })

        resp = es.search(index="data_new", body={"from": 0, "size": 1000,
                                                 "query": {"bool": {"must":
                                                                        {"query_string": {"query": q + '*',
                                                                                          "fields": ["name^24"]}}}},
                                                 "highlight": {
                                                     # "require_field_match": False,
                                                     "fields": {
                                                         "*": {}}}

                                                 })
        print("q", q)
        print("response", resp)
    else:
        print("q is", q)
        resp = es.search(index="data_new", body={"from": 0, "size": 299,
                                                 "query": {"bool": {"must": {"match_all": {}},
                                                                    "filter": [{"term":
                                                                                    {"parentName.keyword":
                                                                                         "Marketplace Data Products"}}]}}})
    return render_template('index.html', response=resp)

    # return render_template('index.html', q=q, response=resp)
    # return render_template('index.html',q=q)
    # return render_template('index.html')


@app.route('/second', methods=["GET", "POST"])
def second():
    idnum = request.args.get("id")
    print('id', idnum)
    name, prof = "", ""

    for i in resp['hits']['hits']:
        if idnum == i['_source']['id']:
            name = i['_source']['name']
            prof = i['_source']['description']
            print(i['_source']['name'], i['_source']['description'])
    return render_template('second_page.html', name=name, description=prof)


if __name__ == '__main__':
    app.run()
