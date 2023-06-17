import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor


def start(message, fs_videos, fs_mp3s, channel):
	# deserialize message from json to python object
	message = json.loads(message)
	
	# create empty temporary file to store video content
	tf = tempfile.NamedTemporaryFile()
	# convert string version fo video_fid to object and use it to get file from mongodb 
	out = fs_videos(get(ObjectId(message["video_fid"])))
	# put video content into empty file, read data from out variable and write it into temp file
	tf.write(out.read())
	# create audio form temp video file
	audio = moviepy.editor.VideoFileClip(tf.name).audio
	tf.close()
	
	# set path of audio tempfile using unique video file id
	tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
	# write audio to file
	audio.write_audiofile(tf_path)
	
	# save file to mongo db
	f = open(tf_path, "rb")
	data = f.read()
	fid = fs_mp3s.put(data)
	f.close()
	
	# delete audio tempfile
	os.remove(tf_path)
	
	# update message with string version of fid object from uploading audio to mongo db
	message["mp3s_fid"] = str(fid)
	
	# put message on queue
	try:
		channel.basic_publish(
			exchange="",
			routing_key=os.environ.get("MP3_QUEUE"),
			body=json.dumps(message),
			properties=pika.BasicProperties(
				delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
			),
		)
	# delete mp3 from mongo db in case of error when message can not be created	
	except Exception as err:
		fs_mp3s.delete(fid)
		return "failed to publish message"
	
	
	
	
	
	
	
	
	
	
		
		)
