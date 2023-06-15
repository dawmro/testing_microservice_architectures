import pika, json


def upload(f, fs, channel, access):
	# put file into mongodb database
	try: 
		# get file if success
		fid = fs.put(f)
	except Exception as err:
		return "internal server error", 500
	
	# create message 
	message = {
		"video_fid": str(fid),
		"mp3_fid": None,
		# who owns the file
		"username": access["username"],
	}	
	# put message in queue
	try:
		channel.basic_publish(
			exchange="",
			routing_key="video",
			# convert python object to json string
			body=json.dumps(message),
			properties=pika.BasicProperties(
				# make messages persistent
				delivery_mode=pika.PERSISTENT_DELIVERY_MODE
			),
		)
	# if message unsuccesfully added to the queue			
	except:
		# delete file, because it's not connected to any message
		fs.delete(fid)
		return "internal server error", 500
	
