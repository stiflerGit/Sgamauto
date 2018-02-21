from concurrent import futures
import cv2
import numpy
import time
import os
import io
from lxml import etree
import face
import paths

import grpc

import driversdb_pb2
import driversdb_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24



class InsuranceServicer(driversdb_pb2_grpc.InsuranceServicer):
	
	def __init__(self):
		self.dbTree = etree.parse(paths._XMLDB)
		self.dbpath = paths._DBPATH

	def getDrivers(self, targa_):

		nomiElts = self.dbTree.findall("./*[@targa = '"+ targa_+"']/*/nome")
		autistiElts = self.dbTree.findall("./*[@targa = '"+ targa_+"']/*")
		subjects= []
		cfs = []
		i = 0
		while i < len(nomiElts):
			subjects.append(nomiElts[i].text)
			cfs.append(autistiElts[i].get('cf'))
			i=i+1
		return subjects, cfs


	def initReport(self, request, context):

		targaPath = self.dbpath + "/" + str(request._targa_)

		if os.path.isfile(targaPath + "/tests.xml"):
			doc = etree.parse(targaPath + "/tests.xml")
		else:
			doc = etree.Element('tests', targa = request._targa_)
			doc = etree.ElementTree(doc)
	  
	 	testsElt = doc.getroot()
		
		testElt = etree.Element('test', ti = str(request._timestamp_))

		timeElt = etree.Element('inizio')
		timeElt.text =  time.ctime(request._timestamp_)
		testElt.append(timeElt)
		
		alcLvlElt = etree.Element('alcLvl')
		alcLvlElt.text = str(request._alc_lvl_)
		testElt.append(alcLvlElt)
		
		testsimg_path = targaPath + "/TESTSIMG"
		if not os.path.exists(testsimg_path):
			os.makedirs(testsimg_path)

		subjects, cfs = self.getDrivers(request._targa_)

		buff = numpy.fromstring(request._foto_, dtype = numpy.uint8)
		img = cv2.imdecode(buff, 1)
		img, autista = face.recognize(img, targaPath + "/face_recognizer.xml", subjects)
		cv2.imwrite(testsimg_path + "/" + str(request._timestamp_) + ".jpg" ,img)
		
		if autista != "Sconosciuto":
			autistaElt = etree.Element('autista_iniziale', cf = cfs[subjects.index(autista)])
		else:
			autistaElt = etree.Element('autista_iniziale', cf = "Sconosciuto")
		
		testElt.append(autistaElt)

		testsElt.append(testElt)

		outXML = open(targaPath + "/tests.xml", 'w')
		doc.write(outXML)
		outXML.close()

		return driversdb_pb2.ACK(_result_ = "OK")


	def finalReport(self, request, context):

		targaPath = self.dbpath + "/" + str(request._targa_)

		if os.path.isfile(targaPath + "/tests.xml"):
			doc = etree.parse(targaPath + "/tests.xml")
		else:
			doc = etree.Element('tests', targa = request._targa_)
			doc = etree.ElementTree(doc)
	  
	 	testsElt = doc.getroot()

		testElt = list(testsElt.iter('test'))
		testElt = testElt[len(testElt)-1]
		testElt.set('tf', str(request._timestamp_))

		timeElt = etree.Element('fine')
		timeElt.text =  time.ctime(request._timestamp_)
		testElt.append(timeElt)

		testsimg_path = targaPath + "/TESTSIMG"
		if not os.path.exists(testsimg_path):
			os.makedirs(testsimg_path)

		subjects, cfs = self.getDrivers(request._targa_)

		buff = numpy.fromstring(request._foto_, dtype = numpy.uint8)
		img = cv2.imdecode(buff, 1)
		img, autista = face.recognize(img, targaPath + "/face_recognizer.xml", subjects)
		cv2.imwrite(testsimg_path + "/" + str(request._timestamp_) + ".jpg" ,img)
		
		if autista != "Sconosciuto":
			autistaElt = etree.Element('autista_finale', cf = cfs[subjects.index(autista)])
		else:
			autistaElt = etree.Element('autista_finale', cf = "Sconosciuto")

		testElt.append(autistaElt)

		testsElt.append(testElt)

		outXML = open(targaPath + "/tests.xml", 'w')
		doc.write(outXML)
		outXML.close()

		return driversdb_pb2.ACK(_result_ = "OK")


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
