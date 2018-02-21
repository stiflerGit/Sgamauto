from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

cam = PiCamera()
cam.resolution = (640, 480)
cam.framerate = 32
rawCapture = PiRGBArray(cam, size=(640, 480))

time.sleep(0.1)
def getFacePicture:
	face = None
	while face == None:
		for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
			img = frame.array
			face, rect = face.detect_face(img)
			# show the frame
			cv2.imshow("Frame", img)
			key = cv2.waitKey(10) & 0xFF
			# clear the stream in preparation for the next frame
			rawCapture.truncate(0)

##
##while True:    
##    with picamera.array.PiRGBArray(cam) as stream:
##        cam.capture(stream, format='bgr')
##        # At this point the image is available as stream.array
##        img = stream.array
##    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
##    faces = faceCascade.detectMultiScale(gray, 1.2,5)
##    for(x,y,w,h) in faces:
##        cv2.rectangle(img,(x,y),(x+w,y+h),(225,0,0),2)
##        Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
##        print("confidence = ", conf)
##        if(Id==1):
##            Id="Stefano"
##        elif(Id==2):
##            Id="Michele"
##        else:
##            Id="Unknown"
##        cv2.cv.PutText(cv2.cv.fromarray(img),str(Id), (x,y+h),font, 255)
##        
##    cv2.imshow('img',img) 
##    if cv2.waitKey(10) & 0xFF==ord('q'):
##        break
    

