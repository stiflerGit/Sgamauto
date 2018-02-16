import time
import io

import grpc

import driversdb_pb2
import driversdb_pb2_grpc

def send_test(stub, targa_ , alc_lvl_):

	test = driversdb_pb2.Test(_targa_ = targa_, _timestamp_ = int(time.time()), _alc_lvl_ = alc_lvl_)

	test._driver_._known_ = 1 
	test._driver_._cf_ = "None"
	test._driver_._name_ = "Unknown"

	img = open("./test-data/test1.jpg", "rb", buffering=0)
	test._driver_._photo_ = img.read()

	ack = stub.Analize(test)
	return ack

def run():
	channel = grpc.insecure_channel('localhost:50052')
	stub = driversdb_pb2_grpc.InsuranceStub(channel)
	send_test(stub, 'afasf', 3)

if __name__ == '__main__':
	run()
