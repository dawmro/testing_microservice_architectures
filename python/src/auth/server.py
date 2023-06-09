import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

# create server as a Flask object
server = Flask(__name__)

# config for mysql connection
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

# connect Flask to MySQL database
mysql = MySQL(server)