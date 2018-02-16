import time
import io

import grpc

import driversdb_pb2
import driversdb_pb2_grpc

def send_test(stub, id_, alc_lvl_):

	test = driversdb_pb2.Test(__id__ = id_, __alc_lvl__ = alc_lvl_, __timestamp__ = int(time.time()))

	test.__driver__.__known__ =  0
	test.__driver__.__id__ = "None"
	test.__driver__.__name__ = "Unknown"

	img = open("./test-data/test1.jpg", "rb", buffering=0)
	test.__driver__.__photo__ = img.read()

	ack = stub.Analize(test)
	return ack

def run():
	channel = grpc.insecure_channel('localhost:50052')
	stub = driversdb_pb2_grpc.InsuranceStub(channel)

if __name__ == '__main__':
	run()
