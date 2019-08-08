from flask import request
import re


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