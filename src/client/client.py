from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import io
import cv2

import grpc

import driversdb_pb2
import driversdb_pb2_grpc

cam = PiCamera()
cam.resolution = (640, 480)
cam.framerate = 32

'''
def Init(stub, _targa):
	targa = driversdb_pb2.Targa(_targa_ = _targa)
	config = stub.InitDevice(targa)

	face_rcg = open("./face_recognizer.xml", "w")
	face_rcg.write(config._face_recogn_)
	face_rcg.close()
	
	data_dev = open('./data_dev.xml', 'w')
	data_dev.write(config._data_dev_)
	data_dev.close()
'''

def getFacePicture():
	rawCapture = PiRGBArray(cam, size=(640, 480))
	for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
		img = frame.array
		face, rect = face.detect_face(img)
		if face != None:
			return img	
		# show the frame
		cv2.imshow("Frame", img)
		key = cv2.waitKey(10) & 0xFF
		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)
	

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

def run():
	channel = grpc.insecure_channel('localhost:50052')
	stub = driversdb_pb2_grpc.InsuranceStub(channel)

	# effettua il test dell'alcol e contemporaneamente fai una foto
	#getAlcLvl()
	img = getFacePicture()
	cv2.imwrite('temp.jpg' , img)
	img = open('temp.jpg', 'rb', buffering = 0)
	request._foto_ = img.read()
	img.close()

	send_initest(stub, "EF123GH", 4)
	time.sleep(5)
	send_fintest(stub, "EF123GH")

if __name__ == '__main__':
	run()
