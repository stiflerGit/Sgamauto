from picamera.array import PiRGBArray
import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import io
import cv2
from PIL import Image

import face
import mq

import grpc

import driversdb_pb2
import driversdb_pb2_grpc

cam = PiCamera()
cam.resolution = (640, 480)
cam.framerate = 32

MQ = mq.MQ()

faceLedPin = 38 
alcLedPin = 40 


class clientDevice():
    
    def __init__(self, targa, serverip, porta):
        self.targa = targa
        channel = grpc.insecure_channel(serverip +":"+porta)
        self.stub = driversdb_pb2_grpc.InsuranceStub(channel)
	#GPIO.setmode(GPIO.BOARD)
	GPIO.setup(faceLedPin, GPIO.OUT)
	GPIO.setup(alcLedPin, GPIO.OUT)
	GPIO.output(faceLedPin, GPIO.LOW)
	GPIO.output(alcLedPin, GPIO.LOW)
	#GPIO.setwarnings(False)

    def getAlcLvl(self):
        alcLvl = MQ.MQPercentage()
        alcLvl = alcLvl["GAS_ALCOHOL"]
        #trasforma alclvl in qualcosa
        return int(alcLvl)

    def getFacePicture(self):

        ti = time.time()
        rawCapture = PiRGBArray(cam, size=(640, 480))
        for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
            img = frame.array
            fc, rect = face.detect_face(img)
            if(fc is not None):
                (x,y,w,h) = rect
                if (w > 280 and h > 280):
                    rawCapture.truncate(0)
                    return img
            # show the frame
            #img2 = Image.fromarray(img, 'RGB')
            #img2.show()
            #cv2.imshow("Frame", img)
            #key = cv2.waitKey(10) & 0xFF
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)
            if time.time() > ti + 1:
                return None
	
    def sendFinTest(self, foto_):

	test = driversdb_pb2.Test(_targa_ = self.targa, _timestamp_ = int(time.time()))

	img = open(foto_, "rb", buffering=0)
	test._foto_ = img.read()
	img.close()

	ack = self.stub.finalReport(test)
	return ack

    def sendIniTest(self, foto_, alcLvl_):

	test = driversdb_pb2.Test(_targa_ = self.targa, _timestamp_ = int(time.time()), _alc_lvl_ = alcLvl_)

	img = open(foto_, "rb", buffering=0)
	test._foto_ = img.read()
	img.close()

	ack = self.stub.initReport(test)
	return ack
    
    def initialTest(self):

    	#initGPIO()
	img = None
	while True:
        	while img is None:
			img = self.getFacePicture()
        	ti = time.time()
        	GPIO.output(faceLedPin, GPIO.HIGH)
        	time.sleep(1)
        	alcLvl = self.getAlcLvl()
        	time.sleep(1)
        	tf = time.time()
        	img = None
        	while tf < ti + 5 and img is None:
            		img = self.getFacePicture()
            		tf = time.time()
		if tf < ti + 5:
			GPIO.output(alcLedPin, GPIO.HIGH)
			cv2.imwrite('temp.jpg' , img)
			self.sendIniTest('temp.jpg', alcLvl)
			break
	        else:
			GPIO.output(faceLedPin, GPIO.LOW)
       		
	time.sleep(5)
	GPIO.output(faceLedPin, GPIO.LOW)
	GPIO.output(alcLedPin, GPIO.LOW)

    def finalTest(self):
	   
	#initGPIO()
	# effettua il test dell'alcol e contemporaneamente fai una foto
	img = None
	while img is None:
       		img = self.getFacePicture()
	cv2.imwrite('temp.jpg' , img)
	self.sendFinTest('temp.jpg')
	GPIO.output(faceLedPin, GPIO.HIGH)
	time.sleep(5)
	GPIO.output(faceLedPin, GPIO.LOW)


