from utlis import *
import cv2

w, h = 360,240
pidYaw = [0.5,0.5,0]
pidFor = [0.2,0.2,0]
pError = 0
startCounter = 0

myDrone  = initializeTello()

while True:

    ## flight
    if startCounter ==0:
        myDrone.takeoff()
        startCounter = 1

    ##step 1
    img = telloGetframe(myDrone,w,h)
    ##step 2
    img,info = findFaces(img)
    print(info[0][0])
    ##step 3
    pError = trackFace(myDrone,info,w,h,pidYaw,pidFor,pError)

    cv2.imshow('image',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break

