__author__ = 'dominikmajda'

#!flask/bin/python
from flask import Flask, jsonify, request
from search_engine import SearchClient
from database_manager import DatabaseManager

PORT = 9458
HOST = "0.0.0.0"

app = Flask(__name__)
dm = DatabaseManager()
searchClient = SearchClient(dm)


@app.route('/search')
def search():
    query = request.args.get('query')
    result, queryTime = searchClient.search(query)


    return jsonify({
        "status": "OK",
        "result":[news.serialize() for news in result],
        "query_time":queryTime
    })

@app.route('/topic')
def clusters():
    clusterId = request.args.get('id')
    print "Received cluster ID", clusterId

    if not clusterId == None:
        path = [int(x) for x in clusterId.split('_')]
        print path
        res = []
        clustering, freqWords = searchClient.getClustering(path)
    else:
        clustering, res, freqWords = searchClient.getInitialClustering()

    for key in clustering:
        clustering[key] = len(clustering[key])

    return jsonify({
        "clustering" : clustering,
        "res" : res,
        "freqWords" : freqWords
    })


@app.route('/articles')
def articles():
    clusterId = request.args.get('id')
    print "Received cluster ID", clusterId

    if clusterId == None:
        return jsonify({
            "status": "OK",
            "result":[],
            "count":0
        })
    else:
        path = [int(x) for x in clusterId.split('_')]
        result = searchClient.getArticles(path)

        return jsonify({
            "status": "OK",
            "result":[news.serialize() for news in result],
            "count":len(result)
        })


if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)