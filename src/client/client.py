import time
import io

import grpc

import driversdb_pb2
import driversdb_pb2_grpc

def Init(stub, _targa):
	targa = driversdb_pb2.Targa(_targa_ = _targa)
	config = stub.InitDevice(targa)

	face_rcg = open("./face_recognizer.xml", "w")
	face_rcg.write(config._face_recogn_)
	face_rcg.close()
	
	data_dev = open('./data_dev.xml', 'w')
	data_dev.write(config._data_dev_)
	data_dev.close()

def send_test(stub, targa_ , alc_lvl_):

	test = driversdb_pb2.Test(_targa_ = targa_, _timestamp_ = int(time.time()), _alc_lvl_ = alc_lvl_)

	test._driver_._known_ = 1 
	test._driver_._cf_ = "None"
	test._driver_._firstname_ = "Unknown"

	img = open("./test-data/test2.jpg", "rb", buffering=0)
	test._driver_._photo_ = img.read()

	ack = stub.Analize(test)
	return ack

def run():
	grpc.max_send_message_length = -1
	grpc.max_receive_message_length = -1

	channel = grpc.insecure_channel('localhost:50052')
	stub = driversdb_pb2_grpc.InsuranceStub(channel)
	Init(stub, "AB123CD")
	print "Done"


		

if __name__ == '__main__':
	run()
