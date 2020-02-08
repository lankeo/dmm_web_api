# web server config sample

WEBSERVER = {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": False
}

MONGOSERVER = {
    "host": "192.168.44.20",
    "port": 27017
}

DBNAME = "dmm"

# collections
CO_PRODUCT = "product_v2"
CO_ACTRESS = "actress"
CO_GENRE = "category"


# request erro
ERROR_NO_DATA = {"erro":1, "msg": "No Data"}
