import numpy as np
import cv2
import time
Starting_Time_Using_Time = time.time(); # Record Starting Time
# Get the required Classifiers
profile_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.3.0/data/haarcascades/haarcascade_profileface.xml')
face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.3.0/data/haarcascades/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture('/home/pi/OpenCV_Project/Test Samples Input/Test_3.mp4')
# Get frames width and height, fps and number of frames
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print('Test: 3')
print('FPS: %d'%fps)
print('Total Number of frames: %d'%length)
print('Length in Seconds: %f'%(length/fps))

out = cv2.VideoWriter('/home/pi/OpenCV_Project/Test_3_Result.avi',cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width,height))

while(True):
    ret, frame = cap.read()
    length=length-1;	# Calculate the remaining number of frames
    if length < 0:	# Break the loop after the last frame
        break
    if ret is True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        continue # If the frame is corrupted, ignore it
    profiles = profile_cascade.detectMultiScale(gray, 1.3, 4)
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
    for (x,y,w,h) in faces: # Applying the first classifier
        sub_face = frame[y:y+h, x:x+w]
        # apply a gaussian blur on this new recangle image
        sub_face = cv2.GaussianBlur(sub_face,(23, 23), 30)
        # merge this blurry rectangle to the current frame
        frame[y:y+sub_face.shape[0], x:x+sub_face.shape[1]] = sub_face
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

    for (x,y,w,h) in profiles:	# Applying the second classifier
        sub_face = frame[y:y+h, x:x+w]
        # apply a gaussian blur on this new recangle image
        sub_face = cv2.GaussianBlur(sub_face,(23, 23), 30)
        # merge this blurry rectangle to the current frame
        frame[y:y+sub_face.shape[0], x:x+sub_face.shape[1]] = sub_face
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
    out.write(frame)

Ending_Time_Using_Time = time.time(); # Record time after video processing
Elapsed_Time_Time = Ending_Time_Using_Time - Starting_Time_Using_Time;
print('Elapsed_Time_Time: %d'%Elapsed_Time_Time) # Print the processing time
cap.release()
out.release()
cv2.destroyAllWindows()
