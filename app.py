from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import re
from config import *

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

client = MongoClient(**MONGOSERVER)
db = client[DBNAME]


def check_num(s, v=None):
    if s is None:
        return v
    rc = re.compile(r'^\d+$')
    ret = rc.match(s)
    return ret[0] if ret is not None else v


def handle_args(default_size=20):
    page = request.args.get('page')
    page_size = request.args.get('pagesize')
    page = check_num(page, 1)
    page_size = check_num(page_size, 10)
    page_size = int(page_size)
    if page_size > default_size:
        page_size = default_size
    skip = (int(page) - 1) * page_size
    return skip, page_size


def handle_query(query):
    dic = dict()
    for k,v in query.items():
        v = request.args.get(v)
        if v is not None:
            v = check_num(v)
            if v is None:
                return
            dic.update({k:v})
    return dic


def handle_sort():
    sort = request.args.get('sort')
    sort_type = {
        "new": [("pub_date", -1)],
        "popular": [("_id", 1)]
    }
    return sort_type.get(sort) if sort is not None else sort_type['new']


@app.route('/api/dnn/actresses')
def actresses():
    co = db[CO_ACTRESS]
    skip, page_size = handle_args() 
    actresses = co.find({},{"_id": 0}).skip(skip).limit(page_size)
    count = co.count()
    return jsonify({"count": count, "actresses": list(actresses)})


@app.route('/api/dnn/actress/<id>')
def actress(id):
    if check_num(id) is None:
        return jsonify(ERROR_NO_DATA)
    co = db[CO_ACTRESS]
    actress = co.find({"act_id":id},{"_id": 0})
    count = co.count({"act_id":id})
    return jsonify({"count": count, "actress": list(actress)})


@app.route('/api/dnn/products')
def products():
    query = {
        "actress.id": "actress",
        "series.id": "series",
        "genre.id": "genre"
    }
    query = handle_query(query)
    if query is None:
        return jsonify(ERROR_NO_DATA)
    co = db[CO_PRODUCT]
    sort = handle_sort()
    skip, page_size = handle_args() 
    products = co.find(query,{"_id":0}).sort(sort).skip(skip).limit(page_size)
    count = co.count(query)
    return jsonify({"count": count, "products": list(products),})


@app.route('/api/dnn/product/<id>')
def product(id):
    if check_num(id) is None:
        return jsonify(ERROR_NO_DATA)
    co = db[CO_PRODUCT]
    product = co.find({"dvd_id":id.upper()},{"_id": 0})
    count = co.count({"dvd_id":id.upper()})
    return jsonify({"count": count, "product": list(product)})


@app.route('/api/dnn/genres')
def genres():
    co = db[CO_GENRE]
    skip, page_size = handle_args()
    query = {
        "cate_l": "cate_l",
        "cate_m": "cate_m",
        "name": "name"
    }
    query = handle_query(query)
    genres = co.find(query,{"_id": 0}).skip(skip).limit(page_size)
    count = co.count(query)
    return jsonify({"count": count, "genres": list(genres)})


@app.route('/api/dnn/genre/<id>')
def genre(id):
    if check_num(id) is None:
        return jsonify(ERROR_NO_DATA)
    co = db[CO_GENRE]
    genre = co.find({"genre_id": id},{"_id": 0})
    count = co.count({"genre_id": id})
    return jsonify({"count": count, "actress": list(genre)})


if __name__ == '__main__':
    app.run(**WEBSERVER)