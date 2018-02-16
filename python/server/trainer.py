import os
import cv2
import numpy as np
import face

data_folder_path = 'training-data'

#------STEP-1--------
#get the directories (one directory for each subject) in data folder
dirs = os.listdir(data_folder_path)
    
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
for dir_name in dirs:
        
    #our subject directories start with letter 's' so
    #ignore any non-relevant directories if any
    if not dir_name.startswith("s"):
        continue;
            
    #------STEP-2--------
    #extract label number of subject from dir_name
    #format of dir name = slabel
    #, so removing letter 's' from dir_name will give us label
    label = int(dir_name.replace("s", ""))
        
    #build path of directory containin images for current subject subject
    #sample subject_dir_path = "training-data/s1"
    subject_dir_path = data_folder_path + "/" + dir_name
    
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
            print label
        
cv2.destroyAllWindows()
cv2.waitKey(1)
cv2.destroyAllWindows()

print("Data prepared")

#print total faces and labels
print("Total faces: ", len(faces))
print("Total labels: ", len(labels))

face_recognizer.train(faces, np.array(labels))
face_recognizer.save('face_recognizer.xml')

'''
if face_recognizer.train(faces, np.array(labels)) != None:
	print "Train sucessfully complete"
	face_recognizer.save("face_recognizer.xml")
else:
	print "Train error"
'''
