from djitellopy import Tello
import cv2
import numpy as np

area = 8100

def initializeTello():
    myDrone = Tello()
    myDrone.connect()
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0
    print(myDrone.get_battery())
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone


def telloGetframe(myDrone, w = 360, h = 240):
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame,(w,h))
    return img




def findFaces(img):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray,1.2,4)

    myFaceListC = []
    myFaceListArea = []

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
        cx = x+w //2
        cy = y+h //2
        area = w*h
        print(str(area)*20,end='\n')
        myFaceListArea.append(area)
        myFaceListC.append([cx,cy])

    if len(myFaceListArea) !=0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img,[myFaceListC[i],myFaceListArea[i]]
    else:
        return img,[[0,0],0]


def trackFace(myDrone,info,w,h,pidYaw,pidFor,pError):

    ## pid yaw
    error = info[0][0]-w//2
    speedYaw = pidYaw[0]*error + pidYaw[1]*(error-pError)
    speedYaw = int(np.clip(speedYaw,-100,100))
    print(f'the yaw speed is : {speedYaw}')
    ## pid for
    error = info[0][0] - h//2
    speedFor = pidFor[0] * error + pidFor[1] * (error - pError)
    speedFor = int(np.clip(speedFor, -100, 100))
    print(f'the Forward speed is : {speedFor}')

    if info[0][0] !=0:
        myDrone.yaw_velocity = speedYaw
        myDrone.for_back_velocity = speedFor
    else:
        myDrone.for_back_velocity = 0
        myDrone.left_right_velocity = 0
        myDrone.up_down_velocity = 0
        myDrone.yaw_velocity = 0
        error = 0

    if myDrone.send_rc_control:
        myDrone.send_rc_control(myDrone.left_right_velocity,
                                myDrone.for_back_velocity,
                                myDrone.up_down_velocity,
                                myDrone.yaw_velocity)

    return error