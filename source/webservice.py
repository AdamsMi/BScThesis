__author__ = 'dominikmajda'

#!flask/bin/python
from flask import Flask, jsonify, request
from search_engine import SearchClient

PORT = 9458
HOST = "0.0.0.0"

app = Flask(__name__)
searchClient = SearchClient()

@app.route('/search')
def data():
    query = request.args.get('query')
    result, queryTime = searchClient.search(query)
    return jsonify({"status": "OK", "result":result, "query_time":queryTime})

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)