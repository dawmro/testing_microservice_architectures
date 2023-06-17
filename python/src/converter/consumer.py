import pika, sys, os, time
from pymongo import MongoClient
import gridfs
# import module from created convert package
from convert import to_mp3


def main():
	# create instance of mongodb client to get access to dbs in mongo database
	client = MongoClient("host.minihube.internal", 27017)
	db_videos = client.videos
	db_mp3s = client.mp3s
	# gridfs to handle large files
	fs_videos = gridfs.GridFS(db_videos)
	fs_mp3s = gridfs.GridFS(db_mp3s)
	
	# configure rabbitmq connection
	connection = pika.BlockingConnection(
		pika.ConnectionParameters(host="rabbitmq")
	)
	channel = connection.channel()
	
	# execute when message is taken off the queue
	def callback(ch, method, properties, body):
		# convert video to mp3
		err = to_mp3.start(body, fs_videos, fs_mp3s, ch)
		# send negative ack if there is an error, make message stay in queue
		if err:
			ch.basic_nack(delivery_tag = method.delivery_tag)
		# ack message if no error
		else:
			ch.basic_ack(delivery_tag = method.delivery_tag)	
	
	# set messages to consume
	channel.basic_consume(
		queue = os.environ.get("VIDEO_QUEUE"),
		on_message_callback = callback
	)
	
	print("Waiting for messages... To exit press CTRL+C")
	# start consumming messages
	channel.start_consuming()
	
	
if __name__ == "__main__":
	# run main function
	try:
		main()
	# wait for keyboard interrupt
	except KeyboardInterrupt:
		print("Interrupted")
		# shut down service in civilized manner
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
			
	
