import cv2
import os
import time
import numpy as np
import HandTrackingModule as htm
from PIL import Image
from numpy import asarray

################
brushThickness = 15
eraserThickness = 50

################
folderPath = "Header"
myList = os.listdir(folderPath)
overlayList = []
for imgPath in myList:
    image = cv2.imread(f'{folderPath}/{imgPath}')
    overlayList.append(image)
header = overlayList[0]
drawColor = (255,0,255)
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 450)
imgCanvas = np.zeros((480,640,3),np.uint8)
detector = htm.handDetector(detectionCon=0.85)
xp,yp = 0,0



while True:
    success, img = cap.read()
    img = cv2.flip(img,1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    if len(lmList)!=0:



        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

        fingers = detector.fingersUp()


        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print("selection mode")
            #checking
            if y1<125:
                if 0 < x1 <100:
                    imgCanvas = np.zeros((480, 640, 3), np.uint8)
                elif 125 < x1 < 225:
                    header = overlayList[0]
                    drawColor=(255,0,255)
                elif 275 < x1 < 375:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 400 < x1 < 475:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 500 < x1 < 575:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        if fingers[1] and fingers[2]==False:
            cv2.circle(img, (x1, y1), 10 ,drawColor, cv2.FILLED)
            print("Drawing mode")
            if xp==0 and yp ==0:
                xp,yp = x1,y1

            if drawColor==(0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1


        if not fingers[0] and  fingers[1] and fingers[2] and  fingers[3] and not fingers[4]:
            image = Image.open('rickroll_4k.png')
            np_img = np.array(image)
            np_img = cv2.cvtColor(np_img, cv2.COLOR_BGR2RGB)

            cv2.imshow("Rickroll", np_img)
            cv2.waitKey(1)
            time.sleep(3)
            cv2.destroyWindow("Rickroll")


    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)

    #setting the header image
    img[0:125, 0:640] = header
    #img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Image",img)
    #cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)
