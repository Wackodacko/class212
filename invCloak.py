from typing import final
import cv2
import time
import numpy as np

#This IS TO SAVE THE OUTPUT IN A FILE OUTPUT.AVI 
fourcc=cv2.VideoWriter_fourcc(*'XVID')
output_file=cv2.VideoWriter("output.avi",fourcc,20.0,(640,480))

#starting the webcam
cap=cv2.VideoCapture(0)

#allowing the camera to start
time.sleep(2)
bg=0

#capturing th background in 60frames
for i in range(60):
    ret,bg=cap.read()
bg=np.flip(bg,axis=1)

#reading the captured frame until the camera is open
while(cap.isOpened()):
    ret,img=cap.read()
    if not ret:
        break
    img=np.flip(img,axis=1)

    #converting the color from BGR to HSV(hue, saturation, value)
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #generating mask to detect the red color

    lower_red=np.array([0,120,50])
    upper_red=np.array([30,255,255])
    mask_1=cv2.inRange(hsv,lower_red,upper_red)
    
    lower_red=np.array([170,120,70])
    upper_red=np.array([180,255,255])
    mask_2=cv2.inRange(hsv,lower_red,upper_red)
    mask_1=mask_1+mask_2

    #open and expand image where ther is mask1
    mask_1=cv2.morphologyEx(mask_1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask_1=cv2.morphologyEx(mask_1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))

    #selecting the only part that does not have red and saving in mask_1
    mask_2 = cv2.bitwise_not(mask_1)

    res1=cv2.bitwise_and(img,img,mask=mask_2)
    res2=cv2.bitwise_and(img,img,mask=mask_1)
    
    #generating the final output bu merging res1 and res2
    finalOutput=cv2.addWeighted(res1,1,res2,1,0)
    output_file.write(finalOutput)
    cv2.imshow("magic",finalOutput)
    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()

