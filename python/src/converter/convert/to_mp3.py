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
	

	
	
	
	
	
	
	
	
	
	
		
		)
