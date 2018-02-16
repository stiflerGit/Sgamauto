import cv2
import numpy as np
import face

#recognizer = cv2.createEigenFaceRecognizer()
#recognizer = cv2.createFisherFaceRecognizer()
recognizer = cv2.createLBPHFaceRecognizer()

recognizer.load('face_recognizer.xml')

cam = cv2.VideoCapture(0)

subjects = [ "Gianmarco", "Stefano", "Michele", "Stefano_PN", "Virgilio", "Tore", "Andrea"]

while True:
    ret, img = cam.read()
    #detect face from the image
    gray, rect = face.detect_face(img)
    #predict the image using our face recognizer 
    if(gray != None):
        label, confidence = recognizer.predict(gray)
	print "label = " + str(label) + " conf =  " + str(confidence)
        #get name of respective label returned by face recognizer
        label_text = subjects[label]

        #draw a rectangle around face detected
        face.draw_rectangle(img, rect)
        #draw name of predicted person
        if(confidence < 50):
            face.draw_text(img, label_text, rect[0], rect[1]-5)
        else:
            face.draw_text(img, "Unknow", rect[0], rect[1]-5)
    cv2.imshow('Face',img) 
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()
