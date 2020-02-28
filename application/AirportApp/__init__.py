from flask import Flask
import pymysql

pymysql.install_as_MySQLdb()

try:
    from .routing import Routing
except ModuleNotFoundError:
    from routing import Routing

app = Flask(__name__)
Routing(app)

if __name__ == "__main__":
    app.run()
