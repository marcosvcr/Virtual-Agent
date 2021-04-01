import numpy as np
import imutils
import time
import cv2



class Motion:

    master = None

    def __init__(self):
        self.master = None



    def detect(self, frame):

        frame1 = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        # blur frame
        frame2 = cv2.GaussianBlur(frame1,(15,15),0)

        # initialize master
        if self.master is None:
            self.master = frame2
        # delta frame
        frame3 = cv2.absdiff(self.master,frame2)

        # threshold frame
        frame4 = cv2.threshold(frame3,15,255,cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes
        kernel = np.ones((2,2),np.uint8)
        frame5 = cv2.erode(frame4,kernel,iterations=4)
        frame5 = cv2.dilate(frame5,kernel,iterations=8)

        # find contours on thresholded image
        contours,none2 = cv2.findContours(frame5.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        # make coutour frame
        frame6 = frame.copy()

        # target contours
        targets = []

        # loop over the contours
        for c in contours:
            
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 500:
                    continue

            # contour data
            M = cv2.moments(c)#;print( M )
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(c)
            rx = x+int(w/2)
            ry = y+int(h/2)
            ca = cv2.contourArea(c)

            # plot contours
            cv2.drawContours(frame6,[c],0,(0,0,255),2)
            cv2.rectangle(frame6,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.circle(frame6,(cx,cy),2,(0,0,255),2)
            cv2.circle(frame6,(rx,ry),2,(0,255,0),2)

            # save target contours
            targets.append((cx,cy,ca))

        # update master
        self.master = frame2
        print(targets)
        return targets