import cv2
import os
from lxml import etree
import paths
import face
import numpy as np


cam = cv2.VideoCapture()
detector = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')

xml_head = '<?xml version="1.0"?>\n\
<db xmlns="'+paths._XMLSCHEMA+'">\n\
</db>'

if os.path.isfile(paths._XMLDB):
	doc = etree.parse(paths._XMLDB)
else:
	doc = etree.fromstring(xml_head)
	doc = etree.ElementTree(doc)

dbElt = doc.getroot()

_targa = raw_input("inserisci il numero della targa\
o premi q per terminare l'acquisizione dei dati\n")
# verifica targa
autoElt = etree.Element('auto', targa=_targa)

nautisti = int(raw_input("inserisci il numero degli autisti\n"))

targapath = paths._DBPATH + "/" + _targa
if not os.path.exists(targapath):
        os.makedirs(targapath)

autistapath = []
i = 0

while i < nautisti:

        _cf = raw_input("inserisci codice fiscale\n")
        _nome = raw_input("inserisci nome\n")
        _cognome = raw_input("inserisci cognome\n")
        _eta = raw_input("inserisci eta\n")
        _anni_patente = raw_input("inserisci anni patente\n")

        autistaElt = etree.SubElement(autoElt, 'autista', cf=_cf)
        nomeElt = etree.SubElement(autistaElt, 'nome')
        cognomeElt = etree.SubElement(autistaElt, 'cognome')
        etaElt = etree.SubElement(autistaElt, 'eta')
        anni_patenteElt = etree.SubElement(autistaElt, 'anni_patente')

        nomeElt.text = _nome
        cognomeElt.text = _cognome
        etaElt.text = _eta
        anni_patenteElt.text = _anni_patente

        autistapath.append(targapath + "/" + _cf)

        if not os.path.exists(autistapath[i]):
                os.makedirs(autistapath[i])

        # file xml contenente le informazioni
        # decidiamo se mettere tutto in targapath o uno per ogni autistapath

	ret = raw_input("preparati per le foto")

	cam.open(0)
        sampleNum=1
        while sampleNum < 30:
                ret, img = cam.read()
                directory = autistapath[i] + "/training-data"
                if not os.path.exists(directory):
                        os.makedirs(directory)
		face.draw_text(img, str(sampleNum), 10, 30 )
                cv2.imwrite(directory + "/img"+str(sampleNum)+".jpg", img)
                cv2.imshow('frame',img)
                cv2.waitKey(100)
                sampleNum = sampleNum+1

	cam.release()
        i = i+1


cv2.destroyAllWindows()

dbElt.append(autoElt)

outXML = open(paths._XMLDB, 'w')
doc.write(outXML)

#list to hold all subject faces
faces = []

#list to hold labels for all subjects
labels = []

#for use EigenFaceRecognizer by replacing above line with 
#face_recognizer = cv2.createEigenFaceRecognizer()

#for use FisherFaceRecognizer by replacing above line with 
#face_recognizer = cv2.createFisherFaceRecognizer()

#create our LBPH face recognizer 
face_recognizer = cv2.createLBPHFaceRecognizer()

print("Preparing data...")    

#let's go through each directory and read images within it
i = 0;
while i < nautisti:
        #extract label number of subject from dir_name
        #format of dir name = slabel
        #, so removing letter 's' from dir_name will give us label
        label = i

        #build path of directory containin images for current subject subject
        #sample subject_dir_path = "training-data/s1"
        subject_dir_path = autistapath[i]  + "/training-data"

        #get the images names that are inside the given subject directory
        subject_images_names = os.listdir(subject_dir_path)

        #------STEP-3--------
        #go through each image name, read image, 
        #detect face and add face to list of faces
        for image_name in subject_images_names:

                #ignore system files like .DS_Store
                if image_name.startswith("."):
                        continue;

                #build image path
                #sample image path = training-data/s1/1.pgm
                image_path = subject_dir_path + "/" + image_name

                #read image
                image = cv2.imread(image_path)

                #display an image window to show the image 
                #cv2.imshow("Training on image...", cv2.resize(image, (400, 500)))
                #cv2.waitKey(300)

                #detect face
                faceimg, rect = face.detect_face(image)

                #------STEP-4--------
                #for the purpose of this tutorial
                #we will ignore faces that are not detected
                if faceimg is not None:
                #add face to list of faces
                        cv2.imshow("Face founded...", faceimg)
                        cv2.waitKey(10)
                        faces.append(faceimg)
                        #add label for this face
                        labels.append(label)

                #cv2.waitKey(1)
                #cv2.destroyAllWindows()
        i = i + 1

print("Data prepared")
#print total faces and labels
print("Total faces: ", len(faces))
print("Total labels: ", len(labels))

face_recognizer.train(faces, np.array(labels))
face_recognizer.save(targapath +'/face_recognizer.xml')

'''
if face_recognizer.train(faces, np.array(labels)) != None:
print "Train sucessfully complete"
face_recognizer.save("face_recognizer.xml")
else:
print "Train error"
'''
