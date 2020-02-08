from config import WEBSERVER
from api import app

if __name__ == "__main__":
    app.run(**WEBSERVER)