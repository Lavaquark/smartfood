from picamera import PiCamera
from time import sleep
# Import gcloud
from google.cloud import storage
import datetime

# Enable Storage
client = storage.Client()

# Reference an existing bucket.
bucket = client.get_bucket('smartfood-184220.appspot.com')
mydatetime = datetime.datetime.now()
print mydatetime
mypicname = 'camerapic_in_{:%Y-%m-%d:%H:%M:%S}.jpg'.format(mydatetime)
print mypicname
camera = PiCamera()
camera.start_preview()
camera.capture('/home/pi/Desktop/' + mypicname)

# Upload a local file to a new file to be created in your bucket.
imageBlob = bucket.blob(mypicname)
if not imageBlob:
	print "nooo"

imageBlob.upload_from_filename(filename='/home/pi/Desktop/' + mypicname)
camera.stop_preview()
