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
	
		if os.path.isfile(paths._DBPATH + "/" + str(request._targa_) + "/tests.xml"):
			doc = etree.parse(paths._DBPATH + "/" + str(request._targa_) + "/tests.xml")
		else:
			doc = etree.Element('tests', targa = request._targa_)
			doc = etree.ElementTree(doc)
	  
	 	testsElt = doc.getroot()
		
		testElt = etree.Element('test', time = str(request._timestamp_))

		timeElt = etree.Element('date')
		timeElt.text =  time.ctime(request._timestamp_)
		testElt.append(timeElt)
		
		alcLvlElt = etree.Element('alcLvl')
		alcLvlElt.text = str(request._alc_lvl_)
		testElt.append(alcLvlElt)

		if request._driver_._known_ == 0:
			driverElt = etree.Element('autista', cf = request._driver_._cf_)
			driverNameElt = etree.Element('nome', request._driver_._name_)
		else:
			driverElt = etree.Element('autista', cf = "Sconosciuto")
		
		testsimg_path = paths._DBPATH + "/" + str(request._targa_) + "/TESTSIMG"
		if not os.path.exists(testsimg_path):
			os.makedirs(testsimg_path)

		img = io.FileIO(testsimg_path + '/' + str(request._timestamp_) + '.jpg', 'w')
		img.write(request._driver_._photo_)
		img.close()

		testElt.append(driverElt)

		testsElt.append(testElt)

		outXML = open(paths._DBPATH + "/" + str(request._targa_) + "/tests.xml", 'w')
		doc.write(outXML)
		outXML.close()

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
