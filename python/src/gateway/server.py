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

# config for mongodb connection
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos

# wrap flask server to interface with mongodb
mongo = pyMongo(server)

# wrap mongo.db into gridfs to handle files larger than 16MB
fs = gridfs.GridFS(mongo.db)

# configure rabbitmq connection, make communication with queue synchronous
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq")
# create channel
channel = connection.channel()
