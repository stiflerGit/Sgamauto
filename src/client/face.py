import cv2
import numpy as np
import sys, math
from PIL import Image


def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)


def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)


def Distance(p1,p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.sqrt(dx*dx+dy*dy)


def ScaleRotateTranslate(image, angle, center = None, new_center = None, scale = None, resample=Image.BICUBIC):
    if (scale is None) and (center is None):
        return image.rotate(angle=angle, resample=resample)
    nx,ny = x,y = center
    sx=sy=1.0
    if new_center:
        (nx,ny) = new_center
    if scale:
        (sx,sy) = (scale, scale)
    cosine = math.cos(angle)
    sine = math.sin(angle)
    a = cosine/sx
    b = sine/sx
    c = x-nx*a-ny*b
    d = -sine/sy
    e = cosine/sy
    f = y-nx*d-ny*e
    return image.transform(image.size, Image.AFFINE, (a,b,c,d,e,f), resample=resample)


def CropFace(image, eye_left=(0,0), eye_right=(0,0), offset_pct=(0.2,0.2), dest_sz = (70,70)):
    # calculate offsets in original image
    offset_h = math.floor(float(offset_pct[0])*dest_sz[0])
    offset_v = math.floor(float(offset_pct[1])*dest_sz[1])
    # get the direction
    eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
    # calc rotation angle in radians
    rotation = -math.atan2(float(eye_direction[1]),float(eye_direction[0]))
    # distance between them
    dist = Distance(eye_left, eye_right)
    # calculate the reference eye-width
    reference = dest_sz[0] - 2.0*offset_h
    # scale factor
    scale = float(dist)/float(reference)
    # rotate original around the left eye
    image = ScaleRotateTranslate(image, center=eye_left, angle=rotation)
    # crop the rotated image
    crop_xy = (eye_left[0] - scale*offset_h, eye_left[1] - scale*offset_v)
    crop_size = (dest_sz[0]*scale, dest_sz[1]*scale)
    image = image.crop((int(crop_xy[0]), int(crop_xy[1]), int(crop_xy[0]+crop_size[0]), int(crop_xy[1]+crop_size[1])))
    # resize it
    image = image.resize(dest_sz, Image.ANTIALIAS)
    return image

'''
	Take an image opened with cv2.imread() as input
	Detect if the image contains a face
	Returns the face in gray scale and the cooridinate where
	the face has been found. If no face has been detected than
	returns None
'''

def detect_face(img):
    #convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #load OpenCV face detector, I am using LBP which is fast
    #there is also a more accurate but slow Haar classifier
    #face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')
    face_cascade = cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml")

    #let's detect multiscale (some images may be closer to camera than others) images
    #result is a list of faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, 1, (100,100))

    #if no faces are detected then return original img
    if (len(faces) == 0):
        return None, None

    #under the assumption that there will be only one face,
    #extract the face area
    (x, y, w, h) = faces[0]

    gray = cv2.resize(gray[y:y+w, x:x+h], (300,300))

    #return only the face part of the image
    return gray, faces[0]

recognizer = cv2.createLBPHFaceRecognizer()
#recognizer = cv2.createEigenFaceRecognizer()
#recognizer = cv2.createFisherFaceRecognizer()

def recognize(img, rcg_path, subjects):
	# carico il recognizer necessario per riconoscere gli autisti di una determinata auto
	recognizer.load(rcg_path)
	#rilevo la faccia dell'autista nella foto
	gray, rect = face.detect_face(img)
	if(gray != None):
		label, confidence = recognizer.predict(gray)
		#print "label = " + str(label) + " conf =  " + str(confidence)
		# Ottengo il nome dell'autista legato all'indice restituito dal recognizer
		label_text = sbjs[label]
		# Disegno un rettangolo e scrivo il nome intorno alla faccia rilevata
		face.draw_rectangle(img, rect)
		if(confidence < 50):
			face.draw_text(img, label_text, rect[0], rect[1]-5)
			return img, sbjs[label]
		else:
			face.draw_text(img, "Sconosciuto", rect[0], rect[1]-5)
			return img, "Sconosciuto"
	return None, None 
