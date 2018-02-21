import cv2
import numpy as np
import face
import paths
from lxml import etree

#recognizer = cv2.createEigenFaceRecognizer()
#recognizer = cv2.createFisherFaceRecognizer()
recognizer = cv2.createLBPHFaceRecognizer()

def recognize(targa, imgpath):
	# carico il recognizer necessario per riconoscere gli autisti di una determinata auto
	recognizer.load(paths._DBPATH + "/" + targa + "/face_recognizer.xml")
	# memorizzo in una lista tutti i soggetti legati a una auto
	doc = etree.parse(paths._XMLDB)
	subjects = doc.findall("./*[@targa='"+targa+"']/*")
	print str(subjects)
	#rilevo la faccia dell'autista nella foto
	img = cv2.imread(imgpath)
	gray, rect = face.detect_face(img)
	if(gray != None):
		label, confidence = recognizer.predict(gray)
		#print "label = " + str(label) + " conf =  " + str(confidence)
		# Ottengo il nome dell'autista legato all'indice restituito dal recognizer
		label_text = subjects[label].find("nome").text
		print label_text
		# Disegno un rettangolo e scrivo il nome intorno alla faccia rilevata
		face.draw_rectangle(img, rect)
		if(confidence < 50):
			face.draw_text(img, label_text, rect[0], rect[1]-5)
			cv2.imwrite(imgpath, img)
			return subjects[label].attrib["cf"]
		else:
			face.draw_text(img, "Sconosciuto", rect[0], rect[1]-5)
	cv2.imwrite(imgpath, img)
	return "Sconosciuto"
