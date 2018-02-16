from concurrent import futures
import time
import os
import io
import paths
from lxml import etree

import grpc

import driversdb_pb2
import driversdb_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class InsuranceServicer(driversdb_pb2_grpc.InsuranceServicer):
	
	def __init__(self):
		pass

	def Analize(self, request, context):

		usr_tests_path = paths._DBPATH + "/" + str(request._targa_) + "/TESTS"
		if not os.path.exists(usr_tests_path)
			os.makedirs(usr_tests_path)

		strtime = time.ctime(request._timestamp_)
		alc_lvl = request._alc_lvl_

		driver_cf = request._driver_._cf_
		driver_name = request._driver_._name_

		
		#img = io.FileIO("./test.jpg", 'w')
		#img.write(request._driver_._photo_)
		#img.close()

		print "usr_test_path = " + usr_tests_path
		print "time = " + strtime
		print "alc_lvl = " + str(alc_lvl)

		print "driver_id = " + driver_id
		print "driver_name = " + driver_name


		return driversdb_pb2.ACK(_result_ = "OK")
		

	def TrainerUpdate(self, request, context):
		pass
	

def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	driversdb_pb2_grpc.add_InsuranceServicer_to_server(InsuranceServicer(), server)
	server.add_insecure_port('[::]:50052')
	server.start()
	try:
		while True:
			time.sleep(_ONE_DAY_IN_SECONDS)
	except KeyboardInterrupt:
		server.stop(0)

if __name__ == '__main__':
	serve()
