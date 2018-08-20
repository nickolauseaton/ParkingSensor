import time
import RPi.GPIO as GPIO
import pyrebase

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
timeout = 0.020

# Firebase config
config = {
  "apiKey": "AIzaSyDrHzhjt4JxNps_JrLaXFUjHUyHI4p-DnY",
  "authDomain": "parkingapplication-f6f50.firebaseapp.com",
  "databaseURL": "https://parkingapplication-f6f50.firebaseio.com/",
  "storageBucket": "parkingapplication-f6f50.appspot.com"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

isTaken = 0 # Current status of the parking spot


while 1:
        GPIO.setup(11, GPIO.OUT)
        #cleanup output
        GPIO.output(11, 0)

        time.sleep(0.000002)

        #send signal
        GPIO.output(11, 1)

        time.sleep(0.000005)

        GPIO.output(11, 0)

        GPIO.setup(11, GPIO.IN)
        
        goodread=True
        watchtime=time.time()
        while GPIO.input(11)==0 and goodread:
                starttime=time.time()
                if (starttime-watchtime > timeout):
                        goodread=False

        if goodread:
                watchtime=time.time()
                while GPIO.input(11)==1 and goodread:
                        endtime=time.time()
                        if (endtime-watchtime > timeout):
                                goodread=False
        
        if goodread:
                duration=endtime-starttime
                distance=duration*34000/2
				if distance <= 30 and isTaken == 0:
					db.child("lot1").update({"spot1": 1})
					isTaken = 1
				elif distance > 30 and isTaken:
					db.child("lot1").update({"spot1": 0})
					isTaken = 0
                print distance
		
		# Check every 5 seconds
		time.sleep(5)
