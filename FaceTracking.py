import cv2
import numpy as np
from djitellopy import tello
import time

# Small Area Around Face => Too Far => Move Forward // area < 6200px
# Big Area Around Face => Too Close => Move Backward // area > 6800px
# Area Around Face Within Acceptable Range => Stay // 6200px < area < 6800px
# Face Left of Center Point => Yaw Counter Clockwise
# Face Right of Center Point => Yaw Clockwise

tello = tello.Tello()
tello.connect()
print(tello.get_battery())
tello.streamon()
tello.takeoff()
tello.send_rc_control(0, 0, 25, 0)

time.sleep(2.5)

pid = [0.4, 0.4, 0]
pError = 0
width, height = 360, 240


def findFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)  # Detect Face

    myFacesCenter = []
    myFacesArea = []

    # Draw Rectangle Around Face
    for (x, y, width, height) in faces:
        cv2.rectangle(img, (x, y), (x + width, y + height), (0, 0, 255), 2)

        # Find Center Point & Draw
        centerX = x + (width // 2)
        centerY = y + (height // 2)
        cv2.circle(img, (centerX, centerY), 5, (0, 255, 0), cv2.FILLED)

        # Find Area of Rectangle
        area = width * height

        # Parallel Arrays
        myFacesCenter.append([centerX, centerY])
        myFacesArea.append(area)

    if len(myFacesArea) != 0:
        # Gives us the index location of the max area in list
        i = myFacesArea.index(max(myFacesArea))
        return img, [myFacesCenter[i], myFacesArea[i]]

    else:
        return img, [[0, 0], 0]


def trackFace(info, width, pid, pError):
    minArea, maxArea = 6200, 6800
    centerX, centerY = info[0]
    area = info[1]
    forwardBackward = 0
    error = centerX - width // 2

    yaw = pid[0] * error + pid[1] * (error - pError)
    yaw = int(np.clip(yaw, -100, 100))

    # Green Zone
    if minArea < area < maxArea:
        forwardBackward = 0

    # Too Close
    elif area > maxArea:
        forwardBackward = -20

    # Too Far
    elif area < minArea and area != 0:
        forwardBackward = 20

    if centerX == 0:
        yaw = 0
        error = 0

    tello.send_rc_control(0, forwardBackward, 0, yaw)
    return error


while True:
    img = tello.get_frame_read().frame
    img = cv2.resize(img, (width, height))

    # Info is an array where info[0] is an array containing x, y center point. info[1] is the area.
    img, info = findFace(img)
    pError = trackFace(info, width, pid, pError)
    cv2.imshow("Output", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        tello.land()
        break
