from picamera.array import PiRGBArray
import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import io
import cv2

import face
import mq

import grpc

import driversdb_pb2
import driversdb_pb2_grpc

cam = PiCamera()
cam.resolution = (640, 480)
cam.framerate = 32

MQ = mq.MQ()

targa = "FF444FF" 

faceLedPin = 18
alcLedPin = 16

"""
def Init(stub, _targa):
	targa = driversdb_pb2.Targa(_targa_ = _targa)
	config = stub.InitDevice(targa)

	face_rcg = open("./face_recognizer.xml", "w")
	face_rcg.write(config._face_recogn_)
	face_rcg.close()
	
	data_dev = open('./data_dev.xml', 'w')
	data_dev.write(config._data_dev_)
	data_dev.close()
"""
def getAlcLvl():
    alcLvl = MQ.MQPercentage()
    alcLvl = alcLvl["GAS_ALCOHOL"]
    #trasforma alclvl in qualcosa
    return int(alcLvl)


def getFacePicture():

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
        cv2.imshow("Frame", img)
        key = cv2.waitKey(10) & 0xFF
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        if time.time() > ti + 1:
            return None
	

def send_fintest(stub, targa_, foto_):

	test = driversdb_pb2.Test(_targa_ = targa_, _timestamp_ = int(time.time()))

	img = open(foto_, "rb", buffering=0)
	test._foto_ = img.read()
	img.close()

	ack = stub.finalReport(test)
	return ack

def send_initest(stub, targa_ , foto_, alc_lvl_):

	test = driversdb_pb2.Test(_targa_ = targa_, _timestamp_ = int(time.time()), _alc_lvl_ = alc_lvl_)

	img = open(foto_, "rb", buffering=0)
	test._foto_ = img.read()
	img.close()

	ack = stub.initReport(test)
	return ack
    
def initialTest():
    channel = grpc.insecure_channel('131.114.209.143:50052')
    stub = driversdb_pb2_grpc.InsuranceStub(channel)
    
    #initGPIO()
    img = None
    while True:
        while img is None:
            img = getFacePicture()
        ti = time.time()
        GPIO.output(faceLedPin, GPIO.HIGH)
        time.sleep(1)
        alcLvl = getAlcLvl()
        time.sleep(1)
        tf = time.time()
        img = None
        while tf < ti + 5 and img is None:
            img = getFacePicture()
            tf = time.time()
        
        if tf < ti + 5:
            GPIO.output(alcLedPin, GPIO.HIGH)
    	    cv2.imwrite('temp.jpg' , img)
            send_initest(stub, targa, 'temp.jpg', alcLvl)
            break
        else:
            GPIO.output(faceLedPin, GPIO.LOW)
        
    time.sleep(5)
    GPIO.output(faceLedPin, GPIO.LOW)
    GPIO.output(alcLedPin, GPIO.LOW)

def finalTest():
    channel = grpc.insecure_channel('192.168.43.45:50052')
    stub = driversdb_pb2_grpc.InsuranceStub(channel)

    #initGPIO()
    # effettua il test dell'alcol e contemporaneamente fai una foto
    img = None
    while img is None:
        img = getFacePicture()
    cv2.imwrite('temp.jpg' , img)
    send_fintest(stub, targa, 'temp.jpg')

    GPIO.output(faceLedPin, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(faceLedPin, GPIO.LOW)

def initGPIO():

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(faceLedPin, GPIO.OUT)#, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(alcLedPin, GPIO.OUT)#, pull_up_down=GPIO.PUD_UP)
    GPIO.output(faceLedPin, GPIO.LOW)
    GPIO.output(alcLedPin, GPIO.LOW)
    GPIO.setwarnings(False)
