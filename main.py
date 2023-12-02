import cv2
import os
from cvzone.HandTrackingModule import HandDetector
import numpy as np


# Variables
width, height = 1280, 720
folderPath = 'presentation'

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# GEt the list of presentation images

files = os.listdir(folderPath)
pathImage = sorted(files, key=lambda x: int(x.split('.')[0]))
# print(pathImage)

# Variables
imgNumber = 0
hs, ws = int(120*3), int(213*3) #width and height for the presentation
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 5
annotations = [[]]
annotationNumber = 0
annotationStart = False
# common_size = (width, height)

# Hand Detector
detector = HandDetector(detectionCon = 0.8, maxHands = 1)

while True:
    # Import Images
    success, webcam = cap.read()
    webcam = cv2.flip(webcam, 1)
    pathFullImage = os.path.join(folderPath, pathImage[imgNumber])
    presentation = cv2.imread(pathFullImage)

    hands, webcam = detector.findHands(webcam) #, flipType = False
    # cv2.line(webcam, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)
    cv2.line(webcam, (0, gestureThreshold), (width, gestureThreshold), (192, 192, 192), 10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']

        lmList = hand['lmList'] #-> LandMark

        # Constrain values for easier drawing
        indexFinger = lmList[8][0], lmList[8][1]

        xVal = int(np.interp(lmList[8][0], [width//2, width-200], [0, width*1.5]))
        yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height*1.5]))
        indexFinger = xVal, yVal

        # print(fingers)

        if cy <= gestureThreshold: # if hand is at the height of th face.
            annotationStart = False

            # Gesture 1 - Left
            if fingers == [1, 0, 0, 0, 0]:
                annotationStart = False
                if imgNumber > 0:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    imgNumber -= 1
                    # print('Left')

            # gesture 2 - Right
            if fingers == [0, 0, 0, 0, 1]:
                annotationStart = False
                if imgNumber < len(pathImage)-1:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    imgNumber += 1
                    # print('Right')

        # Gesture 3 - Show Pointer
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(presentation, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            annotationStart = False

        # Gesture 4 - Draw Pointer
        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is  False:
                annotationStart = True
                annotationNumber +=1
                annotations.append([])
            # print(annotationNumber)
            annotations[annotationNumber].append(indexFinger)
            cv2.circle(presentation, indexFinger, 12, (0, 0, 255, cv2.FILLED))
            print('\U0001F58C Writing')

        else:
            annotationStart = False

        # Gesture 5 - Erase
        if fingers == [0, 1, 1, 1, 1]:
            if annotations:
                if annotationNumber >= 0:
                    annotations.pop(-1)
                    annotationNumber -= 1
                    buttonPressed = True
                    print('\u26AA Erasing')

        # Gesture 6 - Erase All:
        if fingers == [1, 1, 1, 1, 1]:
            annotations = [[]]
            annotationNumber = 0
            buttonPressed = True
            print("\U0001F4A3 \U0001F4A3  Erasing All \U0001F4A3 \U0001F4A3")

        # print(annotationNumber)

    else:
        annotationStart = False

    # Button Pressed iterations
    if buttonPressed:
        buttonCounter +=1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range (len(annotations)):
        for j in range(len(annotations[i])):
            if j !=0:
                cv2.line(presentation, annotations[i][j-1], annotations[i][j], (0, 0, 200), 12)


    # Adding webcam on the slide s
    cam_img = cv2.resize(webcam, (ws, hs))
    h, w, _ = presentation.shape
    presentation[0:hs, w-ws:w] = cam_img

   # presentation = cv2.resize(presentation, common_size)


    #cv2.imshow('webcam', webcam)
    cv2.imshow('presentation', presentation)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break