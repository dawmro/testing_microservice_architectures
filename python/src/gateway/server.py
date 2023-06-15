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


# create login route to communicate with auth service
@server.route("/login", methods=["POST"])
def login():
	token, err = access.login(request)
	
	if not err:
		return token
	else:
		return err
		
		
# create route to upload video 
@server.route("/upload", methods=["POST"])
def upload():
	# check if user has a token fron login route
	access, err = validate.token(request)
	
	# convert json string of access to python object
	access = json.loads(access)
	
	# check for admin rights claim
	if access["admin"]:
		# check if there is one file
		if len(request.files) > 1 or len(request.files) < 1:
			return "exactly 1 file required", 400
		
		# iterate through key-value in request.files dict
		for _, f in request.files.items():
			# upload file, return error if something went wrong
			err = util.upload(f, fs, channel, access)
			# check if something went wrong
			if err:
				return err		
		return "success", 200
		
	# if user is not authorized
	else:
		return "not authorized", 401
	
	
# create route to download created mp3 file
@server.route("/download", methods=["GET"])	
def download():
	pass
	
	
if __name__ == "__main__":
    # run flask server
    server.run(host="0.0.0.0", port=8080)
	
	
	
	
	
	
	
	
	
	
	
	
