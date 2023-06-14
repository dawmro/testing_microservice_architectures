import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
# import validate module from created auth package 
from auth import validate
# import module from created auth service package 
from auth_svc import access
# import module from created storage package 
from storage import util


# create server as a Flask object
server = Flask(__name__)


